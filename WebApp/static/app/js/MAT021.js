function showtime() {
    var element = document.getElementById("time");
    var check = document.getElementById("cboxTime");
    if (check.checked) {
        element.style.display = "block";
    } else {
        element.style.display = "none";
    }
}