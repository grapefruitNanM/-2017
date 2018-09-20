(function(){
	// $("#contactUs").click(function(){
	// 	// $("#model-email").css("display","block");
	// 	// // $("#model .model-container").css("top","25%");
	// 	// $("#model-email .model-container").css("opacity",1);
	// })
	// $("#model-email .model-container .fa-close").click(function(){
	// 	$("#model-email").css("display","none");
	// 	var input=$("#model-email .model-body input");
	// 	var i=input.length;
 //        for(var n=0;n<i-1;n++){
 //            input[n].value='';
 //            $("#model-email .model-body i").css("opacity",0);
 //        }
	// })

})();
var cfm='';
function checkFromMail(node) {
    var tip = document.getElementById("check-from-mail");
    var mail = node.value;
    if( ! isEmail(mail) ){
    	tip.style.color="red";
    	tip.style.opacity=1;
    	tip.className="check fa fa-close";
    	cfm=false;
    	return false;
    }
    else{
    	// tip.className="check fa";
    	tip.style.opacity=0;
    	cfm=true;
    }
}

$("#send").click(function(e){
	e.preventDefault();
	$("#model-alertInfo span.model-title").html("联系我们");
	var content=$("from-content").val();
	if(cfm!=true||content==''){
		alertInformation("请完善表单");
		return false;
	}
	var from=$("#from-mail").val();
	var sender=$("#from-name").val();
	var content=$("#from-content").val();
	$.ajax({
        type:"POST",
        url:"/index/emailSend/",
        // async:false,
        cache:false,
        data:{
            "from": from,
            "sender": sender,
            "content":content
        },
        success:function(data){
        	if(data.code == 1) {
				alertInfoWithJump(data.info,"/index/");
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
});
