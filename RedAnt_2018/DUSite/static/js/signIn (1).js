var cm = "", cp = "";

function isEmail(strEmail) {
    if (strEmail.search(/^[A-Za-z\d]+([-_.][A-Za-z\d]+)*@([A-Za-z\d]+[-.])+[A-Za-z\d]{2,4}$/) != -1)
        return true;
    else
        return false;
}

function checkMail(node) {
    var mail = node.value;
    if (!isEmail(mail)) {
        // tip.style.opacity='1';
        // tip.className='check fa fa-close red';
        cm = false;
        return false;
    }
    else {
        cm = true;
        // tip.className='check fa fa-check green';
        // tip.style.opacity='1';
    }
    // if (mail=='') {
    // 	// tip.className='check fa';
    // 	cm=true;
    // 	// tip.style.opacity='0';
    // }
}

function isPsw(strPsw) {
    if (strPsw.search(/^[\\u4e00-\\u9fa5_a-zA-Z0-9-]{6,20}$/) != -1) {
        return true;
    }
    else {
        return false;
    }
}

function checkPsw(node) {
    var tip = document.getElementById("check-psw");
    var pwd = node.value;
    if (!isPsw(pwd)) {
        // tip.style.opacity='1';
        // tip.className='check fa fa-close red';
        cp = false;
        return false;
    }
    else {
        cp = true;
        // tip.className='check fa fa-check green';
        // tip.style.opacity='1';
    }
    // if (pwd=='') {
    // 	// tip.className='check fa';
    // 	cp=true;
    // 	// tip.style.opacity='0';
    // }
}

$("#login").click(function (e) {
    e.preventDefault();
    $("#model-alertInfo span.model-title").html("登 录");
    if (cm != true || cp != true) {
        alertInformation("请完善表单");
        return false;
    }
    var mail = $("#model #mail").val();
    var psw = $("#model #psw").val();
    $.ajax({
        type: "POST",
        url: "/index/sign_in/",
        // async:false,
        cache: false,
        data: {
            "email": mail,
            "password": psw
        },
        success: function (data) {
            if (data.code == 1) {
                // if(data.info=="鐧诲綍鎴愬姛")
                alertInfoWithJump(data.info, "/index/");
                // else
                // 	alertInformation(data.info);
            }
            else {
                alertInformation(data.info);
            }
            // $('#sign-up-container').load("sign-upJump.txt");
        },
        fail: function () {
            alertInformation("failed");
        },
        error: function (response) {
            // console.log(document.getElementById("login").href);//file://......./user-id.html
            // console.log($("#login").attr('href'));//user-id.html
            // $('.enter').load($("#login").attr('href'));
            alertInformation("error");
        }
    });
});


$("#sign-btn").click(function () {
    $("#model").css("display", "block");
    // $("#model .model-container").css("top","25%");
    $("#model .model-container").css("opacity", 1);
})
$("#model .model-container .fa-close").click(function () {
    $("#model").css("display", "none");
    var input = $("#model .model-body input");
    var i = input.length;
    for (var n = 0; n < i - 1; n++) {
        input[n].value = '';
        $("#model .model-body i").css("opacity", 0);
    }
})

$("#signIn").click(function () {
    $("#model-alertInfo span.model-title").html("登 录");
    $("#model").css("display", "block");
    $("#forget-model").css("display", "none");
});

$("#forget").click(function (e) {
    e.preventDefault();
    $("#model-alertInfo span.model-title").html("忘记密码");
    $("#model").css("display", "none");
    $("#forget-model").css("display", "block");
});

$("#forget-model .model-head i").click(function(e){
	$("#model-alertInfo span.model-title").html(" 登 录 ");
    $("#forget-model").css("display", "none");
});

$("#findBack").click(function (e) {
    e.preventDefault();
    $("#model-alertInfo span.model-title").html("忘记密码");
    $("#model").css("display", "none");
    $("#forget-model").css("display", "block");
    if (cm != true) {
        alertInformation("请正确填写邮箱");
        return false;
    }
    var mail = $("#forget-model #mail").val();
    $.ajax({
        type: "POST",
        url: "/index/forget/",
        // async:false,
        cache: false,
        data: {
            "email": mail
        },
        success: function (data) {
            if (data.code == 1) {
                alertInformation(data.info);
            }
            else {
                alertInformation(data.info);
            }
        },
        fail: function () {
            alertInformation("failed");
        },
        error: function (response) {
            alertInformation("error");
        }
    });
});