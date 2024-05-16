var wid;

//show more description
function showMore(button_id, div_id) {
    document.getElementById(button_id).style.display = "none";
    document.getElementById(div_id).style.display = " initial";
    wid = "md";
    if (button_id == "showMoreSm") { //if device is phone
        document.getElementById("showMoreMd").style.display = "none";
        document.getElementById("readMoreMd").style.display = " initial";
        wid = "sm";
    }
    document.getElementById("showLess").style.display = " initial";
}

//show less description
function showLess() {
    if (wid == "sm") { //if device id phone
        document.getElementById("showMoreSm").style.display = " initial";
        document.getElementById("readMoreSm").style.display = "none";
    }
    else if (wid == "md") { //if device is tablet
        document.getElementById("showMoreMd").style.display = " initial";
        document.getElementById("readMoreMd").style.display = "none";
    }
    document.getElementById("showLess").style.display = "none";
}