$(document).ready(function() {
    $('#get_coordinates').on('click', function() {
        if (navigator.geolocation) {
            navigator.geolocation.getCurrentPosition((position) => {
                $('#id_gps_latitude').val(position.coords.latitude);
                $('#id_gps_longitude').val(position.coords.longitude);
            })
        }
    });
})