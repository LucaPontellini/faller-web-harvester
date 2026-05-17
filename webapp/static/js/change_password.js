// Esegue il codice solo dopo che l'intera pagina è stata caricata
document.addEventListener("DOMContentLoaded", function() {

    // Recupera il form per il cambio password
    const form = document.getElementById("changePasswordForm");
    if (!form) return; // Se il form non esiste, interrompe lo script

    // Aggiunge un listener all'evento "submit" del form
    form.addEventListener("submit", function(event) {

        // Legge e pulisce i valori dei campi password
        const oldPwd = document.getElementById("old_password").value.trim();
        const newPwd = document.getElementById("new_password").value.trim();

        // Box che mostra eventuali errori
        const errorBox = document.getElementById("passwordError");

        // Controlli:
        // 1. La nuova password deve avere almeno 6 caratteri
        // 2. La nuova password deve essere diversa da quella vecchia
        if (newPwd.length < 6 || newPwd === oldPwd) {

            event.preventDefault(); // Blocca l'invio del form

            errorBox.classList.remove("d-none"); // Mostra il messaggio di errore

        } else {

            errorBox.classList.add("d-none"); // Nasconde l'errore se tutto è valido
        }
    });
});