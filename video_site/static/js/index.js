window.onload = function (ev) {
      load('搞笑')
};

function load(category) {
    $.ajax({
        url: '/lt/',
        type: 'POST',
        data: {
            'category': category
        },

        success: function (data) {
            in_html = '';
            info = JSON.parse(data);
            for (var i in info){
                data = info[i];
                in_html += '<div class="col-md-3 col-sm-6">\n' +
                    '                    <div class="cuadro_intro_hover " style="background-color:#cccccc;">\n' +
                    '                        <p style="text-align:center;">\n' +
                    '                            <img src="' + data.img + '" class="img-responsive" alt="">\n' +
                    '                        </p>\n' +
                    '                        <div class="caption" style="margin-top: 95px">\n' +
                    '                            <div class="caption-text">\n' +
                    '                                <a href="/lt/play?id=' + data.id + '" title="' + data.title + '" class="fancybox"><i class="fa fa-arrows-alt fa-2x"></i></a>\n' +
                    '                            </div>\n' +
                    '                        </div>\n' +
                    '                    </div>\n' +
                    '                </div>'
            }
            $('#commend').html(in_html)
        },

        error: function () {
            alert('请求服务器超时')
        },

        beforeSend: function (xhr, settings) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    })
}
