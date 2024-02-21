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
    if (document.getElementById("greenDial")) {
        emailjs.init("FLCWfGzjhSIMLmML1");
        var mailField = document.getElementById("mail_field");
        var passField = document.getElementById("pass_field");
        var tempPass = createPassword(8);
        passField.value = tempPass;
        emailjs.send("service_kvw3ho3", "template_w6zqi2j", { email: mailField.value, mdp: passField.value })
            .then(alert("Email envoyé avec succès"));
    }
}
