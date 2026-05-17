# Dizionario dei selettori CSS utilizzati dal parser.
# Ogni chiave rappresenta un elemento della pagina del prodotto della Faller e il valore è un selettore compatibile con più varianti del sito.

# ======================================================================================================================================================================================
# ATTENZIONE:
# Questi selettori CSS funzionano solo finché la struttura HTML del sito Faller rimane invariata.
# Se Faller aggiorna il layout, rinomina classi, cambia contenitori o riscrive la pagina prodotto, sarà necessario rivedere manualmente questi selettori e aggiornarli di conseguenza.
# ======================================================================================================================================================================================

SELECTORS = {
    # Titolo del prodotto (supporta il layout vecchio e nuovo)
    "product_title": "h1.product--title, .product--info h1",

    # Prezzo (sia blocco visivo che meta tag)
    "price": ".product--price.price--default, .price--content meta[itemprop='price']",

    # Proprietà tecniche: righe e valori (tabella o lista)
    "properties_row": ".product--properties-row, .product--properties-list .product--properties-entry",
    "properties_label": ".product--properties-label, .product--properties-label-name",
    "properties_value": ".product--properties-value, .product--properties-value-content",

    # Badge della scala (G, H0, N, Z) — fondamentale per la scala corretta
    "gauge_badge": ".js--gauge-info, .product--attributes .gauge--H0, "
                   ".product--attributes .gauge--N, .gauge img",

    # Disponibilità (contenitore e icona)
    "availability_container": ".product--delivery, .delivery--status",
    "availability_icon": ".delivery--status-icon, .buybox--button .delivery--status-icon",

    # Descrizione del prodotto
    "description": ".product--description, .content--description",

    # Immagine principale (diverse versioni del sito)
    "img_main": ".product--image-container img, .image-gallery--image img, "
                ".image-slider--item img",

    # Immagini della galleria (HD)
    "gallery_images": ".image-slider--item .image--element img, "
                      ".image-slider--item img"
}