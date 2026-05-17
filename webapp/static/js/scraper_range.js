// Listener principale: intercetta l'invio del form
document.getElementById('scraping-form').onsubmit = async (e) => {
    e.preventDefault();

    const start = parseInt(document.getElementById('start_code').value);
    const end = parseInt(document.getElementById('end_code').value);

    // Validazione: blocca numeri negativi
    if (start < 0 || end < 0) {
        alert("I codici non possono essere negativi.");
        return;
    }

    // Validazione: impedisce intervalli invertiti
    if (start > end) {
        alert("Il codice iniziale deve essere minore o uguale al codice finale.");
        return;
    }

    const btn = document.getElementById('start-btn');
    const status = document.getElementById('status-area');

    // Funzione di blocco dell'UI durante l’elaborazione
    btn.disabled = true;
    status.classList.remove('d-none');

    const data = { start, end };

    // Funzione che invia la richiesta al backend delle API
    const response = await fetch('/api/scraping/start', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
    });

    // Funzione di gestione del risultato
    if (response.ok) {
        alert("Scaricamento completato con successo!");
        window.location.href = "/dashboard";
    } else {
        alert("Errore durante lo scaricamento.");
        btn.disabled = false;
        status.classList.add('d-none');
    }
};