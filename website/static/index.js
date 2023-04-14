function updateSliderValue() {
  var slider = document.getElementById("stay-days");
  var output = document.getElementById("stay-days-value");
  output.innerHTML = slider.value;
}
function getSmartForm() {
  const form = document.querySelector("#smart-form");
  form.style.display = "block";
}
function createSmart() {
  const name = document.getElementById("name").value;
  const description = document.getElementById("description").value;
  const city_id = document.getElementById("city").value;
  var lenOfStay = document.getElementById("stay-days").value;
  const data = { name, description, city_id, lenOfStay };
  axios
    .post("/smartineraries", data)
    .then((response) => {
      // Redirect to the Smartinierary detail page
      const itineraryData = response.data;
      const smart_id = response.data.smart_id;
      itineraryData["lenOfStay"] = lenOfStay;
      axios
        .post("/admin/itinerary", itineraryData)
        .then((response) => {
          window.location.href = `/smartineraries?smart_id=${smart_id}`;
        })
        .catch((error) => {
          console.error(error);
        });
    })
    .catch((error) => {
      console.error(error);
    });
}
