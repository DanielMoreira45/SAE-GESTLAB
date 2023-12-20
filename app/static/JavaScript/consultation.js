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
                option.textContent = categorie.nom;
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
    // Envoyer une requête Ajax pour mettre à jour la liste de matériaux
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
                h2.onclick = function () { edit(this.id) };
                h2.textContent = material.nom;

                div.appendChild(img);
                div.appendChild(h2);
                materialItem.appendChild(div);
                materielsList.appendChild(materialItem);
            });
        })
        .catch(error => console.error('Erreur : ' + error));
}

function edit(id) {
    var labelNom = document.getElementById("nom");
    var labelDomaine = document.getElementById("domaine");
    var labelCategorie = document.getElementById("categorie");
    var labelReference = document.getElementById("reference");
    var labelQuanR = document.getElementById("quantiteR");
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
            labelCategorie.value = data.categorie;
            lavelQuantiteMax.value = data.quantite_max;
            labelQuanT.value = data.quantite_global;
            labelReference.value = reference;
            labelComplements.value = data.complements;
            labelImage.src = "data:image/png;base64," + data.image;
            labelImage.alt = data.nom;
            hiddenid.value = reference;

        })
        .catch(error => console.error('Erreur : ' + error));

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

    var buttonValider = document.getElementById("buttonvalider");
    if (buttonValider) {
        buttonValider.disabled = !buttonValider.disabled;
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
};

function majCategorieInstance(){
    const selectedDomaine = document.getElementById('domaine').value;
    const selectedCategorie = document.getElementById('categorie').value;
    const optionC = document.createElement('option');
    optionC.value = "";
    optionC.textContent = "Catégorie";
    console.log(selectedDomaine);

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
                option.textContent = categorie.nom;
                if (option.value == selectedCategorie) {
                    option.selected = true;
                }
                CatList.appendChild(option);
            });
        })
        .catch(error => console.error('Erreur : ' + error));
}