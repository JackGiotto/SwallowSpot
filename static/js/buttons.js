//variables
const cookies=["no","no","no"];

function getRandomInt(min, max) {
  min = Math.ceil(min);
  max = Math.floor(max);
  return Math.floor(Math.random() * (max - min)) + min;
}

function uniqid() {
  var id = getRandomInt(0, Date.now());
  return id;
}

function getElement(){
    alert("cookies:"+ document.cookie)
    //alert(DOCUMENT.cookie)
}

document.addEventListener('DOMContentLoaded', function() {
  document.querySelector('#output').innerHTML = uniqid();
});

//cookies functions's choices
function reject(){
    //document.getElementById("cookies").classList.add("disappear");
}
function accept(){
    //genera data scadenza cookies persistents (30 giorni)
    var expireDate = new Date();
    expireDate.setDate(expireDate.getDate() + 30);

    create_session_cookie();
    create_technical_cookie();
    create_personal_cookie();
    document.getElementById("cookies").classList.add("disappear");
}
function customize(){
    if(cookies[0] == "yes")
        create_session_cookie();
    else if(cookies[1] == "yes")
        create_technical_cookie();
    else if(cookies[2] == "yes")
        create_personal_cookie();
    document.getElementById("cookies").classList.add("disappear");
}

//activate cookie for custom choices
function activate_session_cookie(){
    var checkbox = document.getElementsByName("checkbox0")
    if(checkbox.checked){
        cookies[0]="yes"
        console.log("IDSESSION agreed")
    }else{
        cookies[0]="no"
        console.log("IDSESSION denied")
    }
}
function activate_technical_cookie(){
    var checkbox = document.getElementsByName("checkbox1")
    if(checkbox.checked){
        cookies[1]="yes"
        console.log("IDSPOTLIGHT agreed")
    }else{
        cookies[1]="no"
        console.log("IDSPOTLIGHT denied")
    }
}
function activate_personal_cookie(){
    var checkbox = document.getElementsByName("checkbox2")
    if(checkbox.checked){
        cookies[2]="yes"
        console.log("SWOT agreed")
    }else{
        cookies[2]="no"
        console.log("SWOT denied")
    }
}

//funtions that creates cookies
function create_session_cookie(){
    document.cookie = "IDSESSION = "+uniqid()//cookie di sessione (expires)
}
function create_technical_cookie(){
    document.cookie = "IDSPOTLIGHT= "+uniqid()+";expires=" + expireDate.toUTCString();//cookie tecnici (SPOTLIGHT: Swallowspot Planning and Operational Tool for High-efficiency)
}
function create_personal_cookie(){
    document.cookie = "IDSWOT="+uniqid()+";expires=" + expireDate.toUTCString();//cookie personali(SWOT: Swallowspot Work Organizational Tool)
}

//disappearing navbar function
var prevScrollpos = window.pageYOffset;
window.onscroll = function() {
    var currentScrollPos = window.pageYOffset;
    if (prevScrollpos > currentScrollPos) {
        document.getElementById("menu").style.top = "0";
    } else {
        document.getElementById("menu").style.top = "-100px";
    }
    prevScrollpos = currentScrollPos;
}