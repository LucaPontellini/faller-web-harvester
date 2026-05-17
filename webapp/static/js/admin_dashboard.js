// Timer per il polling dello stato dello scraper
let syncInterval = null;

// Indice dell’ultimo log mostrato nella console
let lastLogIndex = 0;

// Inizializzato a 0 in modo nativo JavaScript (niente più tag Jinja qui dentro)
let totalProducts = 0;

// Scrive una riga nella console nera della dashboard. Applica una colorazione intelligente in base al contenuto del testo.
function writeToConsole(text) {
    const box = document.getElementById("logBox");
    const div = document.createElement("div");
    
    // Colorazione condizionale avanzata
    if (text.includes("[OK]")) div.style.color = "#00ff9d";
    else if (text.includes("[ERR]")) div.style.color = "#ff4444";
    else if (text.includes("[WARN]")) div.style.color = "#ffcc00";
    else if (text.includes("---")) div.style.color = "#ffffff"; // Separatori
    else div.style.color = "#00d2ff";
    
    div.innerText = text;
    box.appendChild(div);
    box.scrollTop = box.scrollHeight; // Scroll automatico verso il basso
}

// Aggiorna in tempo reale i numeri delle card statistiche senza ricaricare la pagina.
function updateStats() {
    fetch("/admin/get-stats")
        .then(r => r.json())
        .then(data => {
            // Aggiorna i numeri nelle card
            document.getElementById("total-count").innerText = data.total_products;
            document.getElementById("img-count").innerText = data.total_photos;
            document.getElementById("pdf-count").innerText = data.total_pdfs;
            
            // Stampa eventuali log tecnici aggiuntivi
            if (data.detailed_log) {
                writeToConsole(data.detailed_log);
            }
        })
        .catch(err => console.error("Errore aggiornamento stats:", err));
}

// Quando la pagina è pronta carica le stats e recupera in sicurezza la variabile del backend dall'HTML
document.addEventListener("DOMContentLoaded", function() {
    const container = document.getElementById("dashboardContainer");
    if (container) {
        totalProducts = parseInt(container.getAttribute("data-total-products")) || 0;
    }
    updateStats();
});

// Polling periodico dello stato dello scraper. Aggiorna barra di progresso, log e stato finale.
function pollStatus() {
    fetch("/admin/scraper-progress")
        .then(r => r.json())
        .then(data => {
            // Aggiorna barra di avanzamento
            document.getElementById("bar").style.width = data.progress + "%";
            document.getElementById("barText").innerText = data.progress + "%";

            // Stampa nuovi log
            if (data.log.length > lastLogIndex) {
                for (let i = lastLogIndex; i < data.log.length; i++) {
                    writeToConsole(data.log[i]);
                }
                lastLogIndex = data.log.length;
            }

            // Se lo scraper ha finito
            if (!data.running && data.progress >= 100) {
                document.getElementById("statusText").innerText = "READY";
                document.getElementById("statusSubText").innerText = "OPERAZIONE COMPLETATA";
                clearInterval(syncInterval);

                // Aggiorna le card dopo la scansione
                updateStats();
            }
        });
}

// Esegue un'azione amministrativa (reset, delete, run scraper, ecc.) con protezioni intelligenti e reset dell’interfaccia.
function runAction(url, method = 'GET') {
    const isResetAction = url.includes('reset-catalog');
    const isDeleteFiles = url.includes('delete-assets');

    // Blocco intelligente: evita azioni inutili su DB vuoto
    if (totalProducts === 0 && !isResetAction && !isDeleteFiles) {
        writeToConsole("[WARN] Azione annullata: il database è già vuoto.");
        return;
    }

    // Reset UI prima di ogni comando
    clearInterval(syncInterval);
    document.getElementById("logBox").innerHTML = "";
    document.getElementById("bar").style.width = "0%";
    document.getElementById("statusText").innerText = "RUNNING";
    document.getElementById("statusSubText").innerText = "IN CORSO...";
    lastLogIndex = 0;

    // Avvia polling
    syncInterval = setInterval(pollStatus, 800);
    
    fetch(url, { method: method })
        .then(response => response.json())
        .then(data => {
            // Se il reset catalogo è andato a buon fine
            if (isResetAction && data.status === "success") {
                totalProducts = 0;
                writeToConsole("[OK] Database sincronizzato: 0 prodotti.");
                updateStats(); // Aggiorna le card
            }
        })
        .catch(err => {
            writeToConsole("[ERR] Errore durante l'esecuzione dell'azione.");
            clearInterval(syncInterval);
        });
}

// Avvia l’esportazione Excel con messaggi di feedback.
function exportExcel() {
    if (totalProducts === 0) {
        writeToConsole("[WARN] Esportazione impossibile: database vuoto.");
        return;
    }

    writeToConsole("[INFO] Generazione file Excel...");
    window.location.href = "/admin/export-excel";

    // Feedback immediato (dato che il redirect non pulisce la console)
    setTimeout(() => {
        writeToConsole("[OK] Download avviato.");
    }, 1000);
}

// Mostra un popup di conferma prima di eliminare file fisici dal server.
function confirmDelete(type) {
    if (confirm("Sei sicuro di voler eliminare tutti i file " + type + "? Questa azione cancellerà i file fisici dal server.")) {
        runAction('/admin/delete-assets/' + type, 'POST');
    }
}

// Ripulisce completamente la console e resetta la UI.
function clearConsole() {
    document.getElementById("logBox").innerHTML = "<div>[INFO] Console pulita. In attesa di input...</div>";
    document.getElementById("bar").style.width = "0%";
    document.getElementById("barText").innerText = "0%";
    document.getElementById("statusText").innerText = "READY";
    document.getElementById("statusSubText").innerText = "SISTEMA PRONTO";
    lastLogIndex = 0;
}