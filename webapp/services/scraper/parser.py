import os
import re
from .client import get_soup
from webapp.services.io.downloader import download_file
from webapp.config import Config
from .selectors import SELECTORS

# Pulisce le stringhe estratte rimuovendo caratteri inutili, spazi doppi e simboli non desiderati.
def clean_val(text):
    if not text:
        return "N/A"
    clean = text.replace("✓", "").replace('"', '').replace('\n', ' ').strip()
    return " ".join(clean.split())

# Parser principale della pagina del prodotto della Faller.
# Estrae: dati base, proprietà tecniche, immagini, layout, PDF.
def parse_product_page(product_url, code):
    soup = get_soup(product_url)
    if not soup:
        return None

    # Inizializzazione della struttura dati con i valori di default
    info = {
        "code": code,
        "exists": 1,
        "product_link": product_url,

        # Dati principali
        "name": "N/A",
        "price": "N/A",
        "availability": "N/A",

        # Media
        "scale_image": "N/A",
        "description": "N/A",
        "image_main": "N/A",

        # Proprietà tecniche
        "category": "N/A",
        "ean": "N/A",
        "epoch": "N/A",
        "dimensions": "N/A",
        "difficulty": "N/A",
        "delivery_date": "N/A",
        "kit_contains": "N/A",
        "lighting_or_electronics": "N/A",
        "construction_instruction": "N/A",

        # PDF
        "manual_pdf": "N/A",
        "safety_pdf": "FALLER_Sicherheitshinweise.pdf"
    }

    # 1. Titolo e prezzo
    title = soup.select_one(SELECTORS.get("product_title", ".product--title"))
    if title:
        info["name"] = clean_val(title.get_text())

    price_meta = soup.select_one('meta[itemprop="price"]')
    if price_meta and price_meta.get("content"):
        info["price"] = price_meta.get("content") + " €"

    # 2. Disponibilità
    delivery_el = soup.select_one(".delivery--text")
    if delivery_el:
        info["availability"] = clean_val(delivery_el.get_text())
    elif soup.select_one(".alert.is--error"):
        info["availability"] = "not available"

    # 3. Proprietà tecniche (At a glance)
    mapping = {
        "dimensions": "dimensions",
        "track gauge": "scale_image",
        "epoch": "epoch",
        "kit contains": "kit_contains",
        "difficulty": "difficulty",
        "delivery date": "delivery_date",
        "kategorie": "category",
        "category": "category",
        "ean": "ean",
        "lighting/electronics": "lighting_or_electronics",
        "construction instruction": "construction_instruction"
    }

    prop_container = soup.select_one(".product--properties-content")
    if prop_container:
        labels = prop_container.select(".product--properties-label")
        for label_el in labels:
            lab_text = label_el.get_text(strip=True).lower().replace(":", "")
            if lab_text in mapping:
                db_field = mapping[lab_text]
                val_el = label_el.find_next_sibling()

                if val_el:
                    # Caso speciale: immagine della scala
                    if lab_text == "track gauge":
                        img_tag = val_el.select_one("img")
                        info[db_field] = img_tag.get("src") if img_tag else clean_val(val_el.get_text())
                    else:
                        info[db_field] = clean_val(val_el.get_text())

    # 4. Descrizione
    desc_block = soup.select_one(".product--description-block")
    if desc_block:
        info["description"] = clean_val(desc_block.get_text(separator=' ', strip=True))

    # 5. PDF: manuale, sicurezza, layout
    # Forza PDF sicurezza universale
    safety_fname = "FALLER_Sicherheitshinweise.pdf"
    info["safety_pdf"] = safety_fname

    # Scarica il PDF di sicurezza solo se non esiste già
    safety_path = os.path.join(Config.PDF_DIR, safety_fname)
    if not os.path.exists(safety_path):
        download_file(Config.STATIC_SAFETY_PDF, Config.PDF_DIR, safety_fname)

    downloads_col = soup.select_one(".column.downloads")
    if downloads_col:
        layout_idx = 1

        for link in downloads_col.select("a.link--download"):
            href = link.get("href", "")
            text = link.get_text().lower()

            # Evita di confondere PDF sicurezza con manuale
            is_safety_link = any(w in text for w in ["safety", "sicherheit", "sicurezza"])

            # Manuale
            if ("manual" in text or "anleitung" in text) and not is_safety_link:
                fname = f"{code}_manual.pdf"
                if download_file(href, Config.PDF_DIR, fname):
                    info["manual_pdf"] = fname

            # Layout (max 10)
            elif "layout" in text and layout_idx <= 10:
                ext = href.split('.')[-1].lower().split('?')[0]
                if ext not in ['jpg', 'png', 'pdf']:
                    ext = 'jpg'

                fname = f"{code}_layout_{layout_idx}.{ext}"
                if download_file(href, Config.IMG_DIR, fname):
                    info[f"layout_{layout_idx}"] = fname
                    layout_idx += 1

    # 6. Immagini in HD e galleria
    seen_urls = set()

    # Immagine principale
    main_el = soup.select_one(".image-slider--item .image--element")
    if main_el:
        m_url = main_el.get("data-img-original") or main_el.get("src")
        if m_url:
            fname = f"{code}_main.jpg"
            if download_file(m_url, Config.IMG_DIR, fname):
                info["image_main"] = fname
                seen_urls.add(m_url)

    # Galleria delle immagini (HD)
    photo_idx = 1
    for thumb_link in soup.select("a.thumbnail--link"):
        if photo_idx > 10:
            break

        img_url = thumb_link.get("href")
        if not img_url or img_url in seen_urls:
            continue

        fname = f"{code}_photo_{photo_idx}.jpg"
        if download_file(img_url, Config.IMG_DIR, fname):
            info[f"photo_{photo_idx}"] = fname
            seen_urls.add(img_url)
            photo_idx += 1

    return info