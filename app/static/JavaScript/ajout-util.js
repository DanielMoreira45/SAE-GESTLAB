function createPassword(nbCaractere, chaine="azertyuiopqsdfghjklmwxcvbn123456789"){
    var nbLettres = chaine.length + 1;
    var passwd = "";
    for (var i=0; i<nbCaractere; i++){
        var positionLettre = Math.round(Math.random()*nbLettres);
        var lettre = chaine[positionLettre];
        passwd += lettre;
    }
    return passwd;
}

function sendEmail(){
    emailjs.init("FLCWfGzjhSIMLmML1");
    var emailUti = document.getElementById("emailUti");
    emailjs.send("service_kvw3ho3", "template_5okli8n", {email: emailUti.value, mdp: createPassword(8)})
    .then(alert("Email envoyé avec succès"));
}
