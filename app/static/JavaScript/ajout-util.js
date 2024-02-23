function createPassword(nbCaractere, chaine = "abcdefghijklmnopqrstuvwxyz123456789") {
    var nbLettres = chaine.length + 1;
    var passwd = "";
    for (var i = 0; i < nbCaractere; i++) {
        var positionLettre = Math.round(Math.random() * nbLettres);
        var lettre = chaine[positionLettre];
        passwd += lettre;
    }
    return passwd;
}

function sendEmail() {
    emailjs.init("FLCWfGzjhSIMLmML1");
    var emailUti = document.getElementById("emailUti");
    var champMdp = document.getElementById("mdp");
    var mdpTemp = createPassword(8);
    champMdp.value = mdpTemp;
    emailjs.send("service_kvw3ho3", "template_5okli8n", { email: emailUti.value, mdp: champMdp.value })
        .then(alert("Email envoyé avec succès"));
}
