// create global map, destination coordinates, and address
// Create a new blank array for all the listing markers. To be used with the clear button
var markers = [];
var infoWindows = []; // Global array to store all infoWindows
var dest;
var deslat;
var deslng;
var marker_address; // variable to receive address based on the lat, and long
// create a geocoder object
var geocoder = new google.maps.Geocoder();
var address;
var autocomplete;
// ====================================
var directionsDisplay = new google.maps.DirectionsRenderer();
var directionsService = new google.maps.DirectionsService();
// ====================================
// helper variable related to display infoWindow
var bool_display_infowindow = new Boolean(false);
function setTruebooldisplayinfowindow() {
  bool_display_infowindow = true;
}
function setFalsebooldisplayinfowindow() {
  bool_display_infowindow = false;
} // End of helper variable related to infoWindow
// ====================================
//====================================================================

var favMap;
//var infoWindow = new google.maps.InfoWindow();
// Initialize Map
function initFavMap() {

  //====================================================================================
  // Code related to geocoding
  //  // grab search-term from URL
  //var hpAddress = getURLParam('search-term');
  //
  //if (hpAddress !== null) {
  //  goHomepageSearch(hpAddress);
  //}
  // Enf of Code related to geocoding
  //====================================================================================
  //Initialize value
  // set LatLng to Durham
  var sfLatLng = {
    lat: 35.994,
    lng: - 78.8986 //
    //35.9940° N, 78.8986° W
  };
  // create a map object and specify the DOM element for display
  // map appears in map.html
  favMap = new google.maps.Map(document.getElementById('map'), {
    center: sfLatLng,
    scrollwheel: true,
    zoom: 13,
    zoomControl: true,
    panControl: true,
    streetViewControl: true,
    mapTypeId: google.maps.MapTypeId.ROADMAP
  }); // End of favMap
  // directionsDisplay.setMap(favMap);
  // ==============================================================
  // Related to geocoding
  // address = /** @type {!HTMLInputElement} */
  // (document.getElementById('pac-input'));
  // // create an autocomplete search bar
  // autocomplete = new google.maps.places.Autocomplete(address);
  //alert(autocomplete);
  // document.getElementById('pac-input').addEventListener('click', addMarkerSearch(autocomplete));
  //addMarkerSearch
  // Event listenter to get previous favotires places
  //var userId = $('#logout-link').data('userid');
  //document.getElementById('show_fav_link').addEventListener('click', getFavoriteSpots);
  // Event listenter to trigger locateUser
  document.getElementById('my_location_link').addEventListener('click', locateUser);
  // Event listenter to clear button - to remove all adde markers from map
  document.getElementById('clear_markers').addEventListener('click', hideListings);
  // Event listener to any click in the screen to add a marker
  favMap.addListener('click', function (e) {
    // creating lat and long variables
    // Auxiliar variables to get lat and lng dom Event
    var e_lat;
    var e_long;
    e_lat = e.latLng.lat();
    e_long = e.latLng.lng();
    addMarker(e.latLng, e_lat, e_long, favMap);
  }); // End of Function to listen to click event and addd a marker
  // ==============================================================
  // Event listenter to get favotites previous savaed places
  document.getElementById('show_fav_link').addEventListener('click', getFavoriteSpots);
  // Set the infoWindow bool to false then will have an event click
  document.getElementById('show_fav_link').addEventListener('click', setFalsebooldisplayinfowindow);
} // End of Initialize Map

