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


    // Append the datetime string to the images path to prevent cache
    var d = new Date();
    var src = $(".no-cache-image").attr('src') + "?" + d.getTime();
    $(".no-cache-image").attr('src', src);
    autoModal(sessionStorage.getItem('modal'));
});


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



