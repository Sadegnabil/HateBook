$(document).ready(function(){
    $("#login_modal_button").click(function(){
        $("#login_modal_form").modal();
    });

    $("#register_modal_button").click(function(){
        $("#register_modal_form").modal();
    });
});

function toogleView(toogle) {
	if (toogle.checked) {
		$("#modify").hide();
		$("#view").show();		
	}
	else {
		$("#view").hide();
		$("#modify").show();
	}
}

