// Attende che tutta la pagina sia stata caricata
document.addEventListener("DOMContentLoaded", function() {

    // Recupera il form di login
    const form = document.getElementById("loginForm");
    if (!form) return; // Se il form non esiste, interrompe lo script

    // Aggiunge un listener all'evento "submit" del form
    form.addEventListener("submit", function(event) {

        // Legge e pulisce i valori dei campi username e password
        const user = document.getElementById("username").value.trim();
        const pwd = document.getElementById("password").value.trim();

        // Box che mostra l'errore
        const errorBox = document.getElementById("loginError");

        // Controllo: username e password devono avere almeno 3 caratteri
        if (user.length < 3 || pwd.length < 3) {

            event.preventDefault(); // Blocca l'invio del form

            errorBox.classList.remove("d-none"); // Mostra il messaggio di errore

        } else {

            errorBox.classList.add("d-none"); // Nasconde l'errore se tutto è valido
        }
    });
});