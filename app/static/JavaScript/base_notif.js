window.onload = function() {
    majNotifs();    
}

function majNotifs() {
    fetch('/notif/maj')
        .then(response => response.json())
        .then(data => {
            if (data.qte > 0){
                alert("Ajouts de " +data.qte+ " notifications");
            }
        })
        .catch(error => console.error('Erreur : ' + error));
}
