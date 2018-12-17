var myChart = echarts.init(document.getElementById('pieChart1'));
var alarm_data = JSON.parse($("#alarm_data").val());
var useful_data = JSON.parse($("#useful_data").val());

option = {
//    title : {
//        text: '某地区蒸发量和降水量',
//        subtext: '纯属虚构'
//    },
    tooltip : {
        trigger: 'axis'
    },
    legend: {
        data:['报警设备','正常设备'],
        textStyle: {
            color: 'rgba(255, 255, 255, 0.3)'
        }
    },
    toolbox: {
        show : true,
        feature : {
//            dataView : {show: true, readOnly: false},
            magicType : {show: true, type: ['line', 'bar']},
            restore : {show: true},
            saveAsImage : {show: true}
        }
    },
    calculable : true,
    xAxis : [
        {
            type : 'category',
            data : ['1月','2月','3月','4月','5月','6月','7月','8月','9月','10月','11月','12月'],
            axisLine: {
                lineStyle: {
                    color: '#eee'
                }
            }
        }
    ],
    yAxis : [
        {
            type : 'value',
            axisLine: {
                lineStyle: {
                    color: '#eee'
                }
            }
        }
    ],
    series : [
        {
            name:'报警设备',
            type:'bar',
            data:alarm_data,

        },
        {
            name:'正常设备',
            type:'bar',
            data:useful_data,
//            markPoint : {
//                data : [
//                    {name : '年最高', value : 182.2, xAxis: 7, yAxis: 183},
//                    {name : '年最低', value : 2.3, xAxis: 11, yAxis: 3}
//                ]
//            },
//            markLine : {
//                data : [
//                    {type : 'average', name : '平均值'}
//                ]
//            }
        }
    ]
};

myChart.setOption(option);
