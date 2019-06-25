function renderChart(labels, values) {
    new Chart(document.getElementById("stats-chart"), {
        type: 'horizontalBar',
        data: {
            labels: labels,
            datasets: [{
                backgroundColor: ["#FF0000", "#FF8C00", "#FFD700", "#ADFF2F", "#20B2AA"],
                data: values
            }
            ]
        },
        options: {
            legend: {display: false},
            title: {
                display: true
            },
            tooltips: {
                callbacks: {
                    label: function (tooltipItem) {
                        return tooltipItem.xLabel.toFixed(2);
                    }
                }
            }
        }
    });
}