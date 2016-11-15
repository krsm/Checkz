// create global map, destination coordinates, and address
var map, dest, deslat, deslng, address;
// create a geocoder object
//var geocoder = new google.maps.Geocoder();

var address;

var favMap;
// Create a new blank array for all the listing markers. To be used with the clear button
var markers = []; // Global array
var infoWindow = new google.maps.InfoWindow();
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
  // set LatLng to SF
  var sfLatLng = {
    lat: 36.07094,
    lng: - 79.296201
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
  });
  // Event listenter to trigge locateUser
  document.getElementById('my_location_link').addEventListener('click', locateUser);
  // Event listenter to clear button - to remove all adde markers from map
  document.getElementById('clear_markers').addEventListener('click', hideListings);
  // Event listenter to get previous favotires places
  //var userId = $('#logout-link').data('userid');
  //document.getElementById('show_fav_link').addEventListener('click', getFavoriteSpots);
  // Event listener to any click in the screen to add a marker
  favMap.addListener('click', function (e) {
    // creating lat and long variables
    // Auxiliar variables to get lat anf lng drom Event
    var e_lat;
    var e_long;
    e_lat = e.latLng.lat();
    e_long = e.latLng.lng();
    addMarker(e.latLng, e_lat, e_long, favMap);
  }); // End of Function to listen to click event and addd a marker
  document.getElementById('show_fav_link').addEventListener('click', getFavoriteSpots);
} // End of Initialize Map

function addMarker(latLng, f_lat, f_lng, map) {
  // Add function to show
  var marker = new google.maps.Marker({
    position: latLng,
    map: map
  });
  // Call Function to add infoWindow as soon as the marker was created
  addInfoWindowFavoritePlaces(f_lat, f_lng, marker);
  // Push the marker to the array of markers.
  markers.push(marker);
  //debugger;
  //markers.push(marker);
  //alert(makers);
  //map.panTo(latLng);
  //alert(markers);
} // Functio to add infowindow to Marker

