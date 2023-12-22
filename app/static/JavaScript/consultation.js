function change() {
    const searchQuery = document.getElementById('searchinput').value;
    const selectedDomaine = document.getElementById('Domaine').value;
    const selectedCategorie = document.getElementById('Categorie').value;

    const optionC = document.createElement('option');
    optionC.value = "";
    optionC.textContent = "Catégorie";

    fetch(`/get_categories?domaine=${selectedDomaine}`)
        .then(response => response.json())
        .then(data => {
            dataCategories = data.categories;
            const CatList = document.getElementById('Categorie');
            CatList.innerHTML = "";
            CatList.appendChild(optionC);
            dataCategories.forEach(categorie => {
                const option = document.createElement('option');
                option.value = categorie.codeC;
                option.textContent = categorie.nomC;
                if (option.value == selectedCategorie) {
                    option.selected = true;
                }
                CatList.appendChild(option);
            });
            ListeMateriauxMAJ();
        })
        .catch(error => console.error('Erreur : ' + error));
}

function ListeMateriauxMAJ() {
    const searchQuery = document.getElementById('searchinput').value;
    const selectedDomaine = document.getElementById('Domaine').value;
    const selectedCategorie = document.getElementById('Categorie').value;
    fetch(`/consult/recherche?search=${searchQuery}&domaine=${selectedDomaine}&categorie=${selectedCategorie}`)
        .then(response => response.json())
        .then(data => {
            dataMateriels = data.materiels;
            const materielsList = document.getElementById('materielsList');
            materielsList.innerHTML = "";
            dataMateriels.forEach(material => {
                const materialItem = document.createElement('li');

                const div = document.createElement('div');
                div.classList.add('item_mat');

                const img = document.createElement('img');
                img.src = "data:image/png;base64," + material.image;
                img.alt = material.nom;
                const h2 = document.createElement('h2');
                h2.id = material.reference;
                h2.onclick = function () { editMateriauxGenerique(this.id) };
                h2.textContent = material.nom;

                div.appendChild(img);
                div.appendChild(h2);
                materialItem.appendChild(div);
                materielsList.appendChild(materialItem);
            });
        })
        .catch(error => console.error('Erreur : ' + error));
}

function editMateriauxGenerique(id) {
    var labelNom = document.getElementById("nom");
    var labelDomaine = document.getElementById("domaine");
    var labelCategorie = document.getElementById("categorie");
    var labelReference = document.getElementById("reference");
    var labelQuanT = document.getElementById("quantiteT");
    var lavelQuantiteMax = document.getElementById("quantiteMax");
    var labelComplements = document.getElementById("complements");
    var labelImage = document.getElementById("imagePresentation");
    var hiddenid = document.getElementById("hiddenref");

    fetch('/get_info_Materiel/' + id)
        .then(response => response.json())
        .then(data => {
            var reference = data.reference;
            labelNom.value = data.nom;
            labelDomaine.value = data.domaine;
            construitListeCategorie(data.domaine, data.categorie);
            labelCategorie.value = data.categorie;
            lavelQuantiteMax.value = data.quantite_max;
            labelQuanT.value = data.quantite_global;
            labelReference.value = reference;
            labelComplements.value = data.complements;
            labelImage.src = "data:image/png;base64," + data.image;
            labelImage.alt = data.nom;
            hiddenid.value = reference;
            construitMaterielInstance(data.instances, data.reference);
        })
        .catch(error => console.error('Erreur : ' + error));
}

function construitListeCategorie(domaineselect, categorieselect) {
    var selectCategorie = document.getElementById("categorie");
    selectCategorie.innerHTML = "";
    var option = document.createElement("option");
    option.value = "";
    option.textContent = "Catégorie";
    selectCategorie.appendChild(option);
    fetch(`/get_categories?domaine=${domaineselect}`)
        .then(response => response.json())
        .then(data => {
            data.categories.forEach(categorie => {
                var option = document.createElement("option");
                option.value = categorie.codeC;
                option.textContent = categorie.nomC;
                if (categorie.codeC == categorieselect) {
                    option.selected = true;
                }
                selectCategorie.appendChild(option);
            });
        })
        .catch(error => console.error('Erreur : ' + error));
}

