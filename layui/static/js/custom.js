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
                    if( data.result =="Error" )
                    {
                        layer.alert(data.message);
                    }else{
                        $(obj).parents("tr").remove();
                        layer.close(index);
                    }
                }
            });
	});
}

function change_pass(url, id) {
    layer.prompt({
        formType: 1,
        title: '输入修改的密码'
        },
        function(value, index, elem){
            $.ajax({
                type: "PUT",
                url: url,
                data: {id: id, password: value},
                dataType: 'json',
                success: function(data){
                    if( data.result =="Error" )
                    {
                        layer.alert(data.message);
                    }else{
                        layer.close(index);
                        layer.msg('修改成功', {time: 1000});
                    }
                }
            });
        }
    );
}


function disable_user(url, id) {
    layer.confirm('禁用用户？', {icon: 3, title:'提示'},
        function(index){
            $.ajax({
                type: "PUT",
                url: url,
                data: {id: id, is_active: false},
                dataType: 'json',
                success: function(data){
                    if( data.result =="Error" )
                    {
                        layer.alert(data.message);
                    }else{
                        layer.close(index);
                        layer.msg('修改成功', {time: 1000});
                    }
                }
            });
    });
}

function enable_user(url, id) {
    layer.confirm('启用用户？', {icon: 3, title:'提示'},
        function(index){
            $.ajax({
                type: "PUT",
                url: url,
                data: {id: id, is_active: true},
                dataType: 'json',
                success: function(data){
                    if( data.result =="Error" )
                    {
                        layer.alert(data.message);
                    }else{
                        layer.close(index);
                        layer.msg('已启用', {time: 1000});
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
                    if( data.result =="Error" )
                    {
                        layer.alert(data.message);
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
                    if( data.result =="Error" )
                    {
                        layer.alert(data.message);
                    }else{
                        layer.close(index);
                        layer.msg('已启用', {time: 1000});
                    }
                }
            });
    });
}