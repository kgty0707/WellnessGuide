$(function () {
    const chart = $(".flot-chart");
    const ajaxUrl = chart.data("ajax-url");
    const ticks = JSON.parse(chart.attr("data-flot-ticks"));

    $.ajax({
        url: ajaxUrl,
        method: "GET",
        dataType: "json",
        success: function (response) {
            $.plot(chart, response, {
                series: { lines: { show: true }, points: { show: true } },
                xaxis: { ticks: ticks },
                grid: { borderColor: chart.data("flot-border-color") },
                legend: { show: chart.data("flot-legend-show") },
            });
        },
        error: function () {
            console.error("Error loading chart data");
        },
    });
});