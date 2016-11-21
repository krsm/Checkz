// create global map, destination coordinates, and address
var map,
    dest,
    deslat,
    deslng;
// create a geocoder object
var geocoder = new google.maps.Geocoder();
var address;
var autocomplete;
// ====================================
// helper variable related to infoWindow

var bool_display_infowindow = new Boolean(false);

function setTruebooldisplayinfowindow(){

  bool_display_infowindow = true;

}

function setFalsebooldisplayinfowindow(){

  bool_display_infowindow = false;

}
// End of helper variable related to infoWindow
// ====================================
//====================================================================
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
        lat: 37.780919,
        lng: -122.465680

        //  37.780919, -122.465680
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
    // ==============================================================
    // // Related to geocoding
    // address = /** @type {!HTMLInputElement} */
    //     (document.getElementById('pac-input'));
    // // create an autocomplete search bar
    // autocomplete = new google.maps.places.Autocomplete(address);
    // alert(autocomplete)
    // ==============================================================
    // Event listenter to trigger locateUser
    document.getElementById('my_location_link').addEventListener('click', locateUser);
    // Event listenter to clear button - to remove all adde markers from map
    document.getElementById('clear_markers').addEventListener('click', hideListings);
    //document.getElementById('pac-input').addEventListener('click', addMarkerSearch(autocomplete));
    //addMarkerSearch
    // Event listenter to get previous favotires places
    //var userId = $('#logout-link').data('userid');
    //document.getElementById('show_fav_link').addEventListener('click', getFavoriteSpots);
    // Event listener to any click in the screen to add a marker
    favMap.addListener('click', function(e) {
        // creating lat and long variables
        // Auxiliar variables to get lat and lng dom Event
        var e_lat;
        var e_long;
        e_lat = e.latLng.lat();
        e_long = e.latLng.lng();
        addMarker(e.latLng, e_lat, e_long, favMap);
    }); // End of Function to listen to click event and addd a marker
    document.getElementById('show_fav_link').addEventListener('click', getFavoriteSpots);
    // Set the infoWindow bool to false then will have an event click
    document.getElementById('show_fav_link').addEventListener('click', setFalsebooldisplayinfowindow);
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
    alert(markers);
} // Function to add infowindow to Marker

function addInfoWindowFavoritePlaces(lat, long, favMark) {

    var contentString = '<div class="card-title">' +
        '<p> To be replaced by address</p>' +
        '<label> Choose location type </label>' +
        '<select id="type_selected_location" class="browser-default">' +
        '<option value="" disabled selected> Checkz place as favorite </option>' +
        '<option value="Eat">Eat</option>' +
        '<option value="Fun">See</option>' +
        '<option value="Health">Health</option>' +
        '</select>' +
        //Waiting time
        '<button class="btn waves-effect waves-light green" id="favotite-button" type="button" onclick="createFavoriteSpot(' + lat + ',' + long + ')" >Checkz!</button>' +
        '<p> </p>' +
        '<label> Directions to shortest waiting time </label>' +
        '<select id="type_selected_navigate" class="browser-default">' +
        '<option value="" disabled selected> Select type of place to get directions to</option>' +
        '<option value="Eat">Eat</option>' +
        '<option value="Fun">See</option>' +
        '<option value="Health">Health</option>' +
        '</select>' +
        //Navigate
        '<button class="btn waves-effect waves-light blue" id="navigate-button" type="button" onclick="createFavoriteSpot(' + lat + ',' + long + ')" >Get directions!</button>' +
        '</div>';
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
    favMark.addListener('click', function() {
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
        var type_location = document.getElementById('type_selected_location').value // Variable to be send to endpoint
        debugger;
        var markerData = {
            'type_location': type_location,
            'user_id': userId,
            'location_lat': fav_lat,
            'location_long': fav_lng
        };
        $.post('/save_favorite_place/', markerData, function() {
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
            addMarkerPreviousPlaces(place_lat, place_long, favMap,place_waiting_time);
            // Adding infoWindow to the previous saved locations
        } // end of for

    } // end of else

} // End of function makeMarkers
//====================================================================================
// Add markers for previous saved places
function addMarkerPreviousPlaces(f_lat, f_lng, map, waiting_time) {
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
    addInfoWindowPreviousPlaces(f_lat, f_lng, marker,waiting_time);
    // Push the marker to the array of markers.
    markers.push(marker);
} // End offunction addMarkerPreviousPlaces
//====================================================================================
// Deletes all markers in the array by removing references to them.
function deleteMarkers() {
    clearMarkers();
    markers = [];
} // Sets the map on all markers in the array.

function setMapOnAll(map) {
    for (var i = 0; i < markers.length; i++) {
        markers[i].setMap(map);
    }
} // Removes the markers from the map, but keeps them in the array.

function clearMarkers() {
    setMapOnAll(null);
} //====================================================================================

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
        $.post('/remove_favorite_place', delData, function() {
            alert('That spot has been deleted.');
        });
        //deleteMarkers();
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
          'updated_waiting_time':updated_waiting_time
      };

      $.post('/update_waiting_time', updatedData, function() {
          alert('Waiting time has been updated.');
          //alert(updated_waiting_time);
      });
        setTruebooldisplayinfowindow();
        getFavoriteSpots();

      //Recall function to show favorites, to display update waiting time


}} //====================================================================================