function addInfoWindowFavoritePlaces(lat, long, favMark) {
  var contentString = '<div id="content">' +
  '<p>Save as Favorite</p>' +
  '<table>' +
  '<tr>' +
  '<td>Type:</td>' +
  '<td><select id=\'type\'>' +
  '<option value=\'Food\' SELECTED>Food</option>' +
  '<option value=\'Fun\'>Fun</option>' +
  '<option value=\'Health\'>Health</option>' +
  '</select> </td>' +
  '</tr>' +
  '<tr><td></td><td>' +
  '<button type="button" onclick="createFavoriteSpot(' + lat + ',' + long + ')" class="btn btn-primary" id="favotite-button">Checkz!</button>' +
  '</td></tr>' +
  '</div>';
  // var contentString = '<div class="content">'+
  //  	'<table>' +
  // 	'<tr>'+
  //  		'<td>Type :</td>'+
  //  		'<td>'+
  //  		'<select id=\'type\'>'+
  // 		'<option value=\'Food\' SELECTED>Food</option>' +
  //  		'<option value=\'Fun\'>Fun</option>' +
  //  		'<option value=\'Health\'>Health</option>' +
  //  		'</select>'+
  //  		'</td>'+
  // 	'</tr>'+
  // 	'</table>'+
  //  	+ '<button type="button" onclick="createFavoriteSpot(' lat + ',' + long + ',' + value + ')" class="btn btn-primary" id="favotite-button">Checkz!</button>'
  // + '</div>';
  var infowindow = new google.maps.InfoWindow({
    content: contentString
  });
  favMark.addListener('click', function () {
    infowindow.open(map, favMark);
  });
}; // End of addInfoWindowFavoritePlaces
//====================================================================================
// this gets called when you click the fav-button rendered in InfoWindow
function createFavoriteSpot(fav_lat, fav_lng) {
  // grabbing user id from html that only shows if user is in session
  var userId = $('#logout-link').data('userid');
  if (userId !== undefined) {
    // Getting value of type_location from HTML
    var type_location = document.getElementById('type').value // Variable to be send to endpoint
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
// Function to create markers of previous saved favorite places and display InfoWindow to update waiting time
// functtion for debugger

function response_display(response) {
  alert(response);
}
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
  if (response['saved_places'].length === 0) {
    alert('User does not have saved any previous favorite place!')
  } else {
    //var placefavLatLng;
    //  var placefavMark;
    for (var i = 0; i < response['saved_places'].length; i++) {
      // unpacking response data
      place_lat = parseFloat(response['saved_places'][i]['location_lat']);
      place_long = parseFloat(response['saved_places'][i]['location_long']);
      place_waiting_time = response['saved_places'][i]['waiting_time'] || '';
      place_type_location = response['saved_places'][i]['type_location'];
      /***

    Waiting time will be definied as
    Short - Less 10 min
    Medium - Btw 15 and 25 min
    Long - Over 30 min

    ***/
      // Adding previous saved locations to map
      addMarkerPreviousPlaces(place_lat, place_long, favMap);
      // Adding infoWindow to the previous saved locations
    } // end of for

  } // end of else
} // End of function makeMarkers
//====================================================================================
// Add markers for previous saved places

function addMarkerPreviousPlaces(f_lat, f_lng, map) {
  // Add function to show
  var myLatLng = {
    lat: f_lat,
    lng: f_lng
  };
  var marker = new google.maps.Marker({
    position: myLatLng,
    map: map
  });
  // Call Function to add infoWindow as soon as the marker was created
  addInfoWindowPreviousPlaces(f_lat, f_lng, marker);
  // Push the marker to the array of markers.
  markers.push(marker);
  //debugger;
  //markers.push(marker);
  //alert(makers);
  //map.panTo(latLng);
  //alert(markers);
} // End offunction addMarkerPreviousPlaces
//====================================================================================
// Deletes all markers in the array by removing references to them.

function deleteMarkers() {
  clearMarkers();
  markers = [];
}// Sets the map on all markers in the array.

function setMapOnAll(map) {
  for (var i = 0; i < markers.length; i++) {
    markers[i].setMap(map);
  }
}// Removes the markers from the map, but keeps them in the array.

function clearMarkers() {
  setMapOnAll(null);
}//====================================================================================

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
    });
    //deleteMarkers();
    // getting remaining positions and populating the screen
    $.get('/get_favorite_places', userData, makeSavedMarkers);
    location.reload();
  }
} //====================================================================================

function UpdateWaitingTime(lat, long) {
  // to be created
  alert(lat, long);
} //====================================================================================

function addInfoWindowPreviousPlaces(lat, long, favMark) {
  /***

  Waiting time will be definied as
  Short - Less 10 min
  Medium - Btw 15 and 25 min
  Long - Over 30 min

  ***/
  var contentWaitinTime = '<div id="content">' +
  '<p>Current Waiting Time : </p>' +
  '<table>' +
  '<tr>' +
  '<td>Type:</td>' +
  '<td><select id=\'type_waiting_time\'>' +
  '<option value=\'Short\' SELECTED>Short</option>' +
  '<option value=\'Medium\'>Medium</option>' +
  '<option value=\'Long\'>Long</option>' +
  '</select> </td>' +
  '</tr>' +
  '<tr><td></td><td>' +
  '<button type="button" onclick="RemovePreviousSaved(' + lat + ',' + long + ')" class="btn btn-danger" id="remove_saved_places-button">Uncheckz!</button>' +
  '<button type="button" onclick="UpdateWaitingTime(' + lat + ',' + long + ')" class="btn btn-info" id="waiting_time-button">Update Waiting Time!</button>' +
  '</td></tr>' +
  '</div>';
  // var contentString = '<div class="content">'+
  //  	'<table>' +
  // 	'<tr>'+
  //  		'<td>Type :</td>'+
  //  		'<td>'+
  //  		'<select id=\'type\'>'+
  // 		'<option value=\'Food\' SELECTED>Food</option>' +
  //  		'<option value=\'Fun\'>Fun</option>' +
  //  		'<option value=\'Health\'>Health</option>' +
  //  		'</select>'+
  //  		'</td>'+
  // 	'</tr>'+
  // 	'</table>'+
  //  	+ '<button type="button" onclick="createFavoriteSpot(' lat + ',' + long + ',' + value + ')" class="btn btn-primary" id="favotite-button">Checkz!</button>'
  // + '</div>';
  var infowindow = new google.maps.InfoWindow({
    content: contentWaitinTime
  });
  favMark.addListener('click', function () {
    infowindow.open(map, favMark);
  });
}; // End of addInfoWindowFavoritePlaces
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

