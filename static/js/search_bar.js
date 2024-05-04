let AUTOCOMPLETEDATA = [];

const input = document.getElementById("bar");

// Execute a function when the user releases a key on the keyboard
input.addEventListener("keyup", function(event) {
    
    // Get the value entered by the user
    let searchString = event.target.value;
    
    // Call a function to fetch autocomplete data based on the entered value
    getAutoCompleteData(searchString);
});

window.onload = function() {
    getAutoCompleteData()
}

function getAutoCompleteData() {
    $.get("/cities", function(data, status) {
        if (status === "success") {
            AUTOCOMPLETEDATA = JSON.parse(data)['cities'];
            // Call any function that depends on AUTOCOMPLETEDATA here
            autocomplete(input);
        } else {
            console.error("Failed to fetch autocomplete data");
        }
    });
}

function autocomplete(input) {
    const inputValue = input.value.toLowerCase();

    const filteredData = AUTOCOMPLETEDATA.filter(item => item.city_name.toLowerCase().startsWith(inputValue));

    updateAutocompleteList(filteredData);
}

function updateAutocompleteList(data) {
    const autocompleteList = document.getElementById('autocomplete-list');
    autocompleteList.style.display = "block";
    autocompleteList.innerHTML = '';

    data.forEach(item => {
        const listItem = document.createElement('div');
        listItem.classList.add('autocomplete-item');
        listItem.textContent = item.city_name;

        // Fill the search bar with the clicked item
        listItem.addEventListener('click', function() {
            document.getElementById('bar').value = item.city_name;
            // After clicking an item, remove the list
            autocompleteList.innerHTML = '';
        });

        autocompleteList.appendChild(listItem);
    });
}
