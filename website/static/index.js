function updateSliderValue() {
  var slider = document.getElementById("stay-days");
  var output = document.getElementById("stay-days-value");
  output.innerHTML = slider.value;
}
function getSmartForm() {
  const form = document.querySelector("#smart-form");
  form.style.display = "block";
}

//flag for the delete button for every Smart
shown = false;

//function that hides and shows the delete button on Smarts
function showDelete(){
var deleteButtons = document.getElementsByClassName('delete-smart-btn');
if(!shown){
  for (var i = 0; i < deleteButtons.length; i++){
    deleteButtons[i].setAttribute("style", ""); 
  }
  shown = true
}
else{
  for (var i = 0; i < deleteButtons.length; i++){
    deleteButtons[i].setAttribute("style", "display: none"); 
  }
  shown = false;
}
}

//Delete Smarts
function deleteSmart(){
   smart_id = event.target.getAttribute('data-smart-id');
   //for testing purposes
   //console.log(`http://127.0.0.1:5000/smartineraries/delete/?smart_id=${smart_id}`);

   //DELETE request
   axios
     .delete(`http://127.0.0.1:5000/smartineraries/delete/?smart_id=${smart_id}`)
     .then((response) => {
       // remove smartinerary card
       const card = document.querySelector(`div[card-id='${smart_id}']`);
       if (card) {
         card.parentNode.removeChild(card);
       }
     })
     .catch((error) => {
       console.error(error);
     });
}




