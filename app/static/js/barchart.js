
var placeholder = $(".barchart");

var data = [
    [0, 1885], //1-Mar
    [1, 2479], //1-Apr
    [2, 2637], //1-May
    [3, 2714], //1-June
    [4, 0],  //1-Jul
    [5,0]   //1-Aug
];
var dataset = [
    { label: "", data: data, color: "#5482FF" }
];

var ticks = [
    [0, "1-Mar"], [1, "1-Apr"], [2, "1-May"], [3, "1-Jun"],
    [4, "1-Jul"], [5, "1-Aug"]
];

var options = {
    series: {
        bars: {
            show: true,
        },

    },
   bars: {
        align: "center",
        lineWidth: 0,
        barWidth: 0.5,
        fillColor: "#2b54ff"
    },
    xaxis: {

        ticks: ticks,
        tickLength:0

    },
    grid:{borderWidth : 0 },

   yaxis:{show:false, tickLength:0},

 }

 $(document).ready(function () {
 //$.plot(placeholder, dataset, options);

    p= $.plot(placeholder, dataset, options);
    $.each(p.getData()[0].data, function(i, el){
        if (el[1] != 0) {
            var o = p.pointOffset({x: el[0], y: el[1]});
            $('<div class="data-point-label">' + el[1] + '</div>').css( {
               position: 'absolute',
               left: o.left - 15,
               top: o.top - 20,
               display: 'none'
               }).appendTo(p.getPlaceholder()).fadeIn('slow');
        }
    });
});