function addInfoWindowPreviousPlaces(lat, long, favMark,waiting_time) {
    /***

    Waiting time will be definied as
    Short - Less 10 min
    Medium - Btw 15 and 25 min
    Long - Over 30 min


    ***/
    //bool_display_infowindow will be used to show infowindow in case of update of waiting time

    var aux_waiting_time = Math.round(waiting_time);
    var contentWaitinTime = '<div id="content">' +
        '<p>Current Waiting Time : '+ aux_waiting_time +' min</p>' +
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

    //alert(bool_display_infowindow);

    var infowindow = new google.maps.InfoWindow({
        content: contentWaitinTime
    });

    // if case to show to display infowindow
    if (bool_display_infowindow == true) {

        infowindow.open(map, favMark);
    }
    else {

      favMark.addListener('click', function() {
          infowindow.open(map, favMark);
      });

    }



}; // End of addInfoWindowFavoritePlaces
//====================================================================================
function locateUser() {
    var browserSupportFlag = new Boolean();
    if (navigator.geolocation) {
        /* geolocation is available */
        browserSupportFlag = true;
        navigator.geolocation.getCurrentPosition(function(position) {
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
        }, function() {
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
    markers = [];
} //====================================================================================
// Code related to geocoding
//====================================================================================

function geocodeAddress(geocoder, map, address) {
    // clear the pre-existing markers and reset holdMarkers array to empty
    //hideListings() - TODO verify the need to clean the markers
        // geocode user's destination in lat lngs
    geocoder.geocode({
        'address': address
    }, function(results, status) {
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
            console.log('Something went wrong: ' + status);
        }
    });
}
//Function to add marker to search place
function addMarkerSearch(hpAddress) {

    if (hpAddress !== 0) {
        var decodeAddress = decodeURIComponent(hpAddress);
        var aux_address = decodeAddress.split('+').join(' ');
        geocodeAddress(geocoder, favMap, aux_address);
    }
}

function getAddress(lat, long){

// It will return a string with address
//TODO create function to return address based on lat, and long
// It will be used to show addres in the top of marker

}



//====================================================================================
// End of Code related to geocoding
//====================================================================================

$(document).ready(function() {

    //google.maps.event.addDomListener(window, 'resize', initFavMap);
    // Event to load the map
    google.maps.event.addDomListener(window, 'load', initFavMap);
    // related to materialize library
    $('select').material_select();

    // related to display the infoWindow
    setFalsebooldisplayinfowindow();

});
