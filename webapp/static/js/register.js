// Esegue il codice solo dopo che l'intera pagina è stata caricata
document.addEventListener("DOMContentLoaded", function() {

    // Recupera il form di registrazione
    const form = document.getElementById("registerForm");
    if (!form) return; // Se il form non esiste, interrompe l'esecuzione

    // Aggiunge un listener all'evento "submit" del form
    form.addEventListener("submit", function(event) {

        // Recupera i valori dei campi password e conferma password
        const pwd = document.getElementById("password").value;
        const confirm = document.getElementById("confirm_password").value;

        // Box che mostra eventuali errori
        const errorBox = document.getElementById("passwordError");

        // Controllo: le due password devono coincidere
        if (pwd !== confirm) {

            event.preventDefault(); // Blocca l'invio del form

            errorBox.classList.remove("d-none"); // Mostra il messaggio di errore

        } else {

            errorBox.classList.add("d-none"); // Nasconde l'errore se tutto è valido
        }
    });
});