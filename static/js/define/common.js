function layerMsg(e, n) {
    layer.msg(e, {
        icon: n,
        time: 1e3
    })
}
function layer_show(e, n, t, a, s) {
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
function layer_close() {
    var e = parent.layer.getFrameIndex(window.name);
    parent.layer.close(e)
}
function replaceTime(e) {
    return new Date(1e3 * parseInt(e)).toLocaleString().replace(/:\d{1,2}$/, " ")
}
layui.config({
    base: "/static/lib/"
}).extend({
    datatable: "datatable"
}),
layui.use(["element", "layer"],
function() {
    var e = layui.jquery;
    layui.layer,
    layui.element();
    e(function() {
        e(".table-sort").on("click", ".btn-checkall",
        function() {
            e(".btn-checkall").prop("checked", this.checked),
            e('[type="checkbox"][name="sublist"]').prop("checked", this.checked)
        }),
        e(".table-sort").on("click", '[type="checkbox"][name="sublist"]',
        function() {
            e(".btn-checkall").prop("checked", e('[type="checkbox"][name="sublist"]').length == e('[type="checkbox"][name="sublist"]:checked').length)
        })
    })
});
var lang = {
    sProcessing: "处理中...",
    sLengthMenu: "每页 _MENU_ 项",
    sZeroRecords: "没有匹配结果",
    sInfo: "当前显示第 _START_ 至 _END_ 项，共 _TOTAL_ 项。",
    sInfoEmpty: "当前显示第 0 至 0 项，共 0 项",
    sInfoFiltered: "(由 _MAX_ 项结果过滤)",
    sInfoPostFix: "",
    sSearch: "本地搜索：",
    sUrl: "",
    sEmptyTable: "暂无数据",
    sLoadingRecords: "载入中...",
    sInfoThousands: ",",
    oPaginate: {
        sFirst: "首页",
        sPrevious: "上页",
        sNext: "下页",
        sLast: "末页",
        sJump: "跳转"
    },
    oAria: {
        sSortAscending: ": 以升序排列此列",
        sSortDescending: ": 以降序排列此列"
    }
};