function addMarker(latLng, lat, long, map) {
  //marker_address = getAddress(f_lat, f_lng);
  //alert(marker_address);
  //if (marker_address != 'not_available') {
  // verify if it is a valid address
  // Add function to show
  var marker = new google.maps.Marker({
    position: latLng,
    map: map
  });
  // Push the marker to our array of markers.
  var infowindow = new google.maps.InfoWindow();
  // Content to be dsiplayed in the infowindow
  var content_string = '<div class="card-title">' +
  '<p> To be replaced by address</p>' +
  '<label> Choose location type </label>' +
  '<select id="type_selected_location" class="browser-default">' +
  '<option value="" disabled selected> Checkz place as favorite </option>' +
  '<option value="Eat">Eat</option>' +
  '<option value="Fun">Fun</option>' +
  '<option value="Health">Health</option>' +
  '</select>' + //Waiting time
  '<button class="btn waves-effect waves-light green" id="favotite-button" type="button" onclick="createFavoriteSpot(' + lat + ',' + long + ')" > Checkz! </button>' +
  '<p> </p>' +
  '<label> Directions to shortest waiting time </label>' +
  '<select id="type_selected_navigate" class="browser-default">' +
  '<option value="" disabled selected> Select type of place to get directions to</option>' +
  '<option value="Eat">Eat</option>' +
  '<option value="Fun">Fun</option>' +
  '<option value="Health">Health</option>' +
  '</select>' + //Navigate
  '<button class="btn waves-effect waves-light blue" id="navigate-button" type="button" onclick="get_location_shortest_time(' + lat + ',' + long + ')" > Get directions</button>' +
  '</div>' +
  '</div>';
  bindInfoWindow(marker, map, infowindow, content_string, bool_display_infowindow);
  markers.push(marker);
} // End of Function

// Function to add infowindow to Marker
function bindInfoWindow(marker, map, infowindow, html_content, bool_updated_waiting_time) {
  if (bool_updated_waiting_time == false) {
    google.maps.event.addListener(marker, 'click', function () {
      infowindow.close();
      infowindow.setContent(html_content);
      infowindow.open(map, marker);
      //infowindow.marker = marker;
    });
  } else {
    var oldLat = marker.getPosition().lat();
    var oldLng = marker.getPosition().lng();
    infowindow.close();
    infowindow.setContent(html_content);
    infowindow.open(map, marker);
    //infowindow.marker = marker;
  }  // // Make sure the marker property is cleared if the infowindow is closed.
  // infowindow.addListener('closeclick', function() {
  //     infowindow.marker = null;
  // });

  setFalsebooldisplayinfowindow();
}// End of function

// Function to display directions in the map
function getDirections(response) {

  directionsDisplay.setMap(favMap);



  if (response['saved_places'].length == 0) {
    alert('User does not have saved any previous favorite place of selected type!')
  } else {
    //var placefavLatLng;
    //  var placefavMark;
    //  var x = response['saved_places'].length - (response['saved_places'].length -1);//hahahaha
    for (var i = 0; i < response['saved_places'].length; i++) {
      // unpacking response data
      //variables related to destination
      dest_lat = parseFloat(response['saved_places'][i]['location_lat']);
      dest_long = parseFloat(response['saved_places'][i]['location_long']);
      // //variables related to current user location
      current_location_lat = parseFloat(response['saved_places'][i]['current_location_lat']);
      current_location_long = parseFloat(response['saved_places'][i]['current_location_long']);
      //
      // saved_places.append({'current_location_lat': location_lat,
      //               'current_location_long':location_long})
      var markLatLng = new google.maps.LatLng(dest_lat, dest_long);
      //variable relate to user current location
      var curLatLng = new google.maps.LatLng(current_location_lat, current_location_long);
      //
      // alert(markLatLng);
      // alert(curLatLng);
      //  directionsDisplay.setMap(favMap);
      // directionsDisplay.setPanel(document.getElementById('right-panel'));
      //
      var request = {
        // window.userLocation is global
        origin: curLatLng,
        destination: markLatLng,
        travelMode: google.maps.TravelMode.DRIVING
      };
      directionsService.route(request, function (result, status) {
        if (status == 'OK') {
          directionsDisplay.setDirections(result);

           directionsDisplay.setPanel(document.getElementById('myModal'));
          //open a window
          // panel=window.open('about:blank','panel','width=200,height=200,scrollbars=yes');
          // //create a document inside te window
          // // panel.document.open();
          // panel.document.write('<body/>');
          // // panel.document.close();
          // //set the panel
          // directionsDisplay.setPanel(panel.document.body);
          // //bring window into front
          // panel.focus();
          //
          //  directionsDisplay.setPanel(document.getElementById("myModal"));
        }
      });
    } // End of for loop

  } //End of else

} //End of function
//====================================================================================
// this gets called when you click the navigate-button rendered in InfoWindow

