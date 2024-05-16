let AUTOCOMPLETEDATA = [];

window.onload = function() {
    getAutoCompleteData()
}

// obtain citys
function getAutoCompleteData() {
    $.get("/cities", function(data, status) {
        if (status === "success") {
            AUTOCOMPLETEDATA = JSON.parse(data)['cities'];
        } else {
            console.error("Failed to fetch autocomplete data");
        }
    });
}

function autocompleteBar() {
    //console.log("ciao");
    const input_value = $('#bar').val().toLowerCase();

    //console.log(input_value);
    const filteredData = AUTOCOMPLETEDATA.filter(item => item['city_name'].toLowerCase().startsWith(input_value));

    updateAutocompleteList(filteredData);
}

// update items
function updateAutocompleteList(data) {
    const autocompleteList = document.getElementById('autocomplete-list');
    autocompleteList.style.display = "block";
    autocompleteList.innerHTML = '';

    data.forEach(item => {
        autocompleteList.style.display = "block";
        const listItem = document.createElement('div');
        listItem.classList.add('autocomplete-item');
        listItem.textContent = item.city_name;

        // Fill the search bar with the clicked item
        listItem.addEventListener('click', function() {
            document.getElementById('bar').value = item.city_name;
            // After clicking an item, remove the list
            autocompleteList.innerHTML = '';
            autocompleteList.style.display = "none";
        });

        //if the search bar is empty, the autocomplete list is not shown
        if (document.getElementById('bar').value == '') {
            autocompleteList.style.display = "none";
        }

        autocompleteList.appendChild(listItem);
    });
}
