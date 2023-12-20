var ButtonBack = document.getElementById("BackButton");
var ButtonLogout = document.getElementById("logoutButton");
if (ButtonBack) {
    ButtonBack.addEventListener("click", function () {
        window.location.href = "{{ url_for('home') }}";
    });
}
if (ButtonLogout) {
    ButtonLogout.addEventListener("click", function () {
        window.location.href = "{{ url_for('logout') }}";
    });
}