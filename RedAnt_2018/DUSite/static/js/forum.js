$(function () {
    var cur_page = document.getElementById('cur-page');
    cur_page.setAttribute('value', '1');
    $.ajax({
        type: "POST",
        url: "post_tol_page/",
        success: function (data) {
            var tol_page = document.getElementById('tol-page');
            tol_page.setAttribute('value', data.tol_page);
            initPagination(data.tol_page);
            jump(1);
        }
    });

});

function initPagination() {
    var page = parseInt(document.getElementById('tol-page').value);
    var cur_page = parseInt(document.getElementById('cur-page').value);
    var pagination = document.getElementById('pagination');
    if (page <= 5) {
        pagination.innerHTML = '<li><a class=\'page-link\' onclick="jump(\'-\')">«</a></li>';
        for (var i = 1; i <= page; i++) {
            if (i !== cur_page)
                pagination.innerHTML += "<li><a class='page-link' onclick=\"jump('" + i + "')\">" + i + "</a></li>";
            else
                pagination.innerHTML += "<li><a class=\"page-link active\">" + i + "</a></li>";
        }
        pagination.innerHTML += '<li><a class=\'page-link\' onclick="jump(\'+\')">»</a></li>';
    }
    else {
        pagination.innerHTML = '<li><a class=\'page-link\' onclick="jump(\'-\')">«</a></li>';
        if (cur_page !== 1)
            pagination.innerHTML += "……";
        for (var i = 1; i < cur_page; i++) {
            if (i !== cur_page)
                pagination.innerHTML += "<li><a class='page-link' style='display:none'>" + i + "</a></li>";
        }
        for (var i = cur_page; i < cur_page + 5 && i <= page; i++) {
            if (i !== cur_page)
                pagination.innerHTML += "<li><a class='page-link' onclick=\"jump('" + i + "')\">" + i + "</a></li>";
            else
                pagination.innerHTML += "<li><a class=\"page-link active\">" + i + "</a></li>";
        }
        if (cur_page + 5 <= page)
            pagination.innerHTML += "……";
        pagination.innerHTML += '<li><a class=\'page-link\' onclick="jump(\'+\')">»</a></li>';
    }
}

function jump(page) {
    var jump_to = page;
    var cur_page = document.getElementById('cur-page');
    if (page === '-') {
        jump_to = cur_page.value - 1;
        if (jump_to < 1)
            return;
    }
    if (page === '+') {
        jump_to = document.getElementById('cur-page').value + 1;
        if (jump_to > document.getElementById('tol-page').value)
            return
    }
    $.ajax({
        type: "POST",
        url: "post_forum_ajax/",
        data: {
            "page": jump_to
        },
        success: function (result) {
            var posts = document.getElementsByClassName('container')[0];
            for (var i = 0; i < result.length; i++) {
                var post = document.getElementsByClassName("row")[0].cloneNode(true);
                post.setAttribute("style", "");
                post.getElementsByClassName("forumList").item(0).setAttribute('href', "forum=" + result[i].id + "/");
                post.getElementsByClassName("forumName").item(0).innerHTML = result[i].name;
                post.getElementsByClassName("forumMsg").item(0).innerHTML = result[i].month + "-" + result[i].day + "发表  回帖数：" + result[i].postNum + " 作者：" + result[i].user;
                posts.appendChild(post);
                console.log(post);
            }
        }
    });
    cur_page.setAttribute('value', jump_to);
    initPagination();
}