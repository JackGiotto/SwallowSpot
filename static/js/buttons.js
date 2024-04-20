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

//cookies functions
function reject(){
    document.getElementById("cookies").classList.add("disappear");
}
function accept(){
    //genera data scadenza cookies persistents (30 giorni)
    var expireDate = new Date();
    expireDate.setDate(expireDate.getDate() + 30);

    document.cookie = "IDSESSION = "+uniqid()//cookie di sessione (expires)
    document.cookie = "IDSPOTLIGHT= "+uniqid()+"expires=" + expireDate.toUTCString();//cookie tecnici (SPOTLIGHT: Swallowspot Planning and Operational Tool for High-efficiency)
    document.cookie = "IDSWOT="+uniqid()+"expires=" + expireDate.toUTCString();//cookie personali(SWOT: Swallowspot Work Organizational Tool)

}
function customize(){
    //ricevere scelete dell'utente e creare i rispettivi cookie
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