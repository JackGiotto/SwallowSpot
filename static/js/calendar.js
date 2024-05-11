function showPopOut(pop_out_id, show_id, calendar_id) {
    var pop_out = document.getElementById(pop_out_id);
    var show = document.getElementById(show_id);
    var calendar = document.getElementById(calendar_id);
    
    pop_out.style.left = "auto";
    pop_out.style.right = "0";
    calendar.classList.remove("calendarSlideOut");
    calendar.classList.add("calendarSlideIn");
    show.classList.remove("arrowSlideOut");
    show.classList.add("arrowSlideIn");
    show.innerHTML = "<span class=\"rotateArrowIn\" onclick=\"dismissPopOut('popOut', 'showPopOut', 'calendar-out')\"><i class=\"fa-solid fa-angle-right\"></i></span>";
}

function dismissPopOut(pop_out_id, show_id, calendar_id) {
    var pop_out = document.getElementById(pop_out_id);
    var show = document.getElementById(show_id);
    var calendar = document.getElementById(calendar_id);
    
    calendar.classList.remove("calendarSlideIn");
    calendar.classList.add("calendarSlideOut");
    show.classList.remove("arrowSlideIn");
    show.classList.add("arrowSlideOut");
    show.innerHTML = "<span class=\"rotateArrowOut\" onclick=\"showPopOut('popOut', 'showPopOut', 'calendar-out')\"><i class=\"fa-solid fa-angle-left\"></i></span>";
    setTimeout(() => {
        pop_out.style.left = "100%";
        pop_out.style.right = "auto";
    }, 990);
}