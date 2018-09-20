"use strict"
var init=function(){
    $("#old-inv").attr("disabled",true);
    $("#old-time").attr("disabled",true);
    var date=new Date();
    var str="yyyy/mm/dd";
    str=str.replace(/yyyy|YYYY/,date.getFullYear());
    str=str.replace(/mm|MM/,date.getMonth()+1);
    str=str.replace(/dd|DD/,date.getDate());
    $("#new-time").val("str");
}
init();

$("#save").on("click",function(e){
	e.preventDefault();
	var invitation=$("#new-inv").val();
	var time=$("#new-time").val();
	if(invitation==""||time==""){
		alertInformation("请完善设置");
		return false;
	}
	$.ajax({
        type:"POST",
        url:"/manage/invitation/",
        cache:false,
        data:{
            "invitation":invitation,
            "time": time
        },
        success:function(data){
        	if(data.code == 1) {
				alertInfoWithJump(data.info,"/manage/invitation/");
			}
			else {
                alertInformation(data.info);
            }
        },
        fail: function() {
            alertInformation("数据传输有误");
        },
        error: function(response) {
            alertInformation("网络连接有误");
        }
    });
})
