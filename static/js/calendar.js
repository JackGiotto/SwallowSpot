function showPopOut(pop_out_id, show_id) {
    var pop_out = document.getElementById(pop_out_id);
    var show = document.getElementById(show_id);
    
    pop_out.style.left = "auto";
    pop_out.style.right = "0";
    show.innerHTML = "<span onclick=\"dismissPopOut('popOut', 'showPopOut')\"><i class=\"fa-solid fa-angle-right\"></i></span>";
}

function dismissPopOut(pop_out_id, show_id) {
    var pop_out = document.getElementById(pop_out_id);
    var show = document.getElementById(show_id);
    
    pop_out.style.left = "100%";
    pop_out.style.right = "auto";
    show.innerHTML = "<span onclick=\"showPopOut('popOut', 'showPopOut')\"><i class=\"fa-solid fa-angle-left\"></i></span>";
}