layui.use(["layer", "datatable"],
function() {
    var n = layui.jquery,
    e = layui.layer;
    n(function() {
        n("#userTable").dataTable({
            language: lang,
            autoWidth: !1,
            lengthMenu: [15, 30, 50],
            stripeClasses: ["odd", "even"],
            searching: !0,
            paging: !0,
            lengthChange: !0,
            info: !0,
            order: [0, "desc"],
            deferRender: !0,
            ajax: "/auth/list",
            columns: [
            {
                data: "id"
            },
            {
                data: function(n) {
                    return '<u class="btn-showuser">' + n.username + "</u>"
                }
            },
            {
                data: "email"
            },
                {
                data: function(n) {
                    return n.is_superuser ? '<span class="label label-success radius">管理员</span>': '<span class="label label-default radius">已停用</span>'
                }
            }, {
                data: function(n) {
                    return n.is_active ? '<span class="label label-success radius">已启用</span>': '<span class="label label-default radius">已停用</span>'
                },
                className: "td-status"
            },
            {
                data: 'date_joined'
            },

            {
                data: function(n) {
                    return n.status ? '<span title="停用" class="handle-btn handle-btn-stop"><i class="linyer icon-zanting"></i></span><span title="编辑" class="handle-btn handle-btn-edit"><i class="linyer icon-edit"></i></span><span title="修改密码" class="handle-btn handle-btn-updatepwd"><i class="linyer icon-xgpwd2"></i></span><span title="删除" class="handle-btn handle-btn-delect"><i class="linyer icon-delect"></i></span>': '<span title="启用" class="handle-btn handle-btn-run"><i class="linyer icon-qiyong"></i></span><span title="编辑" class="handle-btn handle-btn-edit"><i class="linyer icon-edit"></i></span><span title="修改密码" class="handle-btn handle-btn-updatepwd"><i class="linyer icon-xgpwd2"></i></span><span title="删除" class="handle-btn handle-btn-delect"><i class="linyer icon-delect"></i></span>'
                },
                className: "td-handle"
            }]
        });
    // }),
    // n("#userTable").on("click", ".btn-showuser",
    // function() {
    //     var e = n(this).html(),
    //     t = "user-show.html";
    //     layer_show(e, t, "", "400", "500")
    // }),
    // n("#btn-adduser").on("click",
    // function() {
    //     var e = n(this).html(),
    //     t = "user-add.html";
    //     layer_show(e, t, "", "800", "600")
    // }),
    // n("#refresh").on("click",
    // function() {
    //     window.location.reload()
    // }),
    // n(".table-sort").on("click", ".handle-btn-stop",
    // function() {
    //     var t = n(this);
    //     e.confirm("确认要停用吗？", {
    //         icon: 0,
    //         title: "警告",
    //         shade: !1
    //     },
    //     function(a) {
    //         n(t).parents("tr").find(".td-handle").prepend('<span class="handle-btn handle-btn-run" title="启用"><i class="linyer icon-qiyong"></i></span>'),
    //         n(t).parents("tr").find(".td-status").html('<span class="label label-default radius">已停用</span>');
    //         n(t).remove();
    //         e.msg("已停用!", {
    //             icon: 5,
    //             time: 1e3
    //         })
    //     })
    // }),
    // n(".table-sort").on("click", ".handle-btn-run",
    // function() {
    //     var t = n(this);
    //     e.confirm("确认要启用吗？", {
    //         icon: 0,
    //         title: "警告",
    //         shade: !1
    //     },
    //     function(a) {
    //         n(t).parents("tr").find(".td-handle").prepend('<span class="handle-btn handle-btn-stop" title="停用"><i class="linyer icon-zanting"></i></span>'),
    //         n(t).parents("tr").find(".td-status").html('<span class="label label-success radius">已启用</span>');
    //         n(t).remove();
    //         e.msg("已启用!", {
    //             icon: 6,
    //             time: 1e3
    //         })
    //     })
    // }),
    // n(".table-sort").on("click", ".handle-btn-edit",
    // function() {
    //     n(this);
    //     layer_show("编辑", "user-edit.html", "", "800", "600")
    // }),
    // n(".table-sort").on("click", ".handle-btn-updatepwd",
    // function() {
    //     n(this);
    //     layer_show("编辑", "user-updatepwd.html", "", "600", "500")
    // }),
    // n(".table-sort").on("click", ".handle-btn-delect",
    // function() {
    //     var t = n(this);
    //     e.confirm("确认要删除吗？", {
    //         icon: 0,
    //         title: "警告",
    //         shade: !1
    //     },
    //     function(a) {
    //         n(t).parents("tr").remove();
    //         e.msg("已删除!", {
    //             icon: 1,
    //             time: 1e3
    //         })
    //     })
    // });
    // n("#btn-delect-all").on("click",
    // function() {
    //     console.log(n(".table-sort tbody :checkbox:checked").length);
    //     0 == n(".table-sort tbody :checkbox:checked").length ? e.msg("请选择需要删除的数据！", {
    //         icon: 0
    //     }) : e.confirm("确认要删除吗？", {
    //         icon: 0,
    //         title: "警告",
    //         shade: !1
    //     },
    //     function(t) {
    //         n(".table-sort tbody :checkbox:checked").parents("tr").remove();
    //         e.msg("已删除!", {
    //             icon: 1,
    //             time: 1e3
    //         })
    //     })
    })
});