function showtime() {
    var tiempo = document.getElementById("timeSelec");

    var element = document.getElementById("time");
    var check = document.getElementById("cboxTime");
    if (check.checked) {
        element.style.display = "block";
        tiempo.setAttribute("value", "00:00");
    } else {
        element.style.display = "none";
        tiempo.setAttribute("value", "");
    }
}

console.log("zsdfsa");
