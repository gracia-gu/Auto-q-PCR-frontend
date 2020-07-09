// Add the following code if you want the name of the file appear on select
document.querySelector(".custom-file-input").addEventListener("change",function(e){
	$(this).next(".custom-file-label").html(e.target.files.length + " files uploaded");
});

document.getElementById("relative_ddCT").onclick = function() {
	document.getElementById("csample").setAttribute("required","");
};

document.getElementById("instability").onclick = function() {
	document.getElementById("csample").setAttribute("required","");
};

document.getElementById("y_stats").onclick = function() {
	alert("hello")
	// if ($("y_stats").is(":checked")){
	// 	$("#stats_form").show();
	// } else {
	// 	$("#stats_form").hide();
	// }
};

// $(document).on("click","#y_stats",function(){
// 	alert("hello")
// 	if ($("y_stats").is(":checked")){
// 		$("#stats_form").show();
// 	} else {
// 		$("#stats_form").hide();
// 	}
// });

document.getElementById("glist").setAttribute("disabled","");

document.getElementById("opt_gcol").onclick = function() {
	document.getElementById("gcol").removeAttribute("disabled");
	document.getElementById("glist").setAttribute("disabled","");
};

document.getElementById("opt_glist").onclick = function() {
	document.getElementById("gcol").setAttribute("disabled","");
	document.getElementById("glist").removeAttribute("disabled");
};
