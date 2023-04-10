

function test() {
  console.log("I am working");
}
function openPopup() {
  var popup = window.open("", "myPopup", "width=400,height=400");
  popup.document.write("<h1>Hello, world!</h1>");
}

function createCitiesTable() {
  axios.get('http://127.0.0.1:5000/admin/city')
    .then(response => {
      const tableBody = document.querySelector('#myTable tbody');
      response.data.forEach(city => {
        const row = document.createElement('tr');
        row.innerHTML = `
          <td>${city.name}</td>
          <td>${city.state}</td>
        `;
        tableBody.appendChild(row);
      });
    })
    .catch(error => {
      console.error(error);
    });
}

function updateCitiesTable() {
  event.preventDefault();

  const name = document.getElementById("name").value;
  const state = document.getElementById("state").value;

  console.log({
    name: name,
    state: state
  });

  axios.post("http://127.0.0.1:5000/admin/city", {
    name: name,
    state: state
  })
  .then(response => {

    addRowToTable(name, state);
  })
  .catch(error => {
    console.error(error);
  });
}


function addRowToTable(name, state) {
  var table = document.getElementById("myTable");
  var row = table.insertRow(-1);
  var nameCell = row.insertCell(0);
  var stateCell = row.insertCell(1);
  nameCell.innerHTML = name;
  stateCell.innerHTML = state;
}

function deleteCity(cityId) {
console.log("you are trying to delete city with id:" + cityId);
}