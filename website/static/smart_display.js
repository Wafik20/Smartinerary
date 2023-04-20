function shuffleItinerary(itinerary_id, itinerary_day, smart_id) {
  const morningActivityItem = document.querySelector(
    `.col-md-4[itinerary-id="${itinerary_id}"] .carousel-item[act-type="morning"]`
  );
  const afternoonActivityItem = document.querySelector(
    `.col-md-4[itinerary-id="${itinerary_id}"] .carousel-item[act-type="afternoon"]`
  );
  const eveningActivityItem = document.querySelector(
    `.col-md-4[itinerary-id="${itinerary_id}"] .carousel-item[act-type="evening"]`
  );
  const morningImgTag = morningActivityItem.querySelector("img");
  const morningActivityTag = morningActivityItem.querySelector("li");

  const afternoonImgTag = afternoonActivityItem.querySelector("img");
  const afternoonActivityTag = afternoonActivityItem.querySelector("li");

  const eveningImgTag = eveningActivityItem.querySelector("img");
  const eveningActivityTag = eveningActivityItem.querySelector("li");

  data = {
    smart_id: smart_id,
    itinerary_id: itinerary_id,
    day: itinerary_day,
  };
  axios
    .put("http://127.0.0.1:5000/smartineraries/shuffle", data)
    .then((response) => {
      res = response.data;
      new_morning_act = res["morning_activity"];
      new_afternoon_act = res["afternoon_activity"];
      new_evening_act = res["evening_activity"];

      morningImgTag.src = new_morning_act.activity_image;
      morningActivityTag.innerHTML = `<b>Morning Activity:</b> ${new_morning_act.activity_action} at ${new_morning_act.activity_place}`;

      afternoonImgTag.src = new_afternoon_act.activity_image;
      afternoonActivityTag.innerHTML = `<b>Afternoon Activity:</b> ${new_afternoon_act.activity_action} at ${new_afternoon_act.activity_place}`;

      eveningImgTag.src = new_evening_act.activity_image;;
      eveningActivityTag.innerHTML = `<b>Evening Activity:</b> ${new_evening_act.activity_action} at ${new_evening_act.activity_place}`
    });
}
