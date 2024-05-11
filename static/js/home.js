var wid;

function showMore(button_id, div_id) {
    document.getElementById(button_id).style.display = "none";
    document.getElementById(div_id).style.display = " initial";
    wid = "sm";
    if (button_id == "showMoreSm") {
        document.getElementById("showMoreMd").style.display = "none";
        document.getElementById("readMoreMd").style.display = " initial";
        wid = "md";
    }
    document.getElementById("showLess").style.display = " initial";
}

function showLess() {
    if (wid == "sm") {
        document.getElementById("showMoreSm").style.display = " initial";
        document.getElementById("readMoreSm").style.display = "none";
    }
    else if (wid == "md") {
        document.getElementById("showMoreMd").style.display = " initial";
        document.getElementById("readMoreMd").style.display = "none";
    }
    document.getElementById("showLess").style.display = "none";
}