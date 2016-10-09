
// Function to init a new map and insert a long, and lat

function initMap(cur_lat, cur_long) {

  var myLatLng = {lat:cur_lat, lng: cur_long};


  var map = new google.maps.Map(document.getElementById('map'), {
    zoom: 4,
    center: myLatLng
  });
}



function sayhello(){




}