window.onload = function(){

//直接加载地图


    //初始化地图函数  自定义函数名init
    function init() {
        //定义map变量 调用 qq.maps.Map() 构造函数   获取地图显示容器
         var map = new qq.maps.Map(document.getElementById("mapChart"), {
            center: new qq.maps.LatLng(39.914850, 116.403765),      // 地图的中心地理坐标。
            zoom:5                                                 // 地图的中心地理坐标。
        });
    }

    //调用初始化函数地图
    init();


}