function hideListings() {
  for (var i = 0; i < markers.length; i++) {
    markers[i].setMap(null);
  }
}

//====================================================================================
// Code related to geocoding
//====================================================================================
//function getURLParam (name) {
//
//  var results = new RegExp('[\?&]' + name + '=([^&#]*)').exec(window.location.href);
//  if (results === null) {
//    return null;
//  } else {
//    return results[1] || 0;
//  }
//}
// google maps autocomplete search bar for homepage
//function hpInit() {
//    var searchTerm = document.getElementById('search-term');
//    var hpAutoComplete = new google.maps.places.Autocomplete(searchTerm);
//}
//
//
//function geocodeAddress(geocoder, map, address) {
//  // clear the pre-existing markers and reset holdMarkers array to empty
//  //for (var i = 0; i < holdMarkers.length; i++) {
//    //holdMarkers[i].setMap(null);
//  //}
//
//  holdMarkers = [];
//
//  // geocode user's destination in lat lngs
//  geocoder.geocode({'address': address}, function(results, status) {
//    // if the status comes back OK, get the destination location
//    if (status === google.maps.GeocoderStatus.OK) {
//      dest = results[0].geometry.location;
//      map.setCenter(dest);
//
//      deslat = dest.lat();
//      deslng = dest.lng();
//
//      // create a marker of destination, place on map
//      var marker = new google.maps.Marker({
//        map: map,
//        animation: google.maps.Animation.DROP,
//        position: dest
//      });
//      holdMarkers.push(marker);
//      //getEligibleSpots(limit);
//    } else {
//      console.log('Something went wrong: ' + status);
//    }
//  });
//}
//
//function goHomepageSearch (hpAddress) {
//// scenario where user initates search from homepage
//  if (hpAddress !== 0) {
//      var decodeAddress = decodeURIComponent(hpAddress);
//      address = decodeAddress.split('+').join(' ');
//
//      // grab current day of week and time
//      // var todayDate = new Date();
//      // var weekDays = new Array(7);
//      // weekDays[0]=  "Su";
//      // weekDays[1] = "M";
//      // weekDays[2] = "Tu";
//      // weekDays[3] = "W";
//      // weekDays[4] = "Th";
//      // weekDays[5] = "F";
//      // weekDays[6] = "Sa";
//      // var todayDay = weekDays[todayDate.getDay()];
//      // $('#day').val(todayDay);
//      //
//      // var todayStartHr = todayDate.getHours();
//      // todayStartHr = todayStartHr + "00";
//      // $('#starttime').val(todayStartHr);
//      //
//      // todayEndHr = parseInt(todayStartHr);
//      // todayEndHr = todayEndHr + 100;
//      // todayEndHr = todayEndHr.toString();
//      // $('#endtime').val(todayEndHr);
//
//      geocodeAddress(geocoder, map, address);
//      //$('#show-more').show();
//    }
//}



//====================================================================================
// End of Code related to geocoding
//====================================================================================


$(document).ready(function () {

  // Event to load the map
  google.maps.event.addDomListener(window, 'load', initFavMap);


 //  address = document.getElementById('destination').value;

  //====================================================================================
  // Code related to geocoding
  // google maps related to geocoding
  //google.maps.event.addDomListener(window, 'load', hpInit);
//
//  // enter scenario where user began non-default search from search page form
//  $('#submit').click(function (evt) {
//    evt.preventDefault();
//    // get the value of user's destination input from form
//    address = document.getElementById('search-term').value;
//
//    alert(address);
//   });
//

   // alert(address);


});
