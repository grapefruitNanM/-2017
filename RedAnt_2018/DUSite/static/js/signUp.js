'use strict';

	var cm='',cp='',ca='',cf='',cg='',ci='';
	//验证邮箱
	function isEmail(strEmail) {
	    if (strEmail.search(/^[A-Za-z\d]+([-_.][A-Za-z\d]+)*@([A-Za-z\d]+[-.])+[A-Za-z\d]{2,4}$/) != -1)
	        return true;
	    else
	        return false;
	}

	function checkMail(node) {
	    var tip = document.getElementById("sign-up-mail").getElementsByClassName("check")[0];
	    var mail = node.value;
	    if(mail==""){
	    	tip.style.opacity='0';
	    	cm=false;
	    	return false;
	    }
	    if( ! isEmail(mail) ){
	    	tip.style.opacity='1';
	    	tip.className="fa fa-close check";
	    	tip.style.color="red";
	    	cm=false;
	    	return false;
	    }
	    else{
		    $.ajax({
		        type:"POST",
		        url:"/index/emailCheck/",
		        async:false,
		        cache:false,
		        data:{
	                "email": mail
		        },
		        success:function(data){
		        	if(data.code == 1) {
					    	tip.style.opacity='1';
					    	tip.className="fa fa-check check";
					    	tip.style.color="green";
				    		cm=true;
					    }
					else {
					    	//("#hint-mail").html("邮箱已注册");
					    	alertInformation(data.info);
					    	tip.style.opacity='1';
					    	tip.className="fa fa-close check";
					    	tip.style.color="red";
					    	cm=false;
	                }
		        },
	            fail: function() {
					e.preventDefault();
	                alertInformation("数据传输有误");
	            },
	            error: function(response) {
					e.preventDefault();
	                alertInformation("网络连接有误");
	                // $("html").load("test.php");
	            }
		    });
	    }
	}

	//验证密码
	function isPsw(strPsw) {
	    if (strPsw.search(/^[\\u4e00-\\u9fa5_a-zA-Z0-9-]{6,20}$/) != -1){
	    // if(strPsw.length!=0){
	        return true;
	    }
	    else{
	        return false;
	    }
	}

	function checkPsw(node) {
	    var tip = document.getElementById("sign-up-psw").getElementsByClassName("check")[0];
	    var pwd = node.value;
	    if(pwd==""){
	    	tip.style.opacity='0';
	    	cp=false;
	    	return false;
	    }
	    if( ! isPsw(pwd) ){
	    	tip.style.opacity='1';
	    	tip.className="fa fa-close check";
	    	tip.style.color="red";
	    	cp=false;
	    	return false;
	    }
	    else{
	    	cp=true;
	    	tip.style.opacity='1';
	    	tip.className="fa fa-check check";
	    	tip.style.color="green";
	    }
	    var conf=document.getElementById("cf-psw").value;
	    if(conf!=""){
	    	confirmPsw(document.getElementById("cf-psw"));
	    }
	    if(pwd==""){
	    	confirmPsw(document.getElementById("cf-psw"));
	    }
	}
	//确认密码
	function confirmPsw(node){
		var tip = document.getElementById("confirm-psw").getElementsByClassName("check")[0];
	    var pwd = node.value;
	    var proto=document.getElementById("psw").value;
	    if(pwd==""){
	    	tip.style.opacity='0';
	    	cf=false;
	    	return false;
	    }
	    if( pwd == proto){
	    	tip.style.opacity='1';
	    	tip.className="fa fa-check check";
	    	tip.style.color="green";
	    	cf=true;
	    	if(proto==""){
	    		tip.style.opacity='0';
	    		cf=false;
	    	}
	    }
	    else{
	    	tip.style.opacity='1';
	    	tip.className="fa fa-close check";
	    	tip.style.color="red";
	    	cf=false;
	    	return false;
	    }
	}

	//验证账号
	function checkAccount(node) {
	   	var tip = document.getElementById("sign-up-name").getElementsByClassName("check")[0];
	    var account = $.trim(node.value);
	    var name= node.value;
	    var reg=/^[\u4e00-\u9fff\w]{2,10}$/;/*由字母、数字、_或汉字组成;*/
	    if(name==""){
	    	tip.style.opacity=0;
	        ca=false;
	        return false;
	    }
	    console.log(reg.test(name));
	    if (reg.test(name)!=true) {
	       	tip.style.opacity=1;
	    	tip.className="fa fa-close check";
	    	tip.style.color="red";
	        ca=false;
	        return false;
	    }
	    else {
	    	$.ajax({
		        type:"POST",
		        url:"/index/userCheck/",
		        // async:false,
		        cache:false,
		        data:{
	                "username": name
		        },
		        success:function(data){
		        	if(data.code == 1) {
					    	tip.style.opacity='1';
					    	tip.className="fa fa-check check";
					    	tip.style.color="green";
				    		ca=true;
					    }
					else{
					    	//("#hint-name").html("用户名冲突");
							alertInformation(data.info);
					    	tip.style.opacity='1';
					    	tip.className="fa fa-close check";
					    	tip.style.color="red";
					    	ca=false;
					    }
					},
				fail: function() {
					e.preventDefault();
	                alertInformation("数据传输有误");
	            },
				error: function(response){
                    e.preventDefault();
                    alertInformation("网络连接有误");
                    // $("html").load("test.php");
                }
		    });
	    }
	}


	function checkInv(node){
		var tip = document.getElementById("invitation").getElementsByClassName("check")[0];
		if(node.value==""){
			tip.style.opacity='1';
	    	tip.className="fa fa-close check";
	    	tip.style.color="red";
	        ci=false;
			return false;
		}
		else{
			tip.style.opacity='0';
	    	tip.className="fa check";
	    	ci=true;
		}
	}
	function checkPro(node){
		var tip = document.getElementById("project").getElementsByClassName("check")[0];
		if(node.value=="----"){
			tip.style.opacity='1';
	    	tip.className="fa fa-close check";
	    	tip.style.color="red";
	        cg=false;
			return false;
		}
		else{
			tip.style.opacity='0';
	    	tip.className="fa check";
	    	tip.style.color="green";
	    	cg=true;
		}
	}


	var showHint=function(e){
		var id=e.name;
		var getHint="hint-"+id;
		var hintEl=document.getElementById(getHint);
		$(e).siblings("span.hint").css("opacity","1");
		if(id=="mail"){
			hintEl.innerHTML="";
		}
		else if(id=="name"){
			hintEl.innerHTML="请输入2-10位由字母、数字、_或汉字组成的用户名";
			$(hintEl).siblings("i").css("opacity","1");
		}
		else if(id=="password"){
			hintEl.innerHTML="请输入6-20位密码，可包含字母、数字、横线或下划线";
			$(hintEl).siblings("i").css("opacity","1");
		}
		else if(id=="confirm-password"){
			hintEl.innerHTML="";
		}
		else
			hintEl.innerHTML="";
	}
	var hideHint=function(e){
		var id=e.name;
		var getHint="hint-"+id;
		var hintEl=document.getElementById(getHint);
		$(e).siblings("span.hint").css("opacity","0");
		$(hintEl).siblings("i").css("opacity","0");
	}


	$("#sign-up").on("submit",function(e){
		e.preventDefault();
		if(cm!=true || ca!=true || cp!=true ||cf!=true ||ci!=true ||cg!=true){
			alertInformation("请继续完善信息!");
			return false;
		}
		var username = $("#name").val();
		var email = $("#mail").val();
        var psw = $("#psw").val();
        var project=$("#proGroup").val();
        var invitation=$("#invcode").val();
		$.ajax({
	        type:"POST",
	        url:"/index/sign_up/",
	        async:false,
	        cache:false,
	        data:{
	            "username": username,
                "email": email,
                "password": psw,
                "project" : project,
                "invitation" : invitation
	        },
	        success:function(data){
	        	if(data.code == 1) {
	        		// $('#sign-up-container').load("sign-upJump.txt");
					// location.href=;
					alertInfoWithJump(data.info,"/index/");
					// $('#sign-up-container').load("sign-upJump.txt");
				}
				else {
                    alertInformation(data.info);
                }
	        },
            fail: function() {
				e.preventDefault();
                alertInformation("数据传输有误");
            },
            error: function(response) {
				e.preventDefault();
                alertInformation("网络连接有误");
                // $("html").load("test.php");
            }
	    });
	});
