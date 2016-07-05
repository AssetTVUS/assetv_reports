// Randomly Generated Data
   $(document).ready(function(){

        var placeholder = $("#piechart-container");
        placeholder.unbind();

		var data = [],
			series = Math.floor(Math.random() * 6) + 3;



        data[0] = {data:32,label:"A"}
        data[1] = {data:32,label:"B"}
        data[2] = {data:12,label:"C"}
        data[3] = {data:9,label:"D"}
        data[4] = {data:5,label:"E"}
        data[5] = {data:9,label:"F"}
        data[6] = {data:1,label:"G"}




			//$("#title").text("Combined Slice");
			//$("#description").text("Multiple slices less than a given percentage (5% in this case) of the pie can be combined into a single, larger slice.");

			$.plot(placeholder, data, {
				series: {
					pie: {
						show: true,
						combine: {
							color: "#999",
							threshold: 0.02
						}
					}
				},
				legend: {
					show: true
				}
			});
	});