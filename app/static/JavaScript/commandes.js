function edit(id) {
    var labelNom = document.getElementById("nom");
    var labelNumero = document.getElementById("label-numero")
    var labelDomaine = document.getElementById("label-domaine");
    var labelCategorie = document.getElementById("label-categorie");
    var labelStatut = document.getElementById("label-statut");
    var labelQuantite = document.getElementById("quantite");
    var labelUser = document.getElementById("user");
    if (id == 0){
        labelNom.textContent = "";
        labelNumero.textContent = "";
        labelDomaine.textContent = "";
        labelCategorie.textContent = "";
        labelStatut.textContent = "";
        labelQuantite.textContent = "";
        labelUser.textContent = "";
    }
    else {
        fetch(`/commandes/get_command_info/?id=${id}`)
            .then(response => response.json())
            .then(data => {
                labelNom.textContent = data.nom;
                labelNumero.textContent = "Numéro de commande : "+id
                labelDomaine.textContent = "Domaine : "+data.domaine;
                labelCategorie.textContent = "Catégorie : "+data.categorie;  
                labelStatut.textContent = "Statut : "+data.statut;   
                if (data.unite == null){
                    labelQuantite.textContent = "Quantité commandée : "+data.quantite
                } else {labelQuantite.textContent = "Quantité commandée : "+data.quantite+" "+data.unite;}
                labelUser.textContent = "Commande effectuée par "+data.user;
                
                if (data.statut == "A valider"){
                    document.getElementById("valider").value = "Valider la commande";
                    document.getElementById("annuler").disabled = false;
                    document.getElementById("valider").disabled = false;
                }
                else if (data.statut == "En cours"){
                    document.getElementById("valider").value = "Commande livrée";
                    document.getElementById("valider").disabled = false;
                    document.getElementById("annuler").disabled = true;
                }
                else{
                    document.getElementById("annuler").disabled = true;
                    document.getElementById("valider").disabled = true;
                }
            })
            .catch(error => console.error('Erreur : ' + error));  
    }
}

function search(){
    recherche = document.getElementById("recherche").value;
    domaine = document.getElementById("domaine-select").value;
    categorie_selected = document.getElementById("categorie-select").value;
    statut = document.getElementById("statut-select").value;
    fetch(`/commandes/search/?recherche=${recherche}&domaine=${domaine}&categorie=${categorie_selected}&statut=${statut}`)
        .then(response => response.json())
        .then(data => {  
            var liste_commandes_search = data.liste_commandes;
            var ul = document.getElementById("liste");
            ul.innerHTML = "";
            if (liste_commandes_search.length > 0){
                
                liste_commandes_search.forEach(function(commande) {
                    var li = document.createElement("li");
                    var button = document.createElement("button");
                    button.id = commande.numero;
                    button.className = "command_button";
                    button.addEventListener("click", function(){
                        edit(commande.numero)
                    });
                    var p = document.createElement("p");
                    p.textContent = commande.nom;
                    var image = document.createElement("img");
                    image.src = "data:image/png;base64," + commande.image;
                    image.alt = "image commande";
                    image.className = "img";
                    button.appendChild(image);
                    button.appendChild(p);
                    li.appendChild(button);
                    ul.appendChild(li);
                    edit(liste_commandes_search[0].numero);
                });
                
            }
            else{
                var li = document.createElement("li");
                var p = document.createElement("p");
                p.textContent = "Aucunes commandes trouvées pour cette recherche.";
                li.appendChild(p);
                ul.appendChild(li);
                edit(0);
            }
            
        })
}

function update_categorie(){
    recherche = document.getElementById("recherche").value
    domaine = document.getElementById("domaine-select").value
    categorie_selected = document.getElementById("categorie-select").value
    statut = document.getElementById("statut-select").value
    fetch(`/commandes/search/?recherche=${recherche}&domaine=${domaine}&categorie=${categorie_selected}&statut=${statut}`)
        .then(response => response.json())
        .then(data => {  
            document.getElementById("categorie-select").innerHTML = '<option id="categorie" value="">-- Categorie --</option>';
            data.liste_categories.forEach(function(categorie){
                var option = document.createElement("option");
                option.value = categorie.codeC;
                option.textContent = categorie.nomC;
                if (option.value == categorie_selected){
                    option.selected = true;
                }
                document.getElementById("categorie-select").appendChild(option);
            });
            search()


        })
        .catch(error => console.error('Erreur : ' + error));     
}

function imprimer(){            
    recherche = document.getElementById("recherche").value
    domaine = document.getElementById("domaine-select").value
    categorie_selected = document.getElementById("categorie-select").value
    statut = document.getElementById("statut-select").value
    fetch(`/commandes/creer_pdf?search=${recherche}&domaine=${domaine}&categorie=${categorie_selected}&statut=${statut}`)
        .then(response => response.json())
        .then(data => {
            if (!this.printedIframe) {
                this.printedIframe = document.createElement('iframe');
                document.body.appendChild(this.printedIframe);
                this.printedIframe.style.display = 'none';
                this.printedIframe.onload = function() {
                setTimeout(function() {
                    this.printedIframe.focus();
                    this.printedIframe.contentWindow.print();
                }, 100);
                };
            }
            this.printedIframe.src = `/imprimer_pdf/?chemin=${data.nom_fichier}`;                   
            
        })
        .catch(error => console.error('Erreur : ' + error));
}

function validate(validee){
    var id = document.getElementById("label-numero").textContent;
    fetch(`/commandes/validate/?validee=${validee}&id=${id}`)
    .then(response => response.json())
    .then(data => {
        update_categorie();
        edit(id);
    })
    .catch(error => console.errot('Erreur : ' + error))
}

function reset(){
    document.getElementById("recherche").value = "";
    document.getElementById("domaine").selected = true;
    document.getElementById("categorie").selected = true;
    document.getElementById("statut").selected = true;
    update_categorie();
}