  var map;

  function initMap() {
  var myLatLng = {lat: -25.363, lng: 131.044};

  var map = new google.maps.Map(document.getElementById('map'), {
    zoom: 4,
    center: myLatLng
  });

  var marker = new google.maps.Marker({
    position: myLatLng,
    map: map,
    title: 'Hello World!'
  });


$(document).ready(function () {
  google.maps.event.addDomListener(window, 'load', initMap);

  console.log( "ready!" );
  document.write("aksndas'dkasda");

  //$(window).resize(resizeMap);
  //resizeMap();
});

