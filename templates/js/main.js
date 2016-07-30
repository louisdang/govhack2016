
var map;

var appState = {
    isDropping: false
}

var initMap = function () {
    map = new google.maps.Map(document.getElementById('map'), {
      center: {lat: -34.397, lng: 150.644},
      zoom: 8
    });
}

var getSchools = function () {
    return [
        {
            school: 'Killara High School',
            capacity: 400,
            lat: -33.860427,
            long: 151.204871,
        },
        {
            school: 'Hornsby Girls' ,
            capacity: 400,
            lat: -33.860863,
            long: 151.204832,
        },
        {
            school: 'North Sydney Boys' ,
            capacity: 400,
            lat: -33.863407,
            long: 151.21408,
        },
    ]
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


$('#mainInput').submit(function (e) {

    e.preventDefault();
    var formValue = $('#inputContent').val();

    // $.ajax({
    //       url: 'test-string',
    //       dataType: 'json',
    //       cache: false,
    //       success: function(response) {
    //       },
    //       error: function(xhr, status, err) {
    //       }
    // });

    // on submit draw pointers

    // jsonData


    var schools = getSchools();

    showSchoolsOnMap(schools);

    navigateTo(formValue + ' Australia');

})

$('#addSite').on('click', function(e) {

    appState.isDropping = appState.isDropping ? false : true;

    if ( appState.isDropping ) {

    }


})
