$(document).ready(function()
{
	var ctx = $("#myChart").get(0).getContext("2d");
	
	var data = 
	[
		{
			value: 270,
			color: "cornflowerblue",
			highlight:"lightskyblue",
			label: "JavaScript"
		},
		{
			value: 50,
			color: "lightgreen",
			highlight:"yellowgreen",
			label: "HTML"
		},
		{
			value: 40,
			color: "orange",
			highlight:"darkorange",
			label: "CSS"
		}	
	];
	
	var myNewChart = new Chart(ctx).Doughnut(data);
});