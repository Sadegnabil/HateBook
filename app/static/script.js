$(document).ready(function(){
    $("#login_modal_button").click(function(){
        $("#login_modal_form").modal();
    });

    $("#register_modal_button").click(function(){
        $("#register_modal_form").modal();
    });

    $("#change_profile_picture_btn").click(function(){
    	$("#upload_modal_form").modal();
    });
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

