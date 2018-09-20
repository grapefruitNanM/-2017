window.onscroll=function(){
	var t = document.documentElement.scrollTop || document.body.scrollTop;
	var backTop=document.getElementById("backTop");
	if (t>200) {
		backTop.style.display='inline-block';
	}
	else{
		backTop.style.display='none';
	}
}

function backTotop() {
	var timer = null;
	cancelAnimationFrame(timer);
	requestAnimationFrame(function fn() {
		var oTop = document.body.scrollTop || document.documentElement.scrollTop;
		if (oTop > 0) {
			document.body.scrollTop = document.documentElement.scrollTop = 0;
			timer = requestAnimationFrame(fn);
		} else {
			cancelAnimationFrame(timer);
		}
	});
	// document.documentElement.scrollTop = document.body.scrollTop =0;
}

$(function(){
    //当滚动条的位置处于距顶部100像素以下时，跳转链接出现，否则消失
    $(function () {
        $(window).scroll(function(){
            if ($(window).scrollTop()>500){
                $(".corner-top").css("display","block");
            }
            else
            {
                $(".corner-top").css("display","none");
            }
        });
    });
});