$("#login").click(function(){

    layer.open({
      type: 2,
      title: '燃气云用户登录',
      shadeClose: true,
      shade: 0.3,
      maxmin: false, //开启最大化最小化按钮
      area: ['893px', '600px'],
      content: "/login", //iframe的url，no代表不显示滚动条
      end: function(){ //此处用于演示
        console.log("关闭弹窗！");
      }
    });

})