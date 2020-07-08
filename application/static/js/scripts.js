alert("hello");
// Add the following code if you want the name of the file appear on select
$(".custom-file-input").on("change", function () {
	var fileName = $(this).val().split("\\").pop();
	$(this).siblings(".custom-file-label").addClass("selected").html(fileName);
});

if (document.getElementById("#relative_ddCT").checked) {
	document.getElementById("#csample").setAttribute("required","");
} else if (document.getElementById("instability").checked) {
	document.getElementById("#csample").setAttribute("required","");
}

$(document).on("click","#y_stats",function(){
	if ($("y_stats").is(":checked")){
		$("#stats_form").show();
	} else {
		$("#stats_form").hide();
	}
});

if (document.getElementById("#opt_gcol").checked) {
	document.getElementById("#opt_gcol").disabled = false;
	document.getElementById("#opt_glist").disabled = true;

} else {
	document.getElementById("#opt_gcol").disabled = true;
	document.getElementById("#opt_glist").disabled = false;
}

//1