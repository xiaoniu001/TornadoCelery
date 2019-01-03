var deviceStatusChart = echarts.init(document.getElementById('deviceStatus'));
var statusData = JSON.parse($("#device_status").val());
console.log(statusData);
deviceStatusOption = {
    title: {
        text: '设备状态统计',
//        subtext: '虚构数据',
        left: 'center'
    },
    tooltip : {
        trigger: 'item',
        formatter: "{b} : {c} ({d}%)"
    },
    legend: {
        // orient: 'vertical',
        // top: 'middle',
        bottom: 10,
        left: 'center',
        data: ['正常', '报警','关机','失效','故障']
    },
    series : [
        {
            type: 'pie',
            radius : '65%',
            center: ['50%', '50%'],
            selectedMode: 'single',
            data: statusData,
            itemStyle: {
                emphasis: {
                    shadowBlur: 10,
                    shadowOffsetX: 0,
                    shadowColor: 'rgba(0, 0, 0, 0.5)'
                }
            }
        }
    ]
};

deviceStatusChart.setOption(deviceStatusOption);