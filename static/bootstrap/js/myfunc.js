/**
 * Created by 01054432 on 2016/11/10.
 */


function checkstatus() {
    var tableId = document.getElementById("mytable");
    var str = "";
    for (var i = 1; i < tableId.rows.length; i++) {
        var value = tableId.rows[i].cells[6];
        if (value.innerText == "executed") {
            value.setAttribute("class", "success");

        }
        else if (value.innerText == "check passed") {
            value.setAttribute("class", "warning");

        }
        else if (value.innerText == "running") {
            value.setAttribute("class", "active");
        }
        else {
            value.setAttribute("class", "danger");
        }
    }
}