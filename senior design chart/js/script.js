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
				fillColor: "rgba(16,37,63,1)",
				strokeColor: "rgba(16,37,63,1)",
				highlightFill: "rgba(46,107,180,0.75)",
				highlightStroke: "rgba(46,107,180,0.75)",
				data: [0, 0, 0, 0, 0],
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
		labels: ["X", "Y", "Z"],
		datasets:
		[
			{
				label: "IMU Data",
				fillColor: "rgba(16,37,63,1)",
				strokeColor: "rgba(16,37,63,1)",
				highlightFill: "rgba(46,107,180,0.75)",
				highlightStroke: "rgba(46,107,180,0.75)",
				data: [0, 0, 0],
				
			}
		]
	};
	
	// Get context of radar chart for imu sensor
	var ctx = document.getElementById("imuRadarChart").getContext("2d");
	
	// Create the radar chart for the flex sensor
	var imuChart = new Chart(ctx).Radar(imuData);
			
	// ========================================================
	// Letter Received
	// General Canvas
	// ========================================================
	
	
	// Get context of letter canvas
	var canvas = document.getElementById("receivedLetter");
	
	// Create the canvas for the letter
	var ctx = canvas.getContext("2d");
	
	// Style of the letter's canvas
	ctx.fillStyle = "rgb(16,37,63)";
	ctx.font = "300px Times New Roman";
	ctx.textAlign = "center";
	
	
	function randomUpdateData() 
	{		
		$.getJSON("http://192.227.175.138:5000/tony", function(data) 
		{
			/* {"type":"uint8","length":10,"data":[219,40,182,246,138,87,191,247,166,12],"success":true}*/
		
			/*
			var items = [];
			$.each( data, function( key, val ) {
				items.push( "<li id='" + key + "'>" + val + "</li>" );
			});
		 
			$( "<ul/>", {
				"class": "my-new-list",
				html: items.join( "" )
			}).appendTo( "body" );
			*/
			flexChart.datasets[0].bars[0].value = data["thumb_flex"];
			flexChart.datasets[0].bars[1].value = data["index_flex"];
			flexChart.datasets[0].bars[2].value = data["middle_flex"];
			flexChart.datasets[0].bars[3].value = data["ring_flex"];
			flexChart.datasets[0].bars[4].value = data["pinky_flex"];

			imuChart.datasets[0].points[0].value = data["imu_acc_x"];
			imuChart.datasets[0].points[1].value = data["imu_acc_y"];
			imuChart.datasets[0].points[2].value = data["imu_acc_z"];
			
			ctx.clearRect(0, 0, canvas.width, canvas.height);
			ctx.fillText(data["letter"], canvas.width/2, canvas.height/2 + 100);


		});
				
		flexChart.update();
		imuChart.update();
		
		setTimeout(randomUpdateData, 250);
	}
	randomUpdateData();
});