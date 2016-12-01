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


    // Check if a modal window was previously opened and check which one was open
    autoModal(sessionStorage.getItem('modal'));


    // When a user clicks on the report button display an alert
    $(".report").click(function(){
        alert("Your report has been submitted !");
    });


    // Retrieve the location when the user clicks on the New Post button
    $(".setLocation").click(function(){
        navigator.geolocation.getCurrentPosition(setLocation);
    });


    // Reset the postText field
    $('#postText').html("");


    // Check if the passwords are matching when the user wants to change his/her password
    $('#modify').click(function() {
        var password1 = $('#pwd1').val();
        var password2 = $('#pwd2').val();
        if (password1 != password2) {
            alert("The passwords don't match");
        }
    });
});


// Set the location of the user
function setLocation(position) {

    // Get the coordinates
    var latlng = new google.maps.LatLng(position.coords.latitude, position.coords.longitude);

    // Create a geocoder
    var geocoder = new google.maps.Geocoder();
    geocoder.geocode({ 'latLng': latlng }, function (results, status) {

        // Check if the Geocoder is OK
        if (status == google.maps.GeocoderStatus.OK) {
            for (var i = 0; i < results[0].address_components.length; i++) {
                var address = results[0].address_components[i];

                // check if this entry is the country
                if (address.types[0] == 'country')
                  country = address.long_name;

                // check if this entry is the locality/city
                else if (address.types[0] == ['locality'])
                  city = address.long_name;
            }

            // Save the location
            sessionStorage.setItem('location', city + ", " + country);
        }
    });
}


// Get the location of the user
function getLocation() {
    return sessionStorage.getItem('location');
}


// Prevent image cachin by adding the time to the image name
function noCache(id) {
    // Append the datetime string to the images path to prevent cache
    var d = new Date();
    var src = $("#" + id).attr('src') + "?" + d.getTime();
    $("#" + id).attr('src', src);
}


// Switch the modality according to which modal window was previously open
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


// Function used to add a post
function addPost() {
    // Create the url to create the post and retrieve the text
    var url = '/addPost/' + getLocation() + '/' + $('#postText').val();
    var urlEncoded = encodeURIComponent(url);

    // Use the url to create the post
    window.location.replace(urlEncoded);
}


// Function used to add a comment
function addComment(id) {
    // Create the url to create the comment and retrieve the text
    var url = '/addComment/' +  id + '/' + $('#text_' + (id-1)).val();
    var urlEncoded = encodeURIComponent(url);

     // Use the url to create the comment
    window.location.replace(urlEncoded);
}


// Check if the user has admin rights to access the admin page
function adminRights() {

    // If he doesn't have the rights send it back to the newsfeed page
    if (sessionStorage.getItem('user') != 'admin') {
        alert("You don't have the rights to access this page");
        window.location.replace("/newsfeed");
    }
}


