
var markerIndex = 0;
var map;

var data = JSON.parse($("#map_data").val());
console.log("trend地图", data);
var init = function() {

    var Map = qq.maps.Map;
    Marker = qq.maps.Marker;

    var LatLng = qq.maps.LatLng;
    var Event = qq.maps.event;

    var MarkerImage = qq.maps.MarkerImage;
    var MarkerShape = qq.maps.MarkerShape;
    var MarkerAnimation = qq.maps.MarkerAnimation;
    var Point = qq.maps.Point;
    var Size = qq.maps.Size;
    var ALIGN = qq.maps.ALIGN;

    var MVCArray = qq.maps.MVCArray;
    var MarkerCluster = qq.maps.MarkerCluster;
    var Cluster = qq.maps.Cluster;
    var MarkerDecoration = qq.maps.MarkerDecoration;

    var forEach = function (array, fun) {
        for (var i = 0, l = array.length; i < l; ++i) {
            if (fun(array[i], i) === false) {
                return false;
            }
        }
    };

    var latlng = new LatLng(34.12544756511612, 108.984375);
    var options = {
        'zoom':5,
        'center':latlng,
        'mapStyleId': 'style1'

    };

    map = new Map(document.getElementById('tencentMap'), options);

    var markers = new MVCArray();
    markerCluster = new MarkerCluster({
            map:map,
            minimumClusterSize:2, //默认2
            markers:markers,
            zoomOnClick:true, //默认为true
            gridSize:1, //默认60
            averageCenter:true, //默认false
            maxZoom:18, //默认18
        });;

    initCluster = function createCluster() {
        console.log("ddddddd");
        for (var i = 0; i < data.length; i++) {
            var latLng = new LatLng(data[i][0], data[i][1]);
            var decoration = new MarkerDecoration(i, new Point(0, -5));
            var marker = new Marker({
                'position':latLng,
                map:map
            });
            markers.push(marker);
        }

        Event.addListener(markerCluster, 'clusterclick', function (evt) {
            // writeLog("mouse event", eventType);
            var ss =  evt;
            // alert('点击了聚合点');
        });
    };

    initCluster();

    var maker_add;

    function addMarker(index) {
        var latLng = new LatLng(39.849558,116.406893);
        var decoration = new MarkerDecoration(index, new Point(0, -5));
        maker_add = new Marker({
            'position':latLng,
            decoration:decoration,
            map:map
        });
        markers.push(maker_add);

        markerCluster.addMarker(maker_add);
    }

    var markers_add = [];

    function addMarkers() {
        var bounds = map.getBounds();
        var sw = bounds.getSouthWest();
        var ne = bounds.getNorthEast();
        var lngSpan = Math.abs(sw.getLng() - ne.getLng());
        var latSpan = Math.abs(ne.getLat() - sw.getLat());
        for (var i=0; i < 100; i++) {
            var position = new qq.maps.LatLng(ne.getLat() - latSpan*(Math.random()*0.95), sw.getLng() + lngSpan*(Math.random()*0.95));

            var decoration = new MarkerDecoration(i, new Point(0, -5));
            var makeradd = new Marker({
                'position':position,
                decoration:decoration,
                map:map
            });
            markers_add.push(makeradd);
        }

        markerCluster.addMarkers(markers_add);
    }

};

//点击安装单位的表格时，地图重新加载
var map_reload = function(area){
    console.log(area);
    var markers = [];

    map.panTo(new qq.maps.LatLng(area[0][0], area[0][1]));
    map.zoomTo(20);
    map.setOptions()
    markerCluster.clearMarkers();
    for (i in area) {
        var maker = new Marker({
           'position':new qq.maps.LatLng(area[i][0], area[i][1]),
            map:map
        });
        markers.push(maker)
    }
    markerCluster.addMarkers(markers)
};

//加载地图
init();