function get_location_shortest_time(fav_lat, fav_lng) {
  // grabbing user id from html that only w if user is in session
  var userId = $('#logout-link').data('userid');
  if (userId !== undefined) {
    // Getting value of type_location from HTML
    var type_location = document.getElementById('type_selected_navigate').value // Variable to be send to endpoint
    alert(type_location);
    var markerData = {
      'type_location': type_location,
      'user_id': userId,
      'location_lat': fav_lat,
      'location_long': fav_lng
    };
    $.get('/get_direction_shortest_time', markerData, getDirections);
  } else {
    alert('You need to be logged in to navigate to previous saved spots.');
  }
} //====================================================================================
//====================================================================================
// this gets called when you click the fav-button rendered in InfoWindow

function createFavoriteSpot(fav_lat, fav_lng) {
  // grabbing user id from html that only shows if user is in session
  var userId = $('#logout-link').data('userid');
  if (userId !== undefined) {
    // Getting value of type_location from HTML
    var type_location = document.getElementById('type_selected_location').value // Variable to be send to endpoint
    debugger;
    var markerData = {
      'type_location': type_location,
      'user_id': userId,
      'location_lat': fav_lat,
      'location_long': fav_lng
    };
    $.post('/save_favorite_place/', markerData, function () {
      alert('Your marker has been favorited.');
      // TO DO: Turn marker a different color
    });
  } else {
    alert('You need to be logged in to favorite spots.');
  }
} //====================================================================================
// this gets called when you click the fav-button rendered in InfoWindow

function getFavoriteSpots() {
  var userId = $('#logout-link').data('userid');
  //alert('function getFavoriteSpots was trigged')
  if (userId !== undefined && userId !== null) {
    var userData = {
      'user_id': userId
    };
    $.get('/get_favorite_places', userData, makeSavedMarkers);
  } // end of if UserId

} //====================================================================================
// this function is called to get updated waiting time
// function getUpdateWaitingTime() {
//   var userId = $('#logout-link').data('userid');
//   //alert('function getFavoriteSpots was trigged')
//   if (userId !== undefined && userId !== null) {
//     var userData = {
//       'user_id': userId
//     };
//     $.get('/get_updated_waiting_time', userData, makeSavedMarkers);
//   } // end of if UserId
//
// } //====================================================================================
// Function to create markers of previous saved favorite places and display InfoWindow to update waiting time
// functtion for debugger

function makeSavedMarkers(response) {
  /***
{'saved_places'[{'user_id': place.user_id,
'created_timestamp': place.created_timestamp,
'modified_timestamp': place.modified_timestamp,
'location_lat': place.location_lat,
'location_long': place.location_long,
'address': place.address,
'waiting_time': place.waiting_time,
'type_location': place.type_location})
***/
  // Verify if response was empty
  //=== 	equal value and equal type
  if (response['saved_places'].length == 0) {
    alert('User does not have saved any previous favorite place!')
  } else {
    for (var i = 0; i < response['saved_places'].length; i++) {
      // unpacking response data
      place_lat = parseFloat(response['saved_places'][i]['location_lat']);
      place_long = parseFloat(response['saved_places'][i]['location_long']);
      place_waiting_time = response['saved_places'][i]['waiting_time'] || '';
      place_type_location = response['saved_places'][i]['type_location'];

      // Adding previous saved locations to map
      addMarkerPreviousPlaces(place_lat, place_long, favMap, place_waiting_time, place_type_location);
      // Adding infoWindow to the previous saved locations
    } // end of for

  } // end of else

} // End of function makeMarkers
//====================================================================================
// Add markers for previous saved places

