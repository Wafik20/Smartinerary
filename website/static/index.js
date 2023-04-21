// Function that updates the value of the stay-days slider
function updateSliderValue() {
  var slider = document.getElementById("stay-days");
  var output = document.getElementById("stay-days-value");
  output.innerHTML = slider.value;
}

// Function that displays the Smart form
function getSmartForm() {
  const form = document.querySelector("#smart-form");
  form.style.display = "block";
}

// Flag for the delete button for every Smart
var shown = false;

// Function that hides and shows the delete button on Smarts
function showDelete() {
  var deleteButtons = document.getElementsByClassName("delete-smart-btn");
  if (!shown) {
    for (var i = 0; i < deleteButtons.length; i++) {
      deleteButtons[i].setAttribute("style", "");
    }
    shown = true;
  } else {
    for (var i = 0; i < deleteButtons.length; i++) {
      deleteButtons[i].setAttribute("style", "display: none");
    }
    shown = false;
  }
}

// Function to delete Smarts
function deleteSmart() {
  // Get the ID of the Smart from the data-smart-id attribute of the clicked button
  smart_id = event.target.getAttribute("data-smart-id");
  // For testing purposes
  // console.log(`http://127.0.0.1:5000/smartineraries/delete/?smart_id=${smart_id}`);

  // Send a DELETE request to delete the Smart from the database
  axios
    .delete(`http://127.0.0.1:5000/smartineraries/delete/?smart_id=${smart_id}`)
    .then((response) => {
      // Remove the Smartinerary card from the DOM
      const card = document.querySelector(`div[card-id='${smart_id}']`);
      if (card) {
        card.parentNode.removeChild(card);
      }
    })
    .catch((error) => {
      console.error(error);
    });
}
