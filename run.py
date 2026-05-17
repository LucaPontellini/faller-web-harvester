from webapp import create_app

# Crea l'app Flask usando la factory function definita nel pacchetto webapp
app = create_app()

# Avvio dell'applicazione solo se il file viene eseguito direttamente
if __name__ == "__main__":
    # debug=True → ricarica automatico ed errori dettagliati
    # host='127.0.0.1' → accessibile solo in locale
    # port=5000 → porta standard Flask
    app.run(debug=True, host='127.0.0.1', port=5000)