function addMarkerPreviousPlaces(lat, long, map, waiting_time, type_location) {
  // Add function to show
  var myLatLng = {
    lat: lat,
    lng: long
  };
  waiting_time = parseFloat(waiting_time);
  // 0 - 100 min
  // 0 - 20 fast - green
  // 20 - 45 - Medium - blue
  // over 45 too slow - red
  // Add function to show
  var aux_icon;
  // switch (type_location) {
  //   case "Fun":
  //     aux_icon = '/static/img/food_green.png'
  //   case "Food":
  //     aux_icon = '/static/img/food_green.png'
  //   case "Health":
  //   aux_icon = '/static/img/food_green.png'
  // }
  if (waiting_time < 20) {
    //aux_icon: 'http://maps.google.com/mapfiles/ms/icons/green.png'
    switch (type_location) {
      case 'Fun':
        aux_icon = '/static/img/fun_green.png'
        break
      case 'Eat':
        aux_icon = '/static/img/food_green.png'
        break
      case 'Health':
        aux_icon = '/static/img/health_green.png'
        break
    }    // aux_icon ='http://maps.google.com/mapfiles/ms/icons/green.png';

  }
  if ((20 < waiting_time) && (waiting_time < 45)) {
    switch (type_location) {
      case 'Fun':
        aux_icon = '/static/img/fun_yellow.png'
        break
      case 'Eat':
        aux_icon = '/static/img/food_yellow.png'
        break
      case 'Health':
        aux_icon = '/static/img/health_yellow.png'
        break
    }    // aux_icon= 'http://maps.google.com/mapfiles/ms/icons/yellow.png';
    //  icon: 'http://maps.google.com/mapfiles/ms/icons/blue.png'

  }
  if (waiting_time > 45) {
    switch (type_location) {
      case 'Fun':
        aux_icon = '/static/img/fun_red.png'
        break
      case 'Eat':
        aux_icon = '/static/img/food_red.png'
        break
      case 'Health':
        aux_icon = '/static/img/health_red.png'
        break
    }    //aux_icon: 'http://maps.google.com/mapfiles/ms/icons/red.png'
    // aux_icon ='http://maps.google.com/mapfiles/ms/icons/red.png';

  }
  var marker = new google.maps.Marker({
    position: myLatLng,
    map: map,
    icon: aux_icon
  });
  // Push the marker to our array of markers.
  //markers.push(marker);
  var infowindow = new google.maps.InfoWindow();
  var aux_waiting_time = Math.round(waiting_time);
  var contentWaitinTime = '<div id="content">' +
  '<p>Current Waiting Time : ' + aux_waiting_time + 'min , ' + 'Type of location: ' + type_location + '</p>' +
  '<p>Update Waiting Time </p>' +
  '<form action="#">' +
  '<p class="range-field">' +
  '<input type="range" id="updated_waiting_time" min="0" max="100" />' +
  '</p>' +
  '</form>' +
  '<button class="btn waves-effect waves-light yellow darken-4" id="waiting_time" type="button"onclick="UpdateWaitingTime(' + lat + ',' + long + ')">Update Waiting Time!</button>' +
  '<p> </p>' +
  '<button class="btn waves-effect waves-light red" id="remove_saved_places" type="button" onclick="RemovePreviousSaved(' + lat + ',' + long + ')" >Uncheckz!</button>' +
  '</div>';
  bindInfoWindow(marker, map, infowindow, contentWaitinTime, bool_display_infowindow);
  markers.push(marker);
} // End offunction addMarkerPreviousPlaces
//====================================================================================

