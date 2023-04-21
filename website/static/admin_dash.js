// Delete city
function deleteCity(cityId) {
  axios
    .delete(`http://127.0.0.1:5000/admin/city?city_id=${cityId}`)
    .then((response) => {
      // Remove the row from the table
      const row = document.querySelector(`tr[data-city-id="${cityId}"]`);
      row.parentNode.removeChild(row);
    })
    .catch((error) => {
      console.error(error);
    });
}

// Delete activity
function deleteActivity(ActivityId) {
  axios
    .delete(`http://127.0.0.1:5000/admin/activity?activity_id=${ActivityId}`)
    .then((response) => {
      // Remove the row from the table
      const row = document.querySelector(
        `tr[data-activity-id="${ActivityId}"]`
      );
      row.parentNode.removeChild(row);
    })
    .catch((error) => {
      console.error(error);
    });
}

// Toggle admin status of a user
function toggleAdmin(userId) {
  axios
    .post(`http://127.0.0.1:5000/admin/user/${userId}/toggle_admin`)
    .then((response) => {
      // Update the button text and disabled state
      const button = document.querySelector(`button[data-user-id="${userId}"]`);
      const is_admin = response.data.is_admin;
      if (is_admin) {
        button.classList.remove("btn-primary", "btn-secondary");
        button.classList.add("btn-success");
        button.innerHTML = "Admin";
      } else {
        button.classList.remove("btn-primary", "btn-success");
        button.classList.add("btn-secondary");
        button.innerHTML = "User";
      }
    })
    .catch((error) => {
      console.error(error);
    });
}

// Delete user
function deleteUser(userId) {
  console.log(`http://127.0.0.1:5000/users?user_id=${userId}/`);
  axios
    .delete(`http://127.0.0.1:5000/users?user_id=${userId}`)
    .then((response) => {
      // Remove the card from the DOM
      const card = document.querySelector(`div[data-smart-id='${smart_id}']`);
      if (card) {
        card.parentNode.removeChild(card);
      }
    })
    .catch((error) => {
      console.error(error);
    });
}
