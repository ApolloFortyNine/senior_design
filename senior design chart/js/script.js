$(document).ready(function()
{	
	// ========================================================
	// Flex Sensors
	// Bar Graph
	// ========================================================
		
	var flexData = 
	{
		labels: ["Thumb", "Index", "Middle", "Ring", "Pinky"],
		datasets: 
		[
			{
				label: "Flex Sensors",
				fillColor: "rgba(16,37,63,0.75)",
				strokeColor: "rgba(16,37,63,0.75)",
				highlightFill: "rgba(46,107,180,0.75)",
				highlightStroke: "rgba(46,107,180,0.75)",
				data: [0.36, 0.69, 0.80, 0.81, 0.56],
			}
		]
	};
	
	// Get context of bar chart for flex sensors
	var ctx = document.getElementById("flexBarChart").getContext("2d");

	// Create the bar chart for the flex sensors
	var flexChart = new Chart(ctx).Bar(flexData);
	
	// ========================================================
	// IMU Sensor
	// Radar Graph
	// ========================================================
	
	var imuData =
	{
		labels: ["Up", "Right", "Down", "Left"],
		datasets:
		[
			{
				label: "Flex Sensors",
				fillColor: "rgba(16,37,63,0.75)",
				strokeColor: "rgba(16,37,63,0.75)",
				highlightFill: "rgba(46,107,180,0.75)",
				highlightStroke: "rgba(46,107,180,0.75)",
				data: [0.80, 0.49, 0.51, 0.23],
				
			}
		]
	};
	
	// Get context of radar chart for imu sensor
	var ctx = document.getElementById("imuRadarChart").getContext("2d");
	
	// Create the radar chart for the flex sensor
	var imuChart = new Chart(ctx).Radar(imuData);
});