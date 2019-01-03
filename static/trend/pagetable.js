
layui.use('table', function(){
  var table = layui.table;
  var detail_table = layui.table;
  var all_table = layui.table;
  var table_data = JSON.parse($("#area_alarm_data").val());
  var all_data = JSON.parse($("#all_alarm_data").val());
  console.log(all_data);
  $("#real_time").html(all_data.length);
  //展示已知数据
  table.render({
    elem: '#area_alarm'
    ,id: 'dwtable'
    ,height: 350
    ,cols: [[ //标题栏
       {type:'numbers'}
      ,{field: 'count', title: '报警数',sort: true, width: 100}

      ,{field: 'address', title: '地址',align: 'center'}

      ,{field: 'dwno', title: '单位名称',align: 'center'}
    ]]
    ,data: table_data
    ,skin: 'nob' //表格风格
    ,even: false
    ,page: true //是否显示分页

  });

  detail_table.render({
    elem: '#detail_area_alarm'
    ,id: 'areaTable'
    ,height: 300
    ,cols: [[ //标题栏
       {type:'numbers'}
      ,{field: 'imei', title: 'IMEI',align: 'center'}
      ,{field: 'deviceid', title: '设备id',align: 'center'}
      ,{field: 'address', title: '安装位置',align: 'center'}
      ,{field: 'principal', title: '负责人',align: 'center'}
      ,{field: 'installdate', title: '安装时间',align: 'center'}
    ]]
    ,data: []
    ,skin: 'nob' //表格风格
    ,even: false
    ,page: true //是否显示分页

  });

  all_table.render({
    elem: '#all_area_alarm'
    ,id: 'all_area_alarm'
    ,height: 600
    ,layout: ['limit', 'count', 'prev', 'page', 'next', 'skip']
    ,cols: [[ //标题栏
       {type:'numbers'}
      ,{field: 'imei', title: 'IMEI',align: 'center'}
      ,{field: 'deviceid', title: '设备id',align: 'center'}
      ,{field: 'status', title: '报警类型',align: 'center', templet: '#sexTpl'}
      ,{field: 'deviceLocation', title: '设备监控位置',align: 'center'}
      ,{field: 'address', title: '安装位置',align: 'center'}
      ,{field: 'principal', title: '负责人',align: 'center'}
      ,{field: 'installdate', title: '安装时间',align: 'center'}
    ]]
    ,limit: 20
    ,data: all_data
    ,skin: 'nob' //表格风格
    ,even: false
    ,page: true //是否显示分页

  });

  //监听行单击事件
  table.on('row(area_alarm)', function(obj){
    var data = obj.data;

    $.ajax({
        type: "GET",
        url:'/alarmData',
        data:data,
        dataType:'json',
        success:function(data){
            detail_table.reload("areaTable", {
               data: data.area_alarm_data
            });
            map_reload(data.area_data);
            deviceStatusChart.setOption({series : [{data: data.device_status}]});
        }
    })
    obj.tr.addClass('layui-table-click').siblings().removeClass('layui-table-click');
  });

  detail_table.on('row(detail_area_alarm)', function(obj){
    var data = obj.data;
    console.log(data);
    map_reload([[data.weidu, data.jingdu]])
    obj.tr.addClass('layui-table-click').siblings().removeClass('layui-table-click');
  });

  all_table.on('row(all_area_alarm)', function(obj){
    var data = obj.data;
    console.log(data);
    map_reload([[data.weidu, data.jingdu]])
    obj.tr.addClass('layui-table-click').siblings().removeClass('layui-table-click');
  });


});
