// Call the dataTables jQuery plugin
// $(document).ready(function() {
//   $('#dataTable').DataTable();
// });
$(document).ready(function() {
  $("#dataTable").DataTable({
    "destroy": true,//消除重定义出错
    "lengthChange":true,
    "bPaginate": true,//是否使用分页
    "lengthMenu": [[10, 20, 25, -1], [10, 20, 25, "所有"]],
    "bStateSave":false,
    "iDisplayLength":20,
    "bFilter": true, //是否使用搜索
    "sInfo": true,
    "bAutoWidth": true,
    "serverSide": false,
    "oLanguage": {
      "sLengthMenu": "每页显示 _MENU_ 条记录",
      "sInfo": "显示 _START_ 至 _END_ 条 &nbsp;&nbsp;本页共 _TOTAL_ 条",
      "sSearch" : "查询",
      "oPaginate": {
        "sFirst" : "第一页",
        "sPrevious" : "上一页",
        "sNext" : "下一页",
        "sLast" : "最后一页"
      },
    },
  });

});