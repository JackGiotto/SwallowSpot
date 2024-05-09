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
function checkInputs() {
    var tgid = document.getElementById("ChatID").value.trim();
    var gtgid = document.getElementById("GroupID").value.trim();
    var errorMsg1 = document.getElementById("error");
    var errorMsg2 = document.getElementById("error2");
    var confirmButton = document.getElementById("confirmButton");

    // Verifica se l'input ChatID è valido
    var validChatID = /^\d{9}$/.test(tgid);
    if (validChatID) {
        errorMsg1.innerHTML = "";
        html_block = '<i class="fa-solid fa-check"></i>';
    } else {
        errorMsg1.innerHTML = "ID non valido: deve contenere 9 numeri";
    }

    // Verifica se l'input GroupID è valido
    var validGroupID = /^\d{13}$/.test(gtgid);
    if (validGroupID) {
        errorMsg2.innerHTML = "";
        html_block = '<i class="fa-solid fa-check"></i>';
    } else {
        errorMsg2.innerHTML = "ID non valido: deve contenere 14 numeri";
    }

    // Abilita il pulsante di conferma solo se entrambi gli input sono validi
    confirmButton.disabled = !(validChatID && validGroupID);
}
