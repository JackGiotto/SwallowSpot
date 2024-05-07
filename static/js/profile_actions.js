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