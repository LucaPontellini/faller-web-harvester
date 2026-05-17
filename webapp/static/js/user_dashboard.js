/* Filtro live + evidenziazione + selezione con INVIO */
document.getElementById('filterInput')?.addEventListener('keyup', function(e) {
    const val = this.value.toLowerCase().trim();
    const rows = document.querySelectorAll("#productsTable tbody tr");
    let visibleRows = [];

    // Filtro istantaneo
    rows.forEach(row => {
        row.classList.remove('row-highlight'); // Rimuove l'evidenziazione precedente
        if(row.innerText.toLowerCase().includes(val)) {
            row.style.display = '';
            visibleRows.push(row);
        } else {
            row.style.display = 'none';
        }
    });

    // Se premi INVIO
    if (e.key === "Enter" && val !== "") {
        if (visibleRows.length > 0) {
            const target = visibleRows[0];
            
            // Scroll alla riga trovata
            target.scrollIntoView({ behavior: 'smooth', block: 'center' });
            
            // Evidenzia la riga
            target.classList.add('row-highlight');
            
            // Seleziona la checkbox
            const cb = target.querySelector('.product-cb');
            if(cb) {
                cb.checked = true;
                updateCounter();
            }
        }
    }
});

/* Contatore checkbox selezionate */
const countLabel = document.getElementById('count');
function updateCounter() { 
    if(countLabel) countLabel.innerText = document.querySelectorAll('.product-cb:checked').length; 
}

/* Selezione/deselezione globale (master checkbox) */
document.getElementById('masterCheck')?.addEventListener('change', function() {
    document.querySelectorAll('.product-cb').forEach(c => { 
        if(c.closest('tr').style.display !== 'none') c.checked = this.checked; 
    });
    updateCounter();
});

/* Aggiornamento del contatore al cambio singola checkbox */
document.querySelectorAll('.product-cb').forEach(c => c.addEventListener('change', updateCounter));

/* Eliminazione del singolo prodotto */
function deleteSingle(code) {
    if(confirm(`Eliminare definitivamente il prodotto ${code} e i suoi file?`)) {
        fetch(`/api/scraping/delete_product/${code}`, { method: 'DELETE' })
        .then(res => {
            if(res.ok) {
                document.querySelector(`tr[data-code="${code}"]`)?.remove();
                updateCounter();
            } else {
                alert("Errore durante l'eliminazione.");
            }
        });
    }
}

/* Esportazione ZIP dei prodotti selezionati */
function zipSelected() {
    const selected = Array.from(document.querySelectorAll('.product-cb:checked')).map(c => c.value);
    if (selected.length === 0) return alert("Seleziona prodotti!");
    const codesParam = selected.join(',');
    
    // Unisce il prefisso del Blueprint (/api/export) alla rotta (/download/zip)
    window.location.href = `/api/export/download/zip?codes=${codesParam}`;
}

/* Eliminazione multipla dei prodotti selezionati */
function deleteSelected() {
    const selected = Array.from(document.querySelectorAll('.product-cb:checked')).map(c => c.value);
    if (selected.length === 0) return alert("Seleziona prodotti!");
    
    if(confirm(`Eliminare ${selected.length} prodotti e i relativi file di export (Excel/ZIP)?`)) {
        fetch('/api/scraping/delete_selected', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ codes: selected })
        })
        .then(res => res.json())
        .then(data => {
            if(data.status === "success") {
                location.reload();
            } else {
                alert("Errore durante l'eliminazione di gruppo.");
            }
        });
    }
}