function editMateriauxInstance(id, ref) {
    var labelQuantiteRes = document.getElementById("qteRestante");
    var labelDatePeremption = document.getElementById("datePeremption");
    var hiddenref = document.getElementById("hiddenref2");
    var hiddenMat = document.getElementById("hiddenrefMat");
    fetch('/get_info_Instance/' + id + '/' + ref)
        .then(response => response.json())
        .then(data => {
            labelQuantiteRes.value = data.quantite_restante;
            var datePeremption = new Date(data.date_peremption);
            var formattedDate = datePeremption.toISOString().split('T')[0];
            labelDatePeremption.value = formattedDate;
            hiddenref.value = data.reference;
            hiddenMat.value = ref;            
        })
        .catch(error => console.error('Erreur : ' + error));
}

function construitMaterielInstance(listeInstance , reference) {
    var ul = document.getElementById("instanceList");
    ul.innerHTML = "";
    listeInstance.forEach(instance => {
        var li = document.createElement("li");
        var div = document.createElement("div");
        div.classList.add("item_instance");

        var h2 = document.createElement("h2");
        h2.textContent = instance.nomMateriel;
        h2.id = instance.reference;
        h2.onclick = function () { editMateriauxInstance(this.id, reference) };

        var div2 = document.createElement("div");

        var p = document.createElement("p");
        p.textContent = "Quantité : " + instance.quantite_restante;
        var p2 = document.createElement("p");
        p2.textContent = "Unité : " + instance.unite;

        div2.appendChild(p);
        div2.appendChild(p2);
        div.appendChild(h2);
        div.appendChild(div2);
        li.appendChild(div);
        ul.appendChild(li);
    });
}

function toggleInputField(elementId) {
    var inputField = document.getElementById(elementId);
    if (inputField) {
        inputField.disabled = !inputField.disabled;
        inputField.style.border = inputField.disabled ? "2px solid white" : "2px solid black";
    }
}

function inputsdisabled() {
    toggleInputField("domaine");
    toggleInputField("categorie");
    toggleInputField("reference");
    toggleInputField("quantiteR");
    toggleInputField("quantiteT");
    toggleInputField("complements");
    toggleInputField("nom");
    toggleInputField("quantiteMax");
    toggleInputField("qteRestante");
    toggleInputField("datePeremption");

    var buttonValider = document.getElementById("buttonvalider");
    if (buttonValider) {
        buttonValider.disabled = !buttonValider.disabled;
    }
    var buttonvalider2 = document.getElementById("buttonvalider2");
    if (buttonvalider2) {
        buttonvalider2.disabled = !buttonvalider2.disabled;
    }
}

function suppression() {
    var hiddenid = document.getElementById("hiddenref");
    var reference = hiddenid.value;
    fetch('/consult/supprimer/' + reference)
        .then(response => response.json())
        .then(data => {
            if (data.status == "success") {
                alert("Suppression réussie");
                location.reload();
            }
            else {
                alert("Suppression échouée");
            }
        })
        .catch(error => console.error('Erreur : ' + error));
}

window.onload = function() {
    disabledOnLoad();
    var selectDomaine = document.getElementById('domaine');
    selectDomaine.addEventListener('change', majCategorieInstance);
};

function disabledOnLoad() {
    toggleInputField("domaine");
    toggleInputField("categorie");
    toggleInputField("datePeremption");
    
};

function majCategorieInstance(){
    const selectedDomaine = document.getElementById('domaine').value;
    const selectedCategorie = document.getElementById('categorie').value;
    const optionC = document.createElement('option');
    optionC.value = "";
    optionC.textContent = "Catégorie";

    fetch(`/get_categories?domaine=${selectedDomaine}`)
        .then(response => response.json())
        .then(data => {
            dataCategories = data.categories;
            const CatList = document.getElementById('categorie');
            CatList.innerHTML = "";

            CatList.appendChild(optionC);
            dataCategories.forEach(categorie => {
                const option = document.createElement('option');
                option.value = categorie.codeC;
                option.textContent = categorie.nomC;
                if (option.value == selectedCategorie) {
                    option.selected = true;
                }
                CatList.appendChild(option);
            });
        })
        .catch(error => console.error('Erreur : ' + error));
}

function imprimer(){
    ref = document.getElementById("reference").value
    fetch(`/consult/creer_pdf?ref=${ref}`)
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

function ouvreFDS(){
    var hiddenid = document.getElementById("hiddenref");
    var reference = hiddenid.value;
    var chemin = "/consult/ouvreFDS/" + reference;
    window.open(chemin, '_blank');
}