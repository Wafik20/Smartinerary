function shuffleItinerary(itinerary_id, itinerary_day, smart_id) {
  // Get the morning activity item in the itinerary
  const morningActivityItem = document.querySelector(
    `.col-md-4[itinerary-id="${itinerary_id}"] .carousel-item[act-type="morning"]`
  );
  // Get the afternoon activity item in the itinerary
  const afternoonActivityItem = document.querySelector(
    `.col-md-4[itinerary-id="${itinerary_id}"] .carousel-item[act-type="afternoon"]`
  );
  // Get the evening activity item in the itinerary
  const eveningActivityItem = document.querySelector(
    `.col-md-4[itinerary-id="${itinerary_id}"] .carousel-item[act-type="evening"]`
  );

  // Get the image tag and activity tag for the morning activity
  const morningImgTag = morningActivityItem.querySelector("img");
  const morningActivityTag = morningActivityItem.querySelector("li");

  // Get the image tag and activity tag for the afternoon activity
  const afternoonImgTag = afternoonActivityItem.querySelector("img");
  const afternoonActivityTag = afternoonActivityItem.querySelector("li");

  // Get the image tag and activity tag for the evening activity
  const eveningImgTag = eveningActivityItem.querySelector("img");
  const eveningActivityTag = eveningActivityItem.querySelector("li");

  // Set up the data to be sent with the PUT request
  data = {
    smart_id: smart_id,
    itinerary_id: itinerary_id,
    day: itinerary_day,
  };

  // Send the PUT request to the server to shuffle the activities
  axios
    .put("http://127.0.0.1:5000/smartineraries/shuffle", data)
    .then((response) => {
      // Get the shuffled activities from the response
      res = response.data;
      new_morning_act = res["morning_activity"];
      new_afternoon_act = res["afternoon_activity"];
      new_evening_act = res["evening_activity"];

      // Update the morning activity image and activity description
      morningImgTag.src = new_morning_act.activity_image;
      morningActivityTag.innerHTML = `<b>Morning Activity:</b> ${new_morning_act.activity_action} at ${new_morning_act.activity_place}`;

      // Update the afternoon activity image and activity description
      afternoonImgTag.src = new_afternoon_act.activity_image;
      afternoonActivityTag.innerHTML = `<b>Afternoon Activity:</b> ${new_afternoon_act.activity_action} at ${new_afternoon_act.activity_place}`;

      // Update the evening activity image and activity description
      eveningImgTag.src = new_evening_act.activity_image;
      eveningActivityTag.innerHTML = `<b>Evening Activity:</b> ${new_evening_act.activity_action} at ${new_evening_act.activity_place}`;
    });
}
