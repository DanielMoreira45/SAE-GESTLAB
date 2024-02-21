document.addEventListener("DOMContentLoaded", function() {
    document.getElementById('recherche').addEventListener('input', update_categorie);
    document.getElementById('domaine-select').addEventListener('change', update_categorie);
    document.getElementById('categorie-select').addEventListener('change', update_categorie);
    document.getElementById('statut-select').addEventListener('change', update_categorie);
    document.getElementById('btn-reset').addEventListener('click', reset);
    document.querySelectorAll('.command_button').forEach(button => {
        button.addEventListener('click', function(){
            edit(button.id);
        });
    });
    if (document.getElementById("valider")){
        document.getElementById("valider").addEventListener('click', function(){
            validate(true);
        });
    }
    if (document.getElementById("annuler")){
        document.getElementById("annuler").addEventListener('click', function(){
            validate(false);
        });
    }
    if (document.querySelector(".command_button")) {
        edit(document.querySelector(".command_button").id);
    }
    update_categorie();
    
});

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
                if (document.getElementById("valider") && document.getElementById("annuler")){
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

function edit_notif(idA, numM, type_alerte) {
    var labelTitre = document.getElementById("label-titre");

    var labelCommentaire = document.getElementById("label-commentaire");
    var labelNom = document.getElementById("label-nom");

    var labelQteMax = document.getElementById("label-qtemax");
    var labelSeuilQte = document.getElementById("label-seuilqte");
    var labelQteMateriel = document.getElementById("label-qtemateriel");

    var labelQteRes = document.getElementById("label-qteres");
    var labelDateP = document.getElementById("label-datep");
    var labelSeuilP = document.getElementById("label-seuilp");

    var div = document.getElementById('myDiv');

    var btn = document.getElementById('new_commande');
    // var url = "{{ url_for('new_commande', refMateriel=" + numM + ") }}";
    // var url = "{{ url_for('new_commande') }}" + "?refMateriel=" + numM;
    // btn.href += "?refMateriel=" + numM;

    div.innerHTML = '';

    labelTitre.textContent = "";
    labelCommentaire.textContent = "";
    labelNom.textContent = "";
    labelQteMax.textContent = "";
    labelSeuilQte.textContent = "";
    labelQteMateriel.textContent = "";
    labelQteRes.textContent = "";
    labelDateP.textContent = "";
    labelSeuilP.textContent = "";

    switch(type_alerte){

        case 'quantite':
            labelQteMax.style.display = 'block';
            labelSeuilQte.style.display = 'block';
            labelQteMateriel.style.display = 'block';
                    
            labelTitre.textContent = "Alerte de Quantité";
            fetch(`/alertes/qte/get_info/?ida=${idA}&numm=${numM}`)
                .then(response => response.json())
                .then(data => {
                    btn.href = "http://localhost:5000/delivery/new/?refMateriel="+data.refMateriel;

                    labelCommentaire.textContent = "Commentaire : "+data.commentaire;
                    labelNom.textContent = "Nom de matériel : "+data.nom;
                    labelQteMax.textContent = "Quantité max : "+data.qteMax;
                    labelSeuilQte.textContent = "Seuil de Quantité : "+data.seuil;
                    labelQteMateriel.textContent = "Quantité materiel : "+data.qteMateriel;
                    if(data.unite){
                        labelQteMax.textContent += ' '+data.unite;
                        labelSeuilQte.textContent += ' '+data.unite;
                        labelQteMateriel.textContent += ' '+data.unite;
                    }
                    var qteMateriel = {
                        x: [data.nom],
                        y: [data.qteMateriel],
                        name: 'quantité restante',
                        type: 'bar',
                        marker: {
                        color: 'rgba(255,0,0,0.4)'
                        },
                        hoverinfo: 'none'
                    };
                            
                    var seuil = {
                        x: [data.nom],
                        y: [data.seuil - data.qteMateriel],
                        name: 'minimum',
                        type: 'bar',
                        marker: {
                            color: 'rgba(0,255,0,0.4)'
                        },
                        hoverinfo: 'none'
                    };
                    
                    var max = {
                        x: [data.nom],
                        y: [data.qteMax - data.seuil],
                        name: 'maximum',
                        type: 'bar',
                        marker: {
                            color: 'rgba(0,0,0,0.1)'
                        },
                        hoverinfo: 'none'
                    };
                    var data = [qteMateriel, seuil, max];
                    var layout = {barmode: 'relative', hover: 'None'}
                    Plotly.newPlot('myDiv', data, layout);                
                })
                .catch(error => console.error('Erreur : ' + error));
            break;
    
    case 'seuil':
        labelQteMax.style.display = 'none';
        labelSeuilQte.style.display = 'none';
        labelQteMateriel.style.display = 'none';

        labelTitre.textContent = "Alerte de Péremption";
        fetch(`/alertes/seuil/get_info/?ida=${idA}&numm=${numM}`)
            .then(response => response.json())
            .then(data => {
                btn.href = "http://localhost:5000/delivery/new/?refMateriel="+data.refMateriel;

                labelNom.textContent = "Nom de matériel : "+data.nom;
                labelCommentaire.textContent = "Commentaire : "+data.commentaire;
                labelQteRes.textContent = "Quantité restante : "+data.qteRestante;              
                labelDateP.textContent = "Date de péremption : "+data.datePeremption;
                labelSeuilP.textContent = "Seuil de péremption : "+data.seuilPeremption + ' jours';
            })
            .catch(error => console.error('Erreur : ' + error));
        break;
    }
}