/**
 * Created by mu77 on 2016/12/12.
 */
function data_delete(obj, url) {
	layer.confirm('确认要删除么?', {icon: 3, title:'提示'},
		function(index){
			$.ajax({
                type: "DELETE",
                url: url,
                success: function(data){
                    if( data.result =="failure" )
                    {
                        layer.alert(data.code);
                    }else{
                        $(obj).parents("tr").remove();
                        layer.close(index);
                        layer.msg('已删除');

                    }
                }
            });
	});
}

function change_pass(obj, url) {
    layer.prompt({
        formType: 1,
        title: '输入修改的密码'
        },
        function(value, index, elem){
            $.ajax({
                type: "PUT",
                url: url,
                data: {password: value},
                dataType: 'json',
                success: function(data){
                    if( data.result =="failure" )
                    {
                        layer.alert(data.code);
                    }else{
                        layer.close(index);
                        layer.msg('修改成功', {time: 1000});
                    }
                }
            });
        }
    );
}


function disable_user(obj, url) {
    layer.confirm('禁用用户？', {icon: 3, title:'提示'},
        function(index){
            $.ajax({
                type: "PUT",
                url: url,
                data: {is_active: false},
                dataType: 'json',
                success: function(data){
                    if( data.result =="failure" )
                    {
                        layer.alert(data.code);
                    }else{
                        layer.close(index);
                        location.reload()
                    }
                }
            });
    });
}

function enable_user(obj, url) {
    layer.confirm('启用用户？', {icon: 3, title:'提示'},
        function(index){
            $.ajax({
                type: "PUT",
                url: url,
                data: {is_active: true},
                dataType: 'json',
                success: function(data){
                    if( data.result =="failure" )
                    {
                        layer.alert(data.code);
                    }else{
                        layer.close(index);
                        location.reload()
                    }
                }
            });
    });
}

function container_start(url, id) {
    layer.confirm('确认开启？', {icon: 3, title:'提示'},
        function(index){
            $.ajax({
                type: "PUT",
                url: url,
                data: {id: id, option: 'start'},
                dataType: 'json',
                success: function(data){
                    if( data.result =="failure" )
                    {
                        layer.alert(data.code);
                    }else{
                        layer.close(index);
                        layer.msg('已启用', {time: 1000});
                    }
                }
            });
    });
}

function container_stop(url, id) {
    layer.confirm('确认关闭？', {icon: 3, title:'提示'},
        function(index){
            $.ajax({
                type: "PUT",
                url: url,
                data: {id: id, option: 'stop'},
                dataType: 'json',
                success: function(data){
                    if( data.result =="failure" )
                    {
                        layer.alert(data.code);
                    }else{
                        layer.close(index);
                        layer.msg('已停用', {time: 1000});
                    }
                }
            });
    });
}

function logout() {
	layer.confirm('确认要注销么?', {icon: 3, title:'提示'},
		function(index){
			location.href='/logout';
	});
}

function form_show(e, n, t, a, s) {
    null != e && "" != e || (e = !1),
    null != a && "" != a || (a = 800),
    null != s && "" != s || (s = $(window).height() - 300),
    layer.open({
        type: 2,
        area: [a + "px", s + "px"],
        fix: !1,
        maxmin: !0,
        shade: !1,
        title: e,
        content: n
    })
}

