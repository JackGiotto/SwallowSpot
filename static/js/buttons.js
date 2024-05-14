//variables
const cookies=["no","no","no"];

//genera data scadenza cookies persistents (30 giorni)
var expireDate = new Date();
expireDate.setDate(expireDate.getDate() + 30);

//cookies functions's choices
function reject(){
    disappear();
}
function accept(){

    create_session_cookie();
    create_personal_cookie();
    disappear();
}
function customize(){
    if(cookies[0] == "yes"){
        create_session_cookie();
    }
    if(cookies[1] == "yes"){
        create_personal_cookie();
    }   
    disappear(); 
}

//activate cookie for custom choices
function activate_session_cookie(){
    var checkbox = document.getElementById("checkbox0");
    if(checkbox.checked){
        cookies[0]="yes";
        console.log("IDSESSION agreed");
    }else{
        cookies[0]="no";
        console.log("IDSESSION denied");
    }
}
function activate_personal_cookie(){
    var checkbox = document.getElementById("checkbox2");
    if(checkbox.checked){
        cookies[2]="yes";
        console.log("SWOT agreed");
    }else{
        cookies[2]="no";
        console.log("SWOT denied");
    }
}

//funtions that creates cookies
function create_session_cookie(){
    document.cookie = "IDSESSION = null; path=/"//cookie di sessione (expires)
}
function create_personal_cookie(){
    document.cookie = "SWOT = null;expires=" + expireDate.toUTCString()+"; path=/";//cookie personali(SWOT: Swallowspot Work Organizational Tool)
}

//cookies functions
function disappear(){
    cookies1 = document.getElementById("cookies");
    cookies2 = document.getElementById("customizeCookies");
    cookies1.classList.add("disappear");
    setTimeout(() => { cookies1.remove(); cookies2.remove(); }, 1000);
}