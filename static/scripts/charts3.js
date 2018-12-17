var Chart3 = echarts.init(document.getElementById('pieChart3'));
var alarm_data = JSON.parse($("#alarm_data").val());
var alarm_solution = JSON.parse($("#alarm_solution").val());
option = {
    xAxis: {
        type: 'category',
        data: ['1月','2月','3月','4月','5月','6月','7月','8月','9月','10月','11月','12月'],
        axisLine: {
            lineStyle: {
                color: '#eee'
            }
        }
    },
    yAxis: {
        type: 'value',
        axisLine: {
            lineStyle: {
                color: '#eee'
            }
        }
    },
    tooltip : {
        trigger: 'axis'
    },
    legend: {
        data:['报警数','报警处置'],
        textStyle: {
            color: 'rgba(255, 255, 255, 0.3)'
        }
    },
    series: [{
        name: "报警数",
        data: alarm_data,
        type: 'line'

    },
    {
        name: "报警处置",
        data: alarm_solution,
        type: 'line'
    }
    ]
};
Chart3.setOption(option);