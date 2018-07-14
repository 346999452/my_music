window.onload = function (ev) {
    load();
    jiazai();
};

var my_video = document.getElementById("my_video");

my_video.ontimeupdate = function() {
    var current_time = my_video.currentTime;
    var duration = my_video.duration;
    document.getElementById("current_time").innerHTML = Math.floor(current_time);
    document.getElementById('video_duration').innerHTML = Math.floor(duration);
};

var dataBarrage = [{
    value: '您好, 这是默认的弹幕，用于缓解无弹幕尴尬',
    color: '#FFFFFF',
    time: 0.3
}];

function jiazai() {
    $('.range').on('change', function () {
        // 改变弹幕的透明度和字号大小
        demoBarrage[this.name] = this.value * 1;
    });

    $('input[name="range"]').on('click', function () {
        // 改变弹幕在视频显示的区域范围
        demoBarrage['range'] = this.value.split(',');
    });

    $.ajax({
            url: '/lt/barrage/?movie_id=' + movie_id,
            type: 'GET',

            success: function (data) {
                info = JSON.parse(data);
                for (var i in info){
                    demoBarrage.add({
                        value: info[i].value,
                        color: info[i].color,
                        time: info[i].time
                    });
                }
            },

            error: function () {
                alert('发送弹幕失败')
            },

            beforeSend: function(xhr, settings) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        })
}

var my_canvas = document.getElementById("my_canvas");
var demoBarrage = new CanvasBarrage(my_canvas, my_video, {data: dataBarrage});

document.addEventListener("DOMContentLoaded", function() {
    $('.range').on('change', function () {
        // 改变弹幕的透明度和字号大小
        demoBarrage[this.name] = this.value * 1;
    });

    $('input[name="range"]').on('click', function () {
        // 改变弹幕在视频显示的区域范围
        demoBarrage['range'] = this.value.split(',');
    });

    // 发送弹幕
    var elForm = $('#barrageForm'), elInput = $('#input');
    elForm.on('submit', function (event) {
        event.preventDefault();
        // 新增弹幕

        barrage_data = {
            value: $('#input').val(),
            color: $('#color').val(),
            time: my_video.currentTime,
            movie_id: movie_id
        };

        $.ajax({
            url: '/lt/barrage/',
            type: 'POST',
            data: barrage_data,

            success: function (data) {
                demoBarrage.add(barrage_data);
                elInput.val('').trigger('input');
            },

            error: function () {
                alert('发送弹幕失败')
            },

            beforeSend: function(xhr, settings) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        })
    });
    // 提交按钮
    var elSubmit = elForm.find('input[type="submit"]');

    // 输入框和禁用按钮
    elInput.on('input', function () {
        if (this.value.trim()) {
            elSubmit.removeAttr('disabled');
        } else {
            elSubmit.attr('disabled', 'disabled');
        }
    });
}, false);

function com_commit() {
    $.ajax({
        cache: false,
        type: 'POST',
        data: new FormData($('#comment_data')[0]),
        url: '/lt/play/',
        traditional:true,
        processData: false,
        contentType: false,

        success: function(data) {
            alert(data);
            load()
        },

        error: function(){
            alert('请求服务器超时')
        },

        beforeSend: function(xhr, settings) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    });
};

function like(like, movie_id, comment_user_id, comment_time) {
    if (like){
        url = '/lt/like/'
    }else {
        url = '/lt/unlike/'
    }

    $.ajax({
        url: url,
        type: 'POST',
        data: {
            'movie_id': movie_id,
            'comment_user_id': comment_user_id,
            'comment_time': comment_time,
            'user_id': getCookie('id')
        },

        success: function (data) {
            load();
            alert(data)
        },

        error: function () {
            alert('请求服务器超时')
        },

        beforeSend: function (xhr, settings) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    })
}

function load(){
    $.ajax({
        url: '/lt/play/',
        type: 'POST',
        data: {
            'movie_id': movie_id
        },

        success: function (data) {
            var in_html = '';
            info = JSON.parse(data);
            for(var i in info){
                data = info[i];
                in_html += '<li class="single_comment">\n' +
                '            <div class="username">\n' +
                '              <strong>' + data.username + '</strong>\n' +
                '            </div>\n' +
                '            <div class="contents">\n' +
                '              <p>' + data.comment + '</p>\n' +
                '            </div>\n' +
                '            <div class="comment_time">\n' +
                '              <p class="text-info">' + data.comment_time + '</p>\n' +
                '            </div>\n' +
                '            <div style="min-width: 150px">\n';
                if(data.liked){
                    in_html += '<a href="javascript:void(0);" onclick="like(false, \'' + movie_id + '\', \'' + data.user_id + '\', \'' + data.comment_time + '\')"><img src="/static/image/已赞.png" title="您已赞过该评论" style="width: 50px; margin-left: 100px"></a>\n'
                }
                else {
                    in_html += '<a href="javascript:void(0);" onclick="like(true, \'' + movie_id +'\', \'' + data.user_id + '\', \'' + data.comment_time + '\')">' +
                        '<img src="/static/image/赞.png" style="width: 50px; margin-left: 100px"></a>\n'
                }
                in_html +=
                '                <p style="margin-left: 80px">已有' + data.likes + '人赞过</p>\n' +
                '            </div>\n';
                if (data.could_delete){
                    in_html += '                 <div style="min-width: 50px">\n'+
                    '                    <a href="javascript: void(0);" onclick="shanchu(\'' + data.user_id + '\', \'' + data.comment_time + '\')" style="margin-left: 30px">删除该条评论</a>\n'
                    +
                    '                 </div>\n' +
                    '        </li>'
                }
            }
            if (in_html) {
                $('#com').html(in_html)
            }
        },

        error: function () {
            alert('请求服务器失败')
        },

        beforeSend: function(xhr, settings) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    })
}

function shanchu(user_id, comment_time) {
    $.ajax({
        url: '/lt/delete/',
        type: 'POST',
        data: {
            'movie_id': movie_id,
            'user_id': user_id,
            'comment_time': comment_time
        },

        success: function (data) {
            load();
            alert(data)
        },

        error: function () {
            alert('请求服务器超时')
        },

        beforeSend: function (xhr, settings) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    })
}

var CanvasAutoResize = {
  draw: function() {
    var ctx = document.getElementById('my_canvas').getContext('2d');
    var canvasContainer = document.getElementById('canvas_container');
    ctx.canvas.width  = canvasContainer.offsetWidth - 30;
  },

  initialize: function(){
    var self = CanvasAutoResize;
    self.draw();
    $(window).on('resize', function(event){
      self.draw();
    });
  }
};

$(function(argument) {
  CanvasAutoResize.initialize();
});