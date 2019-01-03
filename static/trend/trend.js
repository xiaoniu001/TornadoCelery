
//最近一小时的报警数据websocket
var ws = new WebSocket("ws://rq.cloudwb.cn:5555/recentAlarm");
//var ws = new WebSocket("ws://192.168.108.87:5555/recentAlarm");
ws.onopen = function() {
     var azdwno = $("#azdwno").val();
     console.log("websocket客户端打开连接");
     ws.send(JSON.stringify({"req": "connectReq", "azdwno": azdwno}));
};

ws.onmessage = function (evt) {

    data = JSON.parse(evt.data)
    console.log(data);
    html = "";
    $.each(data.area_alarm_data, function(index, value){
        html+= '<li style="font-size:15px;padding-top:5px">'+
                '<span>'+ value.bjtime + '</span>'+
                '<a class="alarm_device" href="javascript:void(0);" onclick="refresh_map('+value.jingdu +
                ','+value.weidu+
                ')"><span style="color:red">' + value.address+
                '</span></a>'+ "设备异常" +
                '</li>';

    });
    $("#alarm_data").append(html);

};


$('.alarm').liMarquee({
    direction: 'up'
});


//    浏览器刷新或者关闭页面，断开websocket连接
$(window).bind("beforeunload", function(event){
    if(event.clientX>document.body.clientWidth && event.clientY < 0 || event.altKey){
        ws.onclose = function () {
             ws.close();
            console.log("websocket 客户端关闭");
        };
        console.log("刷新页面");

    }else{
        ws.onclose = function () {
            ws.close();
            console.log("websocket 客户端关闭");
        };
        console.log("刷新页面");

    }
});


layui.use('layer', function(){
    var $ = layui.jquery, layer = layui.layer;
    layer.open({
      type: 1,
      title: '报警信息',
      shadeClose: true,
      shade: 0.3,
      maxmin: false, //开启最大化最小化按钮
      area: ['893px', '693px'],
      content: $(".layer_notice"), //iframe的url，no代表不显示滚动条
      end: function(){ //此处用于演示
        console.log("关闭弹窗！");
      }
    });
})

//最近一小时报警数据点击，更新地图坐标
var refresh_map = function (jingdu, weidu){
    console.log(jingdu, weidu);
    map_reload([[weidu, jingdu]]);
};

//})