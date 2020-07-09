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

document.getElementById("stats_form").style.display = "none"

document.getElementById("y_stats").onclick = function() {
	document.getElementById("stats_form").style.display = "block";
};

document.getElementById("n_stats").onclick = function() {
	document.getElementById("quantity").value = "";
	document.getElementById("opt_gcol").checked = true;
	document.getElementById("opt_glist").checked = false;
	document.getElementById("glist").value = "";
	document.getElementById("gcol").value = "";
	document.getElementById("y_rm").checked = false;
	document.getElementById("n_rm").checked = true;
	document.getElementById("y_nd").checked = true;
	document.getElementById("n_nd").checked = false;
	document.getElementById("stats_form").style.display = "none";
};

document.getElementById("glist").setAttribute("disabled","");

document.getElementById("opt_gcol").onclick = function() {
	document.getElementById("gcol").removeAttribute("disabled");
	document.getElementById("glist").setAttribute("disabled","");
	document.getElementById("glist").value = "";
};

document.getElementById("opt_glist").onclick = function() {
	document.getElementById("gcol").setAttribute("disabled","");
	document.getElementById("gcol").value = "";
	document.getElementById("glist").removeAttribute("disabled");
};
