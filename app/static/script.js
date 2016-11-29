// When the page is ready
$(document).ready(function(){
    
    // Modal functions used to show the modal windows
    $("#login_modal_btn").click(function(){
        $("#login_modal_form").modal();
        sessionStorage.setItem('modal', 1);        
    });

    $("#register_modal_btn").click(function(){
        $("#register_modal_form").modal();
        sessionStorage.setItem('modal', 2);
    });

    $("#change_profile_picture_btn").click(function(){
    	$("#upload_modal_form").modal();
    });

    $("#delete_account_btn").click(function(){
        $("#delete_account_window").modal();
    });

    autoModal(sessionStorage.getItem('modal'));

    $(".report").click(function(){
        alert("Your report has been submitted !");
    });

    $(".setLocation").click(function(){
        navigator.geolocation.getCurrentPosition(setLocation);
    });

    $('#postText').html("");

    $('#modify').click(function() {
        var password1 = $('#pwd1').val();
        var password2 = $('#pwd2').val();
        if (password1 != password2) {
            alert("The passwords don't match");
        }
    });
});

function setLocation(position) {
    var latlng = new google.maps.LatLng(position.coords.latitude, position.coords.longitude);
    var geocoder = new google.maps.Geocoder();
    geocoder.geocode({ 'latLng': latlng }, function (results, status) {

        // This is checking to see if the Geoeode Status is OK before proceeding
        if (status == google.maps.GeocoderStatus.OK) {
            for (var i = 0; i < results[0].address_components.length; i++) {
                var address = results[0].address_components[i];
                // check if this entry in address_components has a type of country
                if (address.types[0] == 'country')
                  country = address.long_name;
                else if (address.types[0] == ['locality'])       // City
                  city = address.long_name;
            }
            sessionStorage.setItem('location', city + ", " + country);
        }
    });
}

function getLocation() {
    return sessionStorage.getItem('location');
}

function noCache(id) {
    // Append the datetime string to the images path to prevent cache
    var d = new Date();
    var src = $("#" + id).attr('src') + "?" + d.getTime();
    $("#" + id).attr('src', src);
}

function autoModal(modal) {
    if (modal == 1) {
        $("#login_modal_form").modal();
    }

    else if (modal == 2) {
        $("#register_modal_form").modal();
    }
}

// Function used to toogle between the "view" and the "modify" profile 
function toogleView(toogle) {
	if (toogle.checked) {
		$(".view").hide();
		$(".modify").show();
	}
	else {
		$(".modify").hide();
		$(".view").show();		
	}
}

function addPost() {
    var url = '/addPost/' + getLocation() + '/' + $('#postText').val();
    var urlEncoded = encodeURIComponent(url);
    window.location.replace(urlEncoded);
}

function addComment(id) {
    var url = '/addComment/' +  id + '/' + $('#text_' + (id-1)).val();
    alert(id);
    var urlEncoded = encodeURIComponent(url);
    window.location.replace(urlEncoded);
}

function adminRights() {
    if (sessionStorage.getItem('user') != 'admin') {
        alert("You don't have the rights to access this page");
        window.location.replace("/newsfeed");
    }
}


