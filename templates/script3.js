document.addEventListener("DOMContentLoaded", function() {
    const itemInput = document.getElementById("item");
    const itemList = document.getElementById("item-list");
    const addItemButton = document.getElementById("add-item");
    const referenceField = document.getElementById("reference-field");
    const bookingForm = document.getElementById("booking-form");

    
    // Function to handle adding items to the reference field
    function addItemToReference(item, quantity) {
        const li = document.createElement("li");
        li.textContent = `${item} - Quantity: ${quantity}`;
        referenceField.appendChild(li);
    }


    // Populate item list for autocomplete
    mockItemList.forEach(item => {
        const option = document.createElement("option");
        option.value = item;
        itemList.appendChild(option);
    });

    // Function to handle adding items to the reference field
    function addItemToReference(item, quantity) {
        const li = document.createElement("li");
        li.textContent = `${item} - Quantity: ${quantity}`;
        referenceField.appendChild(li);
    }

    // Event listener for Add Item button
    addItemButton.addEventListener("click", function() {
        const item = itemInput.value.trim();
        const quantity = document.getElementById("quantity").value.trim();

        if (item && quantity) {
            addItemToReference(item, quantity);
            itemInput.value = "";
            document.getElementById("quantity").value = "";
        } else {
            alert("Please enter both item name and quantity.");
        }
    });

   
        // Function to submit form data using AJAX
function submitForm(formData) {
    // Replace 'YOUR_BACKEND_ENDPOINT' with the actual backend endpoint
    const url = '/submit';
    const xhr = new XMLHttpRequest();
    xhr.open('POST', url, true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.onreadystatechange = function() {
        if (xhr.readyState === 4) {
            if (xhr.status === 200) {
                console.log('Form submitted successfully!');
                // You can add any success message or redirection logic here
                bookingForm.reset(); // Reset form fields
                referenceField.innerHTML = ""; // Clear reference field
            } else {
                console.error('Form submission failed:', xhr.status);
                // You can add error handling logic here
            }
        }
    };
    xhr.send(JSON.stringify(formData));

}
        // Event listener for form submission
bookingForm.addEventListener("submit", function(event) {
    event.preventDefault();

    const formData = new FormData(bookingForm);
    const data = {};
    formData.forEach((value, key) => {
        data[key] = value;
    });

    // Call the submitForm function with form data
    submitForm(data);
});

        // Reset form fields
        bookingForm.reset();
        referenceField.innerHTML = ""; // Clear reference field
    });

    // Event listener for item input to update autocomplete suggestions
    itemInput.addEventListener("input", function() {
        const input = itemInput.value.trim().toLowerCase();
        const filteredItems = mockItemList.filter(item => item.toLowerCase().includes(input));
        itemList.innerHTML = "";
        filteredItems.forEach(item => {
            const option = document.createElement("option");
            option.value = item;
            itemList.appendChild(option);
        });
    });

