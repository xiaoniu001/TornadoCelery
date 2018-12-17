var Chart2 = echarts.init(document.getElementById('pieChart2'));
var brand_data = JSON.parse($("#brand_alarm").val());

function series(data, itemStyle){
    console.log(data);
    var arr_data = [];
    var keys = []
    for(var i in data){
        var dic = {};
        keys.push(i);
        dic["name"] = i;
        dic["type"] = 'scatter',
        dic["itemStyle"] = itemStyle,
        dic["data"] = data[i]
        arr_data.push(dic)
    }
    arr_data.push(keys);
    console.log(arr_data);
    return arr_data;

};


//var dataBJ = [
//    [1,55,9,56,0.46,18,6,"良"],
//    [2,25,11,21,0.65,34,9,"优"],
//    [3,56,7,63,0.3,14,5,"良"],
//    [4,33,7,29,0.33,16,6,"优"],
//    [5,42,24,44,0.76,40,16,"优"],
//    [6,82,58,90,1.77,68,33,"良"],
//    [7,74,49,77,1.46,48,27,"良"],
//    [8,78,55,80,1.29,59,29,"良"],
//    [9,267,216,280,4.8,108,64,"重度污染"],
//    [10,185,127,216,2.52,61,27,"中度污染"],
//    [11,39,19,38,0.57,31,15,"优"],
//    [12,41,11,40,0.43,21,7,"优"]
//];
//
//
//var dataGZ = [
//    [1,26,37,27,1.163,27,13,"优"],
//    [2,85,62,71,1.195,60,8,"良"],
//    [3,78,38,74,1.363,37,7,"良"],
//    [4,21,21,36,0.634,40,9,"优"],
//    [5,41,42,46,0.915,81,13,"优"],
//    [6,56,52,69,1.067,92,16,"良"],
//    [7,64,30,28,0.924,51,2,"良"],
//    [8,55,48,74,1.236,75,26,"良"],
//    [9,76,85,113,1.237,114,27,"良"],
//    [10,91,81,104,1.041,56,40,"良"],
//    [11,84,39,60,0.964,25,11,"良"],
//    [12,64,51,101,0.862,58,23,"良"]
//];
//
//var dataSH = [
//    [1,91,45,125,0.82,34,23,"良"],
//    [2,65,27,78,0.86,45,29,"良"],
//    [3,83,60,84,1.09,73,27,"良"],
//    [4,109,81,121,1.28,68,51,"轻度污染"],
//    [5,106,77,114,1.07,55,51,"轻度污染"],
//    [6,109,81,121,1.28,68,51,"轻度污染"],
//    [7,106,77,114,1.07,55,51,"轻度污染"],
//    [8,89,65,78,0.86,51,26,"良"],
//    [9,53,33,47,0.64,50,17,"良"],
//    [10,80,55,80,1.01,75,24,"良"],
//    [11,117,81,124,1.03,45,24,"轻度污染"],
//    [12,99,71,142,1.1,62,42,"良"]
//];

var schema = [
    {name: 'date', index: 0, text: '日'},
    {name: 'waring', index: 1, text: '报警数量'},
    {name: 'solution', index: 2, text: '正常数量'},
    {name: 'error', index: 3, text: '失效数量'},
    {name: 'close', index: 4, text: '关机数量'},
    {name: 'break', index: 5, text: '故障数量'},

];


var itemStyle = {
    normal: {
        opacity: 0.8,
        shadowBlur: 10,
        shadowOffsetX: 0,
        shadowOffsetY: 0,
        shadowColor: 'rgba(0, 0, 0, 0.5)'
    }
};


var mydata = series(brand_data, itemStyle);
option = {
    backgroundColor: "rgb(8, 24, 50)",
//    color: [
//        '#dd4444', '#fec42c', '#80F1BE'
//    ],
    legend: {
        y: 'top',
        data: mydata[mydata.length-1],
        textStyle: {
            color: '#fff',
            fontSize: 16
        }
    },
    grid: {
        x: '10%',
        x2: 60,
        y: '18%',
        y2: '8%'
    },
    tooltip: {
        padding: 10,
        backgroundColor: '#222',
        borderColor: '#777',
        borderWidth: 1,
        formatter: function (obj) {
            var value = obj.value;
            return '<div style="border-bottom: 1px solid rgba(255,255,255,.3); font-size: 18px;padding-bottom: 7px;margin-bottom: 7px">'
                + obj.seriesName + schema[0].text + '：' + value[0]+"月" + '<br>'
                + '</div>'
                + schema[1].text + '：' + value[1] + '<br>'
                + schema[2].text + '：' + value[2] + '<br>'
                + schema[3].text + '：' + value[3] + '<br>'
                + schema[4].text + '：' + value[4] + '<br>'
                + schema[5].text + '：' + value[5] + '<br>'

        }
    },
    xAxis: {
        type: 'value',
        name: '月份',
        nameGap: 16,
        nameTextStyle: {
            color: '#fff',
            fontSize: 14
        },
        max: 12,
        splitLine: {
            show: false
        },
        axisLine: {
            lineStyle: {
                color: '#eee'
            }
        }
    },
    yAxis: {
        type: 'value',
        name: '报警数量',
        nameLocation: 'end',
        nameGap: 20,
        nameTextStyle: {
            color: '#fff',
            fontSize: 16
        },
        axisLine: {
            lineStyle: {
                color: '#eee'
            }
        },
        splitLine: {
            show: false
        }
    },
    series: mydata.slice(0,-1)
//    [
//        {
//            name: '品牌a',
//            type: 'scatter',
//            itemStyle: itemStyle,
//            data: dataBJ
//        },
//        {
//            name: '品牌b',
//            type: 'scatter',
//            itemStyle: itemStyle,
//            data: dataSH
//        },
//        {
//            name: '品牌c',
//            type: 'scatter',
//            itemStyle: itemStyle,
//            data: dataGZ
//        }
//    ]
};
Chart2.setOption(option);

