//cookies functions
function reject(){
    document.getElementById("cookies").classList.add("disappear");
}
function accept(){

}
function customize(){
    
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