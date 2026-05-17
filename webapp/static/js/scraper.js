// Listener principale: intercetta l'invio del form e avvia il processo di scraping
document.getElementById('scraper-form').addEventListener('submit', async (e) => {
    e.preventDefault();

    const codesArea = document.getElementById('codes');
    const btn = document.getElementById('start-btn');
    const progressArea = document.getElementById('progress-area');
    const progressBar = document.getElementById('progress-bar');
    const statusText = document.getElementById('status-text');

    // Funzione di estrazione e pulizia dei codici inseriti
    const rawCodes = codesArea.value
        .split(/[\n,]+/)
        .map(c => c.trim())
        .filter(c => c.length > 0);

    // Funzione di validazione: accetta solo numeri interi positivi
    const codes = rawCodes.filter(c => /^[0-9]+$/.test(c));

    if (codes.length === 0) {
        alert("Inserisci almeno un codice prodotto valido (solo numeri positivi)!");
        return;
    }

    if (codes.length !== rawCodes.length) {
        alert("Alcuni codici non sono validi. Inserisci solo numeri interi positivi, senza spazi o simboli.");
        return;
    }

    // Funzione di blocco dell'UI durante l’elaborazione
    btn.disabled = true;
    btn.innerText = "Scaricamento...";
    progressArea.classList.remove('d-none');

    let progress = 0;

    // Funzione di avanzamento fittizio della progress bar
    const interval = setInterval(() => {
        if (progress < 90) {
            progress += Math.random() * 10;

            progressBar.style.width = progress + '%';
            progressBar.innerText = Math.floor(progress) + '%';
            statusText.innerText = "Elaborazione prodotti...";
        }
    }, 400);

    try {
        // Funzione di invio richiesta al backend delle API
        const response = await fetch('/api/scraping/start', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ codes: codes })
        });

        const result = await response.json();

        clearInterval(interval);

        // Funzione di completamento dell'UI
        progressBar.style.width = '100%';
        progressBar.innerText = '100%';
        statusText.innerText = "Completato!";

        setTimeout(() => {
            window.location.href = "/dashboard";
        }, 800);

    } catch (err) {
        console.error(err);

        clearInterval(interval);

        // Funzione di gestione errori lato client
        progressBar.classList.remove('progress-bar-animated');
        progressBar.classList.add('bg-danger');

        statusText.innerText = "Errore di connessione al server.";

        btn.disabled = false;
        btn.innerText = "Avvia Scaricamento";
    }
});