function edit(id) {
    var inputId = document.getElementById("id");
    var inputNom = document.getElementById("nom");
    var inputPrenom = document.getElementById("prenom");
    var inputPassword = document.getElementById("password");
    var roleSelect = document.getElementById("id_role");
    var droitModif = document.getElementsByName("modifications");
    var email = document.getElementById("email");

    fetch('/get_user_info/' + id)
        .then(response => response.json())
        .then(data => {
            inputId.value = data.id;
            email.value = data.email;
            inputNom.value = data.nom;
            inputPrenom.value = data.prenom;
            inputPassword.value = data.password;
            roleSelect.innerHTML = '';
            for (const role of ["Administrateur", "Professeur", "Etablissement"]) {
                var option = document.createElement("option");
                option.value = role;
                option.text = role;
                if (role === data.role_name) {
                    option.selected = true;
                }
                roleSelect.appendChild(option);
            }
            if (data.modifications === true) {
                var droit = document.getElementById("yes_choice");
                droit.checked = true;
            } else {
                var droit = document.getElementById("no_choice");
                droit.checked = true;
            }
        })
        .catch(error => console.error('Erreur : ' + error));
}

function sendEmail() {
    emailjs.init("FLCWfGzjhSIMLmML1");
    var nomUti = document.getElementById("nom");
    var prenomUti = document.getElementById("prenom");
    var mdpUti = document.getElementById("password");
    var emailUti = document.getElementById("email");
    emailjs.send("service_kvw3ho3", "template_w6zqi2j", { name: prenomUti.value, surname: nomUti.value, mdp: mdpUti.value, email: emailUti.value })
        .then(alert("Email envoyé avec succès"));
}
