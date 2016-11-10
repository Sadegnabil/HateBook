$(document).ready(function(){
    $("#login_modal_btn").click(function(){
        $("#login_modal_form").modal();
    });

    $("#register_modal_btn").click(function(){
        $("#register_modal_form").modal();
    });

    $("#change_profile_picture_btn").click(function(){
    	$("#upload_modal_form").modal();
    });

    $("#delete_account_btn").click(function(){
        $("#delete_account_window").modal();
    });


    var d = new Date();
    var src = $(".no-cache-image").attr('src') + "?" + d.getTime();
    $(".no-cache-image").attr('src', src)
});

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



