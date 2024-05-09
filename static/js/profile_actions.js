function showSection(id) {
    document.getElementById(id).style.display = "block";
}

function dismissSection(id) {
    document.getElementById(id).style.display = "none";
}

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

function checkInput(input) {
    var tgid = input.value.trim();
    var errorMsg = document.getElementById("error");
    var confirm = document.getElementById("confirmTgID");
    $("#confirmIDcheck").empty();
    html_block = "";
    // Verifica se l'input contiene solo numeri e ha una lunghezza compresa tra 1 e 9
    if (/^\d{9}$/.test(tgid)) {
        errorMsg.innerHTML = "";
        html_block = '<i class="fa-solid fa-check"></i>';
        confirm.disabled = false;
    } else if (tgid == '') {
        errorMsg.innerHTML = "";
        html_block = '<i class="fa-solid fa-xmark"></i>';
        confirm.disabled = true;
    } else {
        errorMsg.innerHTML = "ID non valido: deve contenere 9 numeri";
        html_block = '<i class="fa-solid fa-xmark"></i>';
        confirm.disabled = true;
    }
    $("#confirmIDcheck").append(html_block)
}

function checkGroupInput(input) {
    var tgid = input.value.trim();
    var errorMsg = document.getElementById("error2");
    var confirm = document.getElementById("confirmTgGroupID");
    $("#confirmGroupIDcheck").empty();
    html_block = "";
    // Verifica se l'input contiene solo numeri e ha una lunghezza compresa tra 1 e 9
    if (/^\d{14}$/.test(tgid)) {
        errorMsg.innerHTML = "";
        html_block = '<i class="fa-solid fa-check"></i>';
        confirm.disabled = false;
    } else if (tgid == '') {
        errorMsg.innerHTML = "";
        html_block = '<i class="fa-solid fa-xmark"></i>';
        confirm.disabled = true;
    } else {
        errorMsg.innerHTML = "ID non valido: deve contenere 14 numeri";
        html_block = '<i class="fa-solid fa-xmark"></i>';
        confirm.disabled = true;
    }
    $("#confirmGroupIDcheck").append(html_block)
}

//check if IP is right
function checkInputIP(input) {
    var IPaddress = input.value.trim();
    var doBackup = document.getElementById("backupBtn");
    var error = document.getElementById("IPerror");

    $("#confirmIPcheck").empty();
    html_block = "";

    // Check if the input is a valid IP address
    if (/^(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$/.test(IPaddress)) {
        error.innerHTML = "";
        doBackup.disabled = false; // Enable doBackup
        html_block = '<i class="fa-solid fa-check"></i>';
    } else if (IPaddress == '') {
        error.innerHTML = "";
        doBackup.disabled = true; // Disable doBackup
        html_block = '<i class="fa-solid fa-xmark"></i>';
    } else {
        error.innerHTML = "L'indirizzo IP inserito non &egrave valido";
        doBackup.disabled = true; // Disable doBackup
        html_block = '<i class="fa-solid fa-xmark"></i>';
    }
    $("#confirmIPcheck").append(html_block)
}