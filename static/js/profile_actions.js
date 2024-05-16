//show section to change credentials
function showSection(id) 
{
    document.getElementById(id).style.display = "block";
}

//dismiss section
function dismissSection(id) 
{
    document.getElementById(id).style.display = "none";
}

//logout
function logout() { 
    $.post("/profile/logout/", 
    {
    },
    function(data, status) {
        if (status == "success") {
            window.location = "/";
        }
    }
    )
}

//on admin page

var input1 = false, input2 = false;

//user id
function checkInput(input) {
    var tgid = input.value.trim();
    var errorMsg = document.getElementById("error");
    var confirm = document.getElementById("confirmButton");
    $("#confirmIDcheck").empty();
    html_block = "";
    // Checks whether the input contains only numbers and has a length of 9
    if (/^\d{9}$/.test(tgid)) { //success
        errorMsg.innerHTML = "";
        html_block = '<i class="fa-solid fa-check"></i>';
        if (input2 == true) {
            confirm.disabled = false;
        }
        input1 = true;
    } else if (tgid == '') { // if input is empty
        errorMsg.innerHTML = "";
        html_block = '<i class="fa-solid fa-xmark"></i>';
        confirm.disabled = true;
        input1 = false;
    } else { // error
        errorMsg.innerHTML = "ID non valido: deve contenere 9 numeri";
        html_block = '<i class="fa-solid fa-xmark"></i>';
        confirm.disabled = true;
        input1 = false;
    }
    $("#confirmIDcheck").append(html_block)
}

//group id
function checkGroupInput(input) {
    var tgid = input.value.trim();
    var errorMsg = document.getElementById("error2");
    var confirm = document.getElementById("confirmButton");
    $("#confirmGroupIDcheck").empty();
    html_block = "";
    // Checks whether the input contains only numbers and has a length of 13
    if (/^\d{13}$/.test(tgid)) { //success
        errorMsg.innerHTML = "";
        html_block = '<i class="fa-solid fa-check"></i>';
        if (input1 == true) {
            confirm.disabled = false;
        }
        input2 = true;
    } else if (tgid == '') { // if input is empty
        errorMsg.innerHTML = "";
        html_block = '<i class="fa-solid fa-xmark"></i>';
        confirm.disabled = true;
        input2 = false;
    } else { // error
        errorMsg.innerHTML = "ID non valido: deve contenere 13 numeri";
        html_block = '<i class="fa-solid fa-xmark"></i>';
        confirm.disabled = true;
        input2 = false;
    }
    $("#confirmGroupIDcheck").append(html_block)
}

//check if IP is right

var ipCheck = false, portCheck = false;

function checkInputIP(input) {
    var IPaddress = input.value.trim();
    var doBackup = document.getElementById("backupBtn");
    var error = document.getElementById("IPerror");

    $("#confirmIPcheck").empty();
    html_block = "";

    //success
    if (/^(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$/.test(IPaddress)) {
        error.innerHTML = "";
        ipCheck = true;
        html_block = '<i class="fa-solid fa-xmark"></i>';
        if (portCheck == true) {
            doBackup.disabled = false; // Enable doBackup
            html_block = '<i class="fa-solid fa-check"></i>';
        }
    } else if (IPaddress == '') { // if input is empty
        error.innerHTML = "";
        doBackup.disabled = true; // Disable doBackup
        html_block = '<i class="fa-solid fa-xmark"></i>';
        ipCheck = false;
    } else { // error
        error.innerHTML = "L'indirizzo IP inserito non &egrave valido";
        doBackup.disabled = true; // Disable doBackup
        html_block = '<i class="fa-solid fa-xmark"></i>';
        ipCheck = false;
    }
    $("#confirmIPcheck").append(html_block)
}

//check if port is right
function checkInputPort(input) {
    var port = input.value.trim();
    var doBackup = document.getElementById("backupBtn");
    var error = document.getElementById("IPerror");

    $("#confirmIPcheck").empty();
    html_block = "";

    // Check if the input is a valid IP address
    if (/^\d+$/.test(port)) { // success
        error.innerHTML = "";
        portCheck = true;
        html_block = '<i class="fa-solid fa-xmark"></i>';
        if (ipCheck == true) {
            doBackup.disabled = false; // Enable doBackup
            html_block = '<i class="fa-solid fa-check"></i>';
        }
    } else if (port == "") { // if input is empty
        error.innerHTML = "";
        doBackup.disabled = true; // Disable doBackup
        html_block = '<i class="fa-solid fa-xmark"></i>';
        portCheck = false;
    } else { // error
        error.innerHTML = "La porta inserita non &egrave valida";
        doBackup.disabled = true; // Disable doBackup
        html_block = '<i class="fa-solid fa-xmark"></i>';
        portCheck = false;
    }
    $("#confirmIPcheck").append(html_block)
}