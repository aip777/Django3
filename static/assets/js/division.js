var options = {
        series: [{
            name: 'Infected',

            data: [20065, 30205, 42844, 63026, 84379, 108775, 133978, 153277, null, null, null, null]
        }, {
            name: 'Forcast',
            data: [null, null, null, null, null, null, null, 153277, 154644, 163149, 170090, 172394]
        }],
        chart: {
            height: 350,
            type: 'line',
            zoom: {
                enabled: false
            },
            animations: {
                enabled: false
            },
            toolbar: {
          show: false,
          offsetX: 0,
        },
        },
        colors: ["#ddccdd", "#FF0000"],
        stroke: {
            width: [5, 5, 4],
            curve: 'straight'
        },
        labels: ['15May', 22, 29, '6Jun', 13, 20, 27, '2Jul', 5, 8, 11, 12],
        title: {
            text: 'Focasting base on previous data'
        },
        xaxis: {},
    };

    var chart = new ApexCharts(document.querySelector("#division"), options);
    chart.render();