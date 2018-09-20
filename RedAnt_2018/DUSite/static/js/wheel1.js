//通过left更改达到轮播效果；
'use strict';
//声明
var images=document.getElementById('photo').getElementsByTagName('img');
var preButton=document.getElementById('pre');
var afterButton=document.getElementById('after');
var spot=document.getElementById('wheel-spot').getElementsByTagName('div');
var num=images.length;
// var dis=images[0].width+'px';
// console.log(dis);
var count=0;
var play;

var init=function(){
	for (var i = 1; i < num; i++) {
		images[i].className='hide';
	}
	images[0].className='curr';
	images[num-1].className='last';
}
var show=function(k){
	var i=k-1,j=count+1;
	if (i==-1) {
		i=num-1;
	}
	if (j==num) {
		j=0;
	}
	images[i].className='hide';
	images[j].className='hide';
	images[count].className='curr trans-eff';
	images[k].className='trans-eff last';
	spot[count].className='active-spot spot';
	spot[k].className='spot';
	// setTimeout(function(){images[i].className='hide';},600);
}
var autoWheel=function(){
	play=setInterval(function(){
		var j=count;
		count++;
		if (count==num){
			count=0;
		}
		show(j);
	},3000);
}
var stop=function(){
	clearInterval(play);
}
var preButtonClick=function(){
	var j=count,k=j+1;
	count--;
	if (count==-1){
		count=num-1;
	}
	var i=count-1;
	if(i==-1){
		i=num-1;
	}
	if(k==num){
		k=0;
	}
	images[k].className='hide';
	images[i].className='last';
	images[count].className='trans-eff curr';
	images[j].className='trans-eff hide';
	spot[count].className='active-spot spot';
	spot[j].className='spot';
}
var afterButtonClick=function(){
	var j=count;
	count++;
	if (count==num){
		count=0;
	}
	show(j);
}

//函数调用
init();
//autoWheel();
document.getElementById('photo').addEventListener("mouseover",stop,false);//不能直接用images.
//document.getElementById('photo').addEventListener("mouseout",autoWheel,false);
preButton.addEventListener("click",preButtonClick);
afterButton.addEventListener("click",afterButtonClick);