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

var jsonfy=function (table){
	var userList="{";
	for(var i=0;i<table.rows.length;i++){
		userList+="[";
		for (var j = 1; j < table.rows[i].cells.length; j++) {
			if(j==1){
				userList=userList+"'username':'"+table.rows[i].cells[j].innerHTML+"',";
			}
			if(j==2){
				userList=userList+"'email':'"+table.rows[i].cells[j].innerHTML+"',";
			}
			if (j==3) {
				userList=userList+"'userId':'"+table.rows[i].cells[j].innerHTML+",";
			}
			if (j==4) {
				userList=userList+"'team':'"+table.rows[i].cells[j].innerHTML+"'";
			}
		}
		userList+="]";
		if (i!=table.rows.length-1) {
			userList+=",";
		}
	}
	userList+="}";
	document.getElementById('hide-del').removeChild(table);
	return userList;
}

var submitList=function(table,status){
	var userList=jsonfy(table);
	if (userList=="{}") {
		return;
	}
	$.ajax({
		type:"POST",
        url:"/manage/",
        cache:false,
        data:{
            "userList": userList,
            "status": status
        },
        success:function(data){
        	if(data.code == 1) {
					alertInformation(data.info);
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
}

var removeItem=function(){
	// var list=$(".manager table tr");
	var list=document.getElementsByClassName('manager')[0].getElementsByTagName('table')[0];
	var deleted=document.createElement("table");
	document.getElementById('hide-del').appendChild(deleted);
	var check=document.getElementsByClassName('manager')[0].getElementsByTagName('table')[0].getElementsByTagName("input");
	for(var i=1;i<check.length;i++){
		if(check[i].checked==true){
			console.log(list.getElementsByTagName("tr")[i]);
			var append=list.getElementsByTagName("tr")[i];
			$(list.getElementsByTagName("tr")[i]).remove();
			i--;
			check.length--;
			deleted.appendChild(append);
		}
	}
	return deleted;
}

$(".manager #delete").on("click",function(){
	var table=removeItem();
	submitList(table,"delete");
});

$(".manager #change-rank").on("click",function(){
	var table=removeItem();
	submitList(table,"changeRank");
});


$(".manager select.manage-team").change(function(){
	var emailEl=$(this).parent("td").siblings("td")[2];
	var email=emailEl.innerHTML;
	var team=$(this).find('option:selected').val();
	$.ajax({
		type:"POST",
        url:"/manage/changeGroup/",
        cache:false,
        data:{
            "email":email,
            "team": team
        },
        success:function(data){
			if(data.code == 1) {
					alertInformation(data.info);
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