
var map;

function initMap() {
        map = new google.maps.Map(document.getElementById('map'), {
          center: {lat: -34.397, lng: 150.644},
          zoom: 8

    });

}

$('#mainInput').submit(function (event) {
    event.preventDefault();
    $.ajax({
          url: 'test-string',
          dataType: 'json',
          cache: false,
          success: function(response) {
          },
          error: function(xhr, status, err) {
          }
    });
})


$('#mainInput').on('click', function (event) {

})
