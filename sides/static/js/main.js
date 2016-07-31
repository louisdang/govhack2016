
var map;

var appState = {
    isDropping: false,
    evacSites: [],
    currentSiteCapacity: null,
}

var getSchools = function () {
    return [
        {
            id: 0,
            school: 'Killara High School',
            capacity: 400,
            lat: -33.860427,
            long: 151.204871,
        },
        {
            id: 1,
            school: 'Hornsby Girls' ,
            capacity: 400,
            lat: -33.860863,
            long: 151.204832,
        },
        {
            id: 2,
            school: 'North Sydney Boys' ,
            capacity: 400,
            lat: -33.863407,
            long: 151.21408,
        },
    ]
}

var getResults = function () {
    var results = [{'dst': {'id': 'Adamstown Public School',
   'lat': -32.932213,
   'lng': 151.730971,
   'num_students': 235},
  'src': {'id': 'Abbotsford Public School',
   'lat': -33.852728,
   'lng': 151.131206,
   'num_students': 589},
  'value': 0.0},
 {'dst': {'id': 'Adelong Public School',
   'lat': -35.312333,
   'lng': 148.062802,
   'num_students': 76},
  'src': {'id': 'Abbotsford Public School',
   'lat': -33.852728,
   'lng': 151.131206,
   'num_students': 589},
  'value': 76.0},
 {'dst': {'id': 'Albion Park Public School',
   'lat': -34.570257,
   'lng': 150.77262,
   'num_students': 425},
  'src': {'id': 'Abbotsford Public School',
   'lat': -33.852728,
   'lng': 151.131206,
   'num_students': 589},
  'value': 425.0},
 {'dst': {'id': 'Albury Public School',
   'lat': -36.082454,
   'lng': 146.919253,
   'num_students': 593},
  'src': {'id': 'Abbotsford Public School',
   'lat': -33.852728,
   'lng': 151.131206,
   'num_students': 589},
  'value': 88.0}]

  return results;
}

var showSchoolsOnMap = function (schools) {
    schools.forEach(function(school) {
        var marker = new google.maps.Marker({
         position: { lat: school.lat, lng: school.long },
         map: map,
         title: 'Hello World!'
       });
    })
}

var displayRoute = function (directionsDisplay, directionsService, map, route) {
    directionsService.route({
      origin: {lat: route.src.lat, lng: route.src.lng},
      destination: { lat: route.dst.lat, lng: route.dst.lng },
      travelMode: 'WALKING'
    }, function(response, status) {
      // Route the directions and pass the response to a function to create
      // markers for each step.
      if (status === 'OK') {
        directionsDisplay.setDirections(response);
      } else {
        window.alert('Directions request failed due to ' + status);
      }
    });
}

var showSitesOnMap = function (results) {

    // initialise a directionService


    results.forEach(function(result) {

        var srcMarker = new google.maps.Marker({
             position: { lat: result.src.lat, lng: result.src.lng },
             map: map,
        });
        var directionsService = new google.maps.DirectionsService;
        var directionsDisplay = new google.maps.DirectionsRenderer({map: map});
        displayRoute(directionsDisplay, directionsService, map, result);

       // initialiseRenderer

       var dstMarker = new google.maps.Marker({
           position: { lat: result.dst.lat, lng: result.dst.lng },
           map: map,
       })

    })
}

var navigateTo = function (positionString) {
    var geocoder = new google.maps.Geocoder();
    geocodeAddress(geocoder, map, positionString);
}

var geocodeAddress = function (geocoder, resultsMap, positionString) {
      geocoder.geocode({'address': positionString}, function(results, status) {
        if (status === 'OK') {
          resultsMap.setCenter(results[0].geometry.location);
          resultsMap.setZoom(14);
          var marker = new google.maps.Marker({
            map: resultsMap,
            position: results[0].geometry.location
          });
        } else {
          alert('Geocode was not successful for the following reason: ' + status);
        }
      });
}

var addEvacSite = function (latLng, map) {
    var marker = new google.maps.Marker({
        position: latLng,
        map: map
    });
    marker.meta = {
        type: 'evac',
        id: appState.evacSites.length,
        capacity: appState.currentSiteCapacity
    }
    appState.evacSites.push(marker);
    appState.currentSiteCapacity = null;
    $('#siteCapacity').val('')
}

var mapEvacSites = function (sites) {
    return sites.map(function(site){
        return {
            id: site.meta.id,
            lat: site.position.lat(),
            lng:  site.position.lng(),
            num_students: site.meta.capacity,
        }
    })
}

var mapSchools = function (schools) {
    return schools.map(function (school) {
        return {
            id: school.id,
            lat: school.lat,
            lng: school.long,
            num_students: school.capacity
        }
    })
}

var getSchoolsAndSites = function () {
    // get evac on map
    // get schools on map
}

var addMapListeners = function (map) {
    map.addListener('click', function (e) {
        console.log(e.latLng.lat(), e.latLng.lng());
        if (!appState.isDropping) return;
        addEvacSite(e.latLng, map);
    })
}

var initMap = function () {
    map = new google.maps.Map(document.getElementById('map'), {
      center: {lat: -34.397, lng: 150.644},
      zoom: 8
    });
    addMapListeners(map);
}


$('#mainInput').submit(function (e) {
    e.preventDefault();
    var formValue = $('#inputContent').val();
	
	console.log(formValue)
	
     // $.ajax({
     //      url: '/search_postcode/?postcode=' + formValue,
     //      dataType: 'json',
     //      cache: false,
     //      success: function(response) {
	 //		   console.log(response)
     //      },
     //      error: function(xhr, status, err) {
	 //		   console.log(status)
     //     }
     //});
	 $.get('/search_postcode/?postcode=' + formValue, function(response){
		 console.log(response);
	 })
	 
	
	

    // on submit draw pointers

    // jsonDatas

    var schools = getSchools();
    showSchoolsOnMap(schools);
    navigateTo(formValue + ' Australia');
})

$('#addSite').on('click', function(e) {

    appState.isDropping = appState.isDropping ? false : true;
    if ( appState.isDropping ) {
        $('#addSite').val('Dropping');
        $('#siteCapacity').css('display', 'inline-block');
    } else {
        $('#addSite').val('Add evac site');
        $('#siteCapacity').css('display', 'none');
    }

})

$('#siteCapacity').on('keyup', function(e) {
    appState.currentSiteCapacity = e.currentTarget.value;
})

$('#run').on('click', function(e) {
    // var schools = getSchools();
    var sites = mapEvacSites(appState.evacSites);
    var schools = mapSchools(getSchools());

    var data = { sources: schools, destinations: sites }

    $.ajax({
        type: "POST",
        url: 'http://ec2-54-206-103-17.ap-southeast-2.compute.amazonaws.com/get_optimized_results',
        data: data,
        dataType: 'json',
        success: function (res) {
            console.log('success')
            console.log(res)
        },
        error: function (err) {
            console.log('err')
            console.log(err)
        }
    });

    // debugger;

})

$('#test').on('click', function(e) {
    showSitesOnMap(getResults());
})
