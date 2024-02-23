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

    var btnCommande = document.getElementById('new_commande');
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
                    btnCommande.href = "http://localhost:5000/delivery/new/?refMateriel="+data.refMateriel;

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
                btnCommande.href = "http://localhost:5000/delivery/new/?refMateriel="+data.refMateriel;

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
function imprimer(){            
    fetch(`/alertes/creer_pdf/`)
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