function RemovePreviousSaved(lat, long) {
  //Getting userID
  var userId = $('#logout-link').data('userid');
  if (userId !== undefined) {
    var delData = {
      'user_id': userId,
      'location_lat': lat,
      'location_long': long
    };
    var userData = {
      'user_id': userId
    };
    $.post('/remove_favorite_place', delData, function () {
      alert('That spot has been deleted.');
      remove_marker(lat, long);
    });
    // getting remaining positions and populating the screen
    $.get('/get_favorite_places', userData, makeSavedMarkers);
    //location.reload();
  }
} //====================================================================================

function UpdateWaitingTime(lat, long) {
  //Getting userID
  var userId = $('#logout-link').data('userid');
  var updated_waiting_time = document.getElementById('updated_waiting_time').value
  if (userId !== undefined) {
    var updatedData = {
      'user_id': userId,
      'location_lat': lat,
      'location_long': long,
      'updated_waiting_time': updated_waiting_time
    };
    $.post('/update_waiting_time', updatedData, function () {
      //alert(updated_waiting_time);
    });
    // attempt to close the marker to avoid duplicate infowindow
    setTruebooldisplayinfowindow();
    close_marker(lat, long);
    $.get('/get_updated_waiting_time', updatedData, makeSavedMarkers);
    //Recall function to show favorites, to display update waiting time
  }
} //====================================================================================
//====================================================================================

function locateUser() {
  var browserSupportFlag = new Boolean();
  if (navigator.geolocation) {
    /* geolocation is available */
    browserSupportFlag = true;
    navigator.geolocation.getCurrentPosition(function (position) {
      var lat = position.coords.latitude;
      var long = position.coords.longitude;
      //infoWindow.setPosition(pos);
      //infoWindow.setContent('Location found.');
      //favMap.setCenter(pos);
      var favMark = new google.maps.Marker({
        map: favMap,
        position: new google.maps.LatLng(lat, long),
        icon: 'http://maps.google.com/mapfiles/ms/icons/blue.png'
      });
      // Push the marker to the array of markers.
      markers.push(favMark);
      // Call function to display pop up to save place as favorite
      addInfoWindowFavoritePlaces(lat, long, favMark);
      window.userLocation = new google.maps.LatLng(position.coords.latitude, position.coords.longitude);
      // anything that needs to ref userLocation MUST happen before the end of this function
    }, function () {
      handleNoGeolocation(browserSupportFlag);
    });
  } // end if
  // browser doesn't support Geolocation so call the handleNoGeolocation fn
   else {
    /* geolocation is not available */
    browserSupportFlag = false;
    handleNoGeolocation(browserSupportFlag);
  }
} // end of function locateUser

function handleNoGeolocation(errorFlag) {
  if (errorFlag == true) {
    alert('Geolocation service failed.');
  } else {
    alert('Your browser does not support geolocation.');
  }
} // End of handleNoGeolocation
// This function will loop through the listings and hide them all.
//function will hide an specific marker based on a predefinied position

function close_marker(lat, long) {
  var new_marker_position = new google.maps.LatLng(lat, long);
  for (var i = 0; i < markers.length; i++) {
    var marker_oldLat = markers[i].getPosition().lat();
    var marker_oldLng = markers[i].getPosition().lng();
    if (lat == marker_oldLat) {
      if (long == marker_oldLng) {
        markers[i].setMap(null);
      } // end of if long

    } // end of id lat

  } // End of for

} // End of close_marker
// function to hide all markers


// // // function to clear routes on the map
// function clear_routes(){
//   // directionsDisplay.setMap(null);
//
//   // Clear past routes
// if (directionsDisplay != null) {
//     directionsDisplay.setMap(null);
//     directionsDisplay = null;
// }
// }



function hideListings() {
  for (var i = 0; i < markers.length; i++) {
    markers[i].setMap(null);
  }// end of for
  // clear_routes();
} //====================================================================================
// Code related to geocoding
//====================================================================================

