document.addEventListener("DOMContentLoaded", function () {
    const chart = $(".flot-chart");
    const ajaxUrl = chart.data("ajax-url");

    $.ajax({
        url: ajaxUrl,
        method: "GET",
        dataType: "json",
        success: function (response) {
            $.plot(chart, response, {
                series: { lines: { show: true }, points: { show: true } },
                xaxis: { 
                    ticks: [
                        [1, "20~24세"], [2, "25~29세"], [3, "30~34세"], [4, "35~39세"],
                        [5, "40~44세"], [6, "45~49세"], [7, "50~54세"], [8, "55~59세"],
                        [9, "60~64세"], [10, "65~69세"], [11, "70~74세"], [12, "75~79세"],
                        [13, "80~84세"], [14, "85세+"]
                    ],
                    axisLabel: "연령대",
                },
                yaxis: {
                    min: 0,
                    max: 100,
                    axisLabel: "비율 (%)"
                },
                grid: { borderColor: chart.data("flot-border-color") },
                legend: { show: chart.data("flot-legend-show") },
            });
        },
        error: function () {
            console.error("Error loading chart data");
        },
    });
});
