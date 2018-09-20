'use strict'
$(document).ready(function(){
	var filed=document.getElementsByClassName('news');
	$.ajax({
		type:"GET",
		url:"/static/news.json",
		dataType: 'JSON',
		success:function(news){
			var newContent='';
			for (var j = 0; j < filed.length; j++) {
				newContent='';
				for (var i = 0; i < news[j].length; i++) {      // looping through events
					newContent += '<li><span class="news-title"><a href=' + news[j][i].link + '>' + news[j][i].newsname + '</a></span>';
					newContent += '<span class="num">' + news[j][i].num + '</span>' + '</li>';
			    }
			    filed[j].getElementsByTagName('ul')[0].innerHTML=newContent;
			}
		}
	})
})