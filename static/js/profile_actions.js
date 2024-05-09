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