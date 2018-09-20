// "use strict";
// var cp='',cf='',ca='',cpre='',cm='';


//     function checkPsw(node) {
//         var tip = document.getElementById("checkNewCode");
//         var pwd = node.value;
//         console.log(pwd);
//         if(pwd==""){
//             tip.style.opacity='0';
//             cp=false;
//             if(conf!=""){
//                 confirmPsw(document.getElementById("cf-psw"));
//             }
//             return false;
//         }
//         else{
//             cp=true;
//             tip.style.opacity='1';
//             tip.className="fa fa-check check";
//         }
//     }

//     function isEmail(strEmail) {
//         if (strEmail.search(/^[A-Za-z\d]+([-_.][A-Za-z\d]+)*@(163.)+[A-Za-z\d]{2,4}$/) != -1 || strEmail.search(/^[A-Za-z\d]+([-_.][A-Za-z\d]+)*@(qq.)+[A-Za-z\d]{2,4}$/) != -1)
//             return true;
//         else
//             return false;
//     }

//     function checkEmail(node) {
//         var tip = document.getElementById("checkNewMail");
//         var mail = node.value;
//         if( ! isEmail(mail) ){
//             tip.style.opacity='1';
//             tip.className="check fa fa-close";
//             tip.getElementsByTagName("span")[0].innerHTML = "邮箱格式不正确";
//             cm=false;
//             return false;
//         }
//         else{
//             tip.getElementsByTagName("span")[0].innerHTML = "";
//             tip.className="check fa fa-check";
//             tip.style.opacity='1';
//             cm=true;
//         }
//     }


// $("#save").on("click",function(e){
// 	e.preventDefault();
// 	var mail=$("#new-mail").val();
// 	var code=$("#new-code").val();
// 	if(cp=="" || cm==""){
// 		alertInformation("请完善设置");
// 		return false;
// 	}
// 	$.ajax({
//         type:"POST",
//         url:"/manage/changeEmail/",
//         cache:false,
//         data:{
//             "mail":mail,
//             "code": code
//         },
//         success:function(data){
//         	if(data.code == 1) {
// 				alertInfoWithJump(data.info,"/manage/changeMail");
// 			}
// 			else {
//                 alertInformation(data.info);
//             }
//         },
//         fail: function() {
//             alertInformation("数据传输有误");
//         },
//         error: function(response) {
//             alertInformation("网络连接有误");
//         }
//     });
// })




$(".manager table .select-all").on("change",function(){
    var list=$(".manager table input[type='checkbox']");
    if (list[0].checked==true) {
        for(var i=1;i<list.length;i++){
            list[i].checked=true;
        }
    }
    else{
        for(var j=1;j<list.length;j++){
            list[j].checked=false;
        }
    }
});
$(".manager table input[type='checkbox']").on("change",function(){
    var list=$(".manager table input[type='checkbox']");
    if ($(this).hasClass("select-all")==false) {
        var flag=0;
        for(var i=1;i<list.length;i++){
            if(list[i].checked==true){
                flag++;
            }
            if(list[i].checked==false){
                flag--;
            }
        }
        if(flag==list.length-1){
            list[0].checked=true;
        }
        else{
            list[0].checked=false;
        }
    }
});

$(".manager .manage-btn #readed").on("click",function(){
    var list=$(".manager table input[type='checkbox']");
    for(var i=1;i<list.length;i++){
        if (list[i].checked==true) {
            console.log($(list[i]).parent().parent());
            $(list[i]).parent().parent().attr("class","");
            list[i].checked=false;
        }
    }
});