function addMarkerSearch(hpAddress) {
  if (hpAddress !== 0) {
    var decodeAddress = decodeURIComponent(hpAddress);
    var aux_address = decodeAddress.split('+').join(' ');
    geocodeAddress(geocoder, favMap, aux_address);
  }
}
function geocodeAddress(geocoder, map, address) {
  // clear the pre-existing markers and reset holdMarkers array to empty
  //hideListings() - TODO verify the need to clean the markers
  // geocode user's destination in lat lngs
  geocoder.geocode({
    'address': address
  }, function (results, status) {
    // if the status comes back OK, get the destination location
    if (status === google.maps.GeocoderStatus.OK) {
      dest = results[0].geometry.location;
      map.setCenter(dest);
      deslat = dest.lat();
      deslng = dest.lng();
      addMarker(dest, deslat, deslng, map);
      // // create a marker of destination, place on map
      // var marker1 = new google.maps.Marker({
      //   map: map,
      //   //animation: google.maps.Animation.DROP,
      //   position: dest
      // });
      // addInfoWindowFavoritePlaces(deslat,deslng,marker1);
      // markers.push(marker);
    } else {
      alert('Something went wrong: ' + status);
    }
  });
} //Function to add marker to search place

function getAddress(lat, long) {
  // It will return a string with address
  //function to return address based on lat, and long
  // It will be used to show addres in the top of marker
  var latlng = {
    lat: parseFloat(lat),
    lng: parseFloat(long)
  };
  if (geocoder) {
    geocoder.geocode({
      'latLng': latlng
    }, function (results, status) {
      if (status == google.maps.GeocoderStatus.OK) {
        if (results[1]) {
          return results[1].formatted_address;
        } else {
          alert('Not a valid address.');
          // Case that not valid address
          var not_valid_address = 'not_available';
          return not_valid_address;
        }
      } else {
        alert('Geocoder failed due to: ' + status);
      }
    });
  }
} //====================================================================================
// End of Code related to geocoding
//====================================================================================
// function to remove a marker

function remove_marker(lat, long) {
  //var to_be_removed_marker_position = new google.maps.LatLng(lat, long);
  for (var i = 0; i < markers.length; i++) {
    var aux_maker_Lat = markers[i].getPosition().lat();
    var aux_marker_Lng = markers[i].getPosition().lng();
    if (lat == aux_maker_Lat) {
      if (long == aux_marker_Lng) {
        markers[i] = [
        ];
      } // end of if long

    } // end of id lat

  } // end of for
  // directionsDisplay.setMap(null);

} //====================================================================================
// //function will hide an specific marker based on a predefinied position
// function close_marker(lat, long) {
//
//     var new_marker_position = new google.maps.LatLng(lat, long);
//
//     for (var i = 0; i < markers.length; i++) {
//
//         var marker_oldLat = markers[i].getPosition().lat();
//         var marker_oldLng = markers[i].getPosition().lng();
//
//         if (lat == marker_oldLat) {
//             if (long == marker_oldLng) {
//                 markers[i].setMap(null);
//             } // end of if long
//         } // end of id lat
//
//     } // End of for
//
// } // End of close_marker

function closeAllInfoWindows(lat, long) {
  for (var i = 0; i < infoWindows.length; i++) {
    position: new google.maps.LatLng(lat, long);
    var info_position;
    info_position = infoWindows[i].getposition();
    if (position == info_position) {
      infoWindows[i].close();
    } // end of if

  } // end of for

} // end of function

$(document).ready(function () {
  //google.maps.event.addDomListener(window, 'resize', initFavMap);
  // Event to load the map
  google.maps.event.addDomListener(window, 'load', initFavMap);
  // related to materialize library
  $('select').material_select();
  // related to display the infoWindow
  setFalsebooldisplayinfowindow();
});
