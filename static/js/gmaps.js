
 function initialize() {
    var myLatlng = new google.maps.LatLng({{ geolat }}, {{ geolong }});

    var myOptions = {
        zoom: 16,
        center: myLatlng,
        streetViewControl: true,
        mapTypeControl: true,
        zoomControl: true,
        mapTypeId: google.maps.MapTypeId.SATELLITE
    };
    map = new google.maps.Map(document.getElementById("map_canvas"), myOptions);

    var marker = new google.maps.Marker({
        draggable: true,
        position: myLatlng,
        map: map,
        title: "Your location"
    });

    google.maps.event.addListener(marker, 'dragend', function (event) {
            sendCoords(event.latLng.lat(),event.latLng.lng() )
    });

    // close popup window
    google.maps.event.addListener(map, 'click', function() {
    infowindow.close();
    });


        function initMap(cur_lat, cur_long) {
        var map = new google.maps.Map(document.getElementById('map'), {
          zoom: 8,
          center: {lat: -34.397, lng: 150.644}
        });
        var geocoder = new google.maps.Geocoder();

        document.getElementById('submit').addEventListener('click', function() {
          geocodeAddress(geocoder, map);
        });
      }



      function geocodeAddress(geocoder, resultsMap) {
        var address = document.getElementById('address').value;
        geocoder.geocode({'address': address}, function(results, status) {
          if (status === 'OK') {
            resultsMap.setCenter(results[0].geometry.location);
            var marker = new google.maps.Marker({
              map: resultsMap,
              position: results[0].geometry.location
            });
          } else {
            alert('Geocode was not successful for the following reason: ' + status);
          }
        });
      }
