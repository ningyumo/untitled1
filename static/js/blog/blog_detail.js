$(document).ready(function (newChild, refChild) {
    var blog_pk = $('#id_object_id').val();
    // 定义一个格式化函数
    String.prototype.format = function(){
    var str = this;
    for (var i = 0; i < arguments.length; i++) {
        var str = str.replace(new RegExp('\\{' + i + '\\}', 'g'), arguments[i])
    };
    return str;
};
    // 监控滚动条，到一定位置后评论区固定
    $(document).scroll(function () {
        var scroH = $(document).scrollTop();
        if (scroH > 72) {
            $('#blog_detail_comment').addClass('blog_detail_comment_second');
        } else {
            $('#blog_detail_comment').removeClass('blog_detail_comment_second');
        }
    });
    // 清除评论错误的内容
    $('#id_content').click(function () {
        $('#form_non_field_errors').text('');
    });
    //ajax提交评论
    $('#comment_form').submit(function (event) {
        event.preventDefault();
        var content = $('#id_content').val();
        if (content.trim() == '') {
            $('#form_non_field_errors').text('评论不能为空');
        } else {
            $('.no_comment').hide();
            $.ajax({
                url: '/comment/submit/',
                type: 'post',
                cached: false,
                data: $(this).serialize(),
                success: function (data) {
                    if (data['status'] == 'SUCCESS') {
                        $('#id_content').val('');
                        $('#comment_to').text('');
                        if (data['comment_top_comment_pk'] == ''){
                            var html_text = '<div class="comment ancestor_comment comment_{0}" id="comment_{0}">' +
                                '<div class="row"><div class="col-md-2">' +
                                '<img class="blog_detail_profile_avatar img-circle" src="{4}" alt="">' +
                                '</div><div class="col-md-10">' +
                                '<span class="comment_creater">{1}</span> &nbsp;：{2}' +
                                '<div class="option" data-pk="{0}" id="option_{0}">{3}' +
                                '<span class="pull-right">' +
                                '<span class="delete" id="delete_{0}" hidden="hidden" data-delete-pk="{0}"><a href="">删除</a></span>&nbsp;' +
                                '<span class="reply" data-parent-comment-pk="{0}" ' +
                                'data-parent-comment-name="{1}" data-top-comment-pk="{0}">' +
                                '<a href="">回复</a>' +
                                '</span>&nbsp;<span class="like like_dislike" data-content-type="comment" data-object-id="{0}" id="like_{0}">' +
                                '赞(<span id="like_{0}_total">0</span>)</span></span></div><div class="child_comment" id="top_comment_{0}"></div></div></div></div>';
                            html_text = html_text.format(data['comment_pk'],
                                data['comment_creater_username'],
                                data['comment_content'],
                                data['create_time'],
                                data['avatar_url']);
                            $('#comment_area').prepend(html_text);
                            // 绑定回复功能
                            $('#comment_area').on('click', '.reply',function (event) {
                                event.preventDefault();
                                var parent_comment_creater_username = $(this).data('parent-comment-name');
                                var parent_comment_pk = $(this).data('parent-comment-pk');
                                var top_comment_pk = $(this).data('top-comment-pk');
                                $('#comment_to').text('回复 ' + parent_comment_creater_username + "：");
                                $('#id_content').focus();
                                $('#id_object_class').val('comment');
                                $('#id_object_id').val(parent_comment_pk);
                                $('#id_parent_comment_pk').val(parent_comment_pk);
                                $('#id_top_comment_pk').val(top_comment_pk);
                            });
                            //绑定显示隐藏删除按钮事件
                            $('#comment_area').on('mouseover', '#option_' + data['comment_pk'], function () {
                                $('#delete_' + data['comment_pk']).show();
                            });
                            $('#comment_area').on('mouseout', '#option_' + data['comment_pk'], function () {
                                $('#delete_' + data['comment_pk']).hide();
                            });
                            // 绑定删除评论事件
                            $('#comment_area').on('click', '#delete_' + data['comment_pk'], function (event) {
                                event.preventDefault();
                                var pk = data['comment_pk'];
                                var csrftoken = jQuery("[name=csrfmiddlewaretoken]").val();

                                function csrfSafeMethod(method) {
                                    // these HTTP methods do not require CSRF protection
                                    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
                                }
                                $.ajaxSetup({
                                    beforeSend: function(xhr, settings) {
                                        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                                            xhr.setRequestHeader("X-CSRFToken", csrftoken);
                                        }
                                    }
                                });
                                $.ajax({
                                    url: '/comment/delete/'+ pk + '/',
                                    type: 'post',
                                    cache: 'false',
                                    data:$(this).serialize(),
                                    success: function () {
                                        $('#comment_' + pk).detach();
                                        if ($('.comment').length == 0) {
                                            $('.no_comment').show();
                                        }
                                    }
                                })
                            });
                            // 绑定点赞事件
                            $('#comment_area').on('click', '#like_' + data['comment_pk'], function (event) {
                                event.preventDefault();
                                var object_id = data['comment_pk'];
                                var content_type = 'comment';
                                $.ajax({
                                    url: '/like/change',
                                    type: 'GET',
                                    cached: false,
                                    data: {
                                        'content_type' : content_type,
                                        'object_id' : object_id,
                                    },
                                    success: function (data) {
                                        if (data['status'] == 'CREATED_SUCCESS') {
                                            $('#like_' + object_id).removeClass('like_dislike');
                                            $('#like_' + object_id).addClass('like_like');
                                            var total = $('#like_' + object_id + '_total').text();
                                            total++;
                                            $('#like_' + object_id + '_total').text(total);
                                        } else if (data['status'] == 'DELETE_SUCCESS') {
                                            $('#like_' + object_id).removeClass('like_like');
                                            $('#like_' + object_id).addClass('like_dislike');
                                            var total = $('#like_' + object_id + '_total').text();
                                            total--;
                                            $('#like_' + object_id + '_total').text(total)
                                        }
                                    }
                                })
                            })
                        } else {
                            var html_text = '<div class="comment child_comment_{0}" id="comment_{0}">' +
                                '<span class="comment_creater">{1}</span>&nbsp;&nbsp;回复&nbsp;&nbsp;<span class="comment_creater">{2}</span>：{3}' +
                                '<div class="option" data-pk="{0}"  id="option_{0}">{4}<span class="pull-right">' +
                                '<span class="delete" id="delete_{0}" hidden="hidden" data-delete-pk="{0}"><a href="">删除</a></span>&nbsp;' +
                                '<span class="reply" data-parent-comment-pk="{0}" ' +
                                'data-parent-comment-name="{1}" data-top-comment-pk="{5}">' +
                                '<a href="">回复</a></span>&nbsp;<span  class="like like_dislike" data-content-type="comment" data-object-id="{0}" id="like_{0}">' +
                                '赞(<span id="like_{0}_total">0</span>)</span></span></div></div>';
                            html_text = html_text.format(data['comment_pk'],
                                data['comment_creater_username'],
                                data['comment_parent_creater_username'],
                                data['comment_content'],
                                data['create_time'],
                                data['comment_top_comment_pk']
                                );
                            $('#top_comment_' + data['comment_top_comment_pk']).prepend(html_text);
                            // 绑定回复事件
                            $('#comment_area').on('click', '.reply',function (event) {
                                event.preventDefault();
                                var parent_comment_creater_username = $(this).data('parent-comment-name');
                                var parent_comment_pk = $(this).data('parent-comment-pk');
                                var top_comment_pk = $(this).data('top-comment-pk');
                                $('#comment_to').text('回复 ' + parent_comment_creater_username + "：");
                                $('#id_content').focus();
                                $('#id_object_class').val('comment');
                                $('#id_object_id').val(parent_comment_pk);
                                $('#id_parent_comment_pk').val(parent_comment_pk);
                                $('#id_top_comment_pk').val(top_comment_pk);
                            });
                            $('#id_object_class').val('blog');
                            $('#id_object_id').val(blog_pk);
                            $('#id_parent_comment_pk').val('');
                            $('#id_top_comment_pk').val('');
                            //绑定显示隐藏删除按钮事件
                            $('#comment_area').on('mouseover', '#option_' + data['comment_pk'], function () {
                                $('#delete_' + data['comment_pk']).show();
                            });
                            $('#comment_area').on('mouseout', '#option_' + data['comment_pk'], function () {
                                $('#delete_' + data['comment_pk']).hide();
                            });
                            // 绑定删除评论事件
                            $('#comment_area').on('click', '#delete_' + data['comment_pk'], function (event) {
                                event.preventDefault();
                                var pk = data['comment_pk'];
                                var csrftoken = jQuery("[name=csrfmiddlewaretoken]").val();

                                function csrfSafeMethod(method) {
                                    // these HTTP methods do not require CSRF protection
                                    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
                                }
                                $.ajaxSetup({
                                    beforeSend: function(xhr, settings) {
                                        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                                            xhr.setRequestHeader("X-CSRFToken", csrftoken);
                                        }
                                    }
                                });
                                $.ajax({
                                    url: '/comment/delete/'+ pk + '/',
                                    type: 'post',
                                    cache: 'false',
                                    data:$(this).serialize(),
                                    success: function () {
                                        $('#comment_' + pk).detach();
                                        if ($('.comment').length == 0) {
                                            $('.no_comment').show();
                                        }
                                    }
                                })
                            })
                            // 绑定点赞事件
                            $('#comment_area').on('click', '#like_'+ data['comment_pk'], function (event) {
                                event.preventDefault();
                                var object_id = data['comment_pk'];
                                var content_type = 'comment';
                                $.ajax({
                                    url: '/like/change',
                                    type: 'GET',
                                    cache: false,
                                    data: {
                                        'content_type' : content_type,
                                        'object_id' : object_id,
                                    },
                                    success: function (data) {
                                        if (data['status'] == 'CREATED_SUCCESS') {
                                            $('#like_' + object_id).removeClass('like_dislike');
                                            $('#like_' + object_id).addClass('like_like');
                                            var total = $('#like_' + object_id + '_total').text();
                                            total++;
                                            $('#like_' + object_id + '_total').text(total);
                                        } else if (data['status'] == 'DELETE_SUCCESS') {
                                            $('#like_' + object_id).removeClass('like_like');
                                            $('#like_' + object_id).addClass('like_dislike');
                                            var total = $('#like_' + object_id + '_total').text();
                                            total--;
                                            $('#like_' + object_id + '_total').text(total)
                                        }
                                    }
                                })
                            })
                        }
                    } else if (data['status'] == 'CONTENT_ERRORS') {
                        $('#form_non_field_errors').text('评论不能为空');
                    } else if (data['status'] == 'COMMENT_OBJECT_ERRORS') {
                        $('#form_non_field_errors').text('评论对象不存在');
                    }
                }
            })
        }
    });
    // 回复评论（登录后）
    $('.reply').click(function (event) {
        event.preventDefault();
        var parent_comment_creater_username = $(this).data('parent-comment-name');
        var parent_comment_pk = $(this).data('parent-comment-pk');
        var top_comment_pk = $(this).data('top-comment-pk');
        $('#comment_to').text('回复 ' + parent_comment_creater_username + "：");
        $('#id_content').focus();
        $('#id_object_class').val('comment');
        $('#id_object_id').val(parent_comment_pk);
        $('#id_parent_comment_pk').val(parent_comment_pk);
        $('#id_top_comment_pk').val(top_comment_pk);
    });
    // 回复评论（未登录，显示登陆框）
    $('.reply_no_login').click(function (event) {
        event.preventDefault();
        $('#login_modal').modal('show');
    })
    // 显示和隐藏删除评论按钮
    $('.option').mouseout(function () {
       var  pk = $(this).data('pk');
        $('#delete_' + pk).hide();
    })
    $('.option').mouseover(function () {
        var  pk = $(this).data('pk');
        $('#delete_' + pk).show();
    });

    // 删除评论
    $('.delete').click(function (event) {
        event.preventDefault();
        var pk = $(this).data('delete-pk');
        var csrftoken = jQuery("[name=csrfmiddlewaretoken]").val();

        function csrfSafeMethod(method) {
            // these HTTP methods do not require CSRF protection
            return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
        }
        $.ajaxSetup({
            beforeSend: function(xhr, settings) {
                if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                    xhr.setRequestHeader("X-CSRFToken", csrftoken);
                }
            }
        });
        $.ajax({
            url: '/comment/delete/'+ pk + '/',
            type: 'post',
            cache: 'false',
            data:$(this).serialize(),
            success: function () {
                $('#comment_' + pk).detach();
                if ($('.comment').length == 0) {
                    $('.no_comment').show();
                }
            }
        })
    });

    // 点赞评论
    $('.like').click(function (event) {
        event.preventDefault();
        var object_id = $(this).data('object-id');
        var content_type = $(this).data('content-type');
        $.ajax({
            url: '/like/change',
            type: 'GET',
            cache: false,
            data: {
                'content_type' : content_type,
                'object_id' : object_id,
            },
            success: function (data) {
                if (data['status'] == 'CREATED_SUCCESS') {
                    $('#like_' + object_id).removeClass('like_dislike');
                    $('#like_' + object_id).addClass('like_like');
                    var total = $('#like_' + object_id + '_total').text();
                    total++;
                    $('#like_' + object_id + '_total').text(total);
                } else if (data['status'] == 'DELETE_SUCCESS') {
                    $('#like_' + object_id).removeClass('like_like');
                    $('#like_' + object_id).addClass('like_dislike');
                    var total = $('#like_' + object_id + '_total').text();
                    total--;
                    $('#like_' + object_id + '_total').text(total)
                } else if (data['status'] == 'NO_LOGIN_ERROR') {
                    $('#login_modal').modal('show');
                }
            }
        })
    });

    // 点赞博客
    $('#like_blog').click(function () {
        var object_id = $(this).data('blog-pk');
        $.ajax({
            url: '/like/change',
            type: 'GET',
            cache: false,
            data: {
                'content_type' : 'blog',
                'object_id' : object_id,
            },
            success: function (data) {
                if (data['status'] == 'CREATED_SUCCESS') {
                    $('#like_' + object_id).text('感谢点赞');
                    var total = $('.like_blog_total').text();
                    total++;
                    $('.like_blog_total').text(total);
                    $('#like_blog_' + object_id).addClass('like_blog');
                    $('#like_' + object_id).addClass('option_blog_btn');
                } else if (data['status'] == 'DELETE_SUCCESS') {
                    $('#like_blog_' + object_id).removeClass('like_blog');
                    $('#like_' + object_id).removeClass('option_blog_btn');
                    $('#like_' + object_id).text('点个赞吧');
                    var total = $('.like_blog_total').text();
                    total--;
                    $('.like_blog_total').text(total);
                } else if (data['status'] == 'NO_LOGIN_ERROR') {
                    $('#login_modal').modal('show');
                }
            }
        })
    })

    // 收藏博客
    $('#collect_blog').click(function () {
        var object_id = $(this).data('blog-pk');
        $.ajax({
            url: '/collection/collect/',
            cache: false,
            type: 'get',
            data: {
                'content_type': 'blog',
                'object_id': object_id
            },
            success: function (data) {
                if (data['status'] == 'CREATE_SUCCESS') {
                    $('#collect_' + object_id).text('感谢收藏');
                    var total = $('.collect_blog_total').text();
                    total++;
                    $('.collect_blog_total').text(total);
                    $('#collect_blog_' + object_id).addClass('collected');
                    $('#collect_' + object_id).addClass('option_blog_btn');
                } else if (data['status'] == 'DELETE_SUCCESS'){
                    $('#collect_' + object_id).text('收藏一下');
                    var total = $('.collect_blog_total').text();
                    total--;
                    $('.collect_blog_total').text(total);
                    $('#collect_blog_' + object_id).removeClass('collected');
                    $('#collect_' + object_id).removeClass('option_blog_btn');
                } else if (data['status'] == 'NO_LOGIN_ERRORS') {
                    $('#login_modal').modal('show');
                }
            },
        })
    })
});