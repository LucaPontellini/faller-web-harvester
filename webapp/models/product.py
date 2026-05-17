class Product:
    def __init__(self, data):
        d = dict(data)

        # Identificativi e stato del prodotto
        self.code = d.get('code')                 # Codice del prodotto (es. 130026)
        self.exists = d.get('exists', 0)          # 1 = trovato, 0 = non trovato
        self.product_link = d.get('product_link') # Link alla pagina ufficiale del prodotto


        # Informazioni principali
        self.name = d.get('name')                        # Nome del prodotto
        self.price = d.get('price', 'N/A')               # Prezzo
        self.availability = d.get('availability', 'N/A') # Stato di disponibilità
        self.category = d.get('category', 'N/A')         # Categoria
        self.ean = d.get('ean', 'N/A')                   # Codice EAN


        # Dettagli tecnici
        self.scale_image = d.get('scale_image')            # Immagine del badge della scala (G, H0, N, Z)
        self.epoch = d.get('epoch', 'N/A')                 # Epoca ferroviaria (I, II, ..., VI)
        self.dimensions = d.get('dimensions', 'N/A')       # Dimensioni (in mm)
        self.difficulty = d.get('difficulty', 'N/A')       # Difficoltà di montaggio (facile, moderata, ...)
        self.delivery_date = d.get('delivery_date', 'N/A') # Data prevista di arrivo in magazzino


        # Campi extra richiesti
        self.lighting_or_electronics = d.get('lighting_or_electronics', 'N/A')   # Luci comprese nel kit o elettronica (servomotori, ...)
        self.construction_instruction = d.get('construction_instruction', 'N/A') # Numero di istruzioni
        self.kit_contains = d.get('kit_contains', 'N/A')                         # Contenuto del kit


        # Testi e media
        self.description = d.get('description', '')  # Descrizione testuale
        self.image_main = d.get('image_main')        # Immagine principale


        # Galleria delle immagini secondarie (photo_1 ... photo_10)
        self.all_photos = [
            d.get(f'photo_{i}') for i in range(1, 11)
            if d.get(f'photo_{i}') and d.get(f'photo_{i}') != 'N/A'
        ]

        # Layout / piante (layout_1 ... layout_10)
        self.all_layouts = [
            d.get(f'layout_{i}') for i in range(1, 11)
            if d.get(f'layout_{i}') and d.get(f'layout_{i}') != 'N/A'
        ]

        # Documenti PDF
        self.manual_pdf = d.get('manual_pdf')   # Manuale PDF
        self.safety_pdf = d.get('safety_pdf')   # Scheda di sicurezza PDF