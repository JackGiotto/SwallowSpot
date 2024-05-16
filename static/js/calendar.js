//show calendar
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

//dismiss calendar
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

//obtain report dates
function getBulletinsDates(type) {
    return new Promise((resolve, reject) => {
        $.get("/bulletins_dates", { "type": type })
            .done(function(data, status) {
                resolve(JSON.parse(data)['dates']);
            })
            .fail(function(jqXHR, textStatus, errorThrown) {
                console.error("Error fetching bulletin dates:", errorThrown);
                reject(new Error("Failed to fetch bulletin dates"));
            });
    });
}

//create calendar with flatpickr
async function createCalendar(type){
    data = await getBulletinsDates(type);
    //dates
    let dates = data;
    //classes
    classDict = {
        0: 'event'
    };

    //split in 2 digits
    function get2DigitFmt(val) {
        return ('0' + val).slice(-2);
    }
    
    flatpickr("#dateInput", {
        dateFormat: "d-m-Y",
        altInput: true,
        altFormat: "j F Y",
        disableMobile: "true",
        onDayCreate: function(dObj, dStr, fp, dayElem){
            let date = dayElem.dateObj,
            key = date.getFullYear() + get2DigitFmt(date.getMonth() + 1) + get2DigitFmt(date.getDate()),
            value = classDict[dates[key]];
            if (value) {
                dayElem.className += ' ' + value;
            }
        }
    });
}