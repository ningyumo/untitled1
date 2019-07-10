$(document).ready(function () {
    // 修改昵称
    $('#change_nick_name_link').click(function () {
        $('#change_nick_name_form_errors').text('');
        $('#id_nick_name').val('');
    });
    $('#change_nick_name_form').submit(function (event) {
        event.preventDefault();
        $.ajax({
            url: 'change/nickname/',
            type: 'POST',
            data: $(this).serialize(),
            cache: false,
            success: function (data) {
                if (data['status'] == 'SUCCESS') {
                    window.location.reload();
                } else {
                    $('#change_nick_name_form_errors').text('该昵称已存在')
                }
            }
        })
    });

    // 修改邮箱
    $('#change_email_link').click(function () {
        $('#id_email').val('');
        $('#id_verify_code').val('');
        $('#change_email_form_errors').text('');
    });
    $('#send_email').click(function () {
        $('#change_email_form_errors').text('');
        var email = $('#id_email').val();
        if (email == '') {
            $('#change_email_form_errors').text('请输入邮箱');
        } else {
            $.ajax({
            url: '/accounts/sendemail/',
            type: 'get',
            data: {
                'to': email,
                'action': 'change_email',
            },
            cache: 'false',
            success: function () {
            }});
        $(this).addClass('disabled');
        $(this).attr('disabled', true);
        var time = 30;
        $(this).text(time + '秒后可重新发送');
        function clock() {
            if (time <= 0) {
                clearInterval(interval);
                $('#send_email').removeClass('disabled');
                $('#send_email').attr('disabled', false);
                $('#send_email').text('发送验证码');
                return false;
            }
            time --;
            $('#send_email').text(time + '秒后可重新发送')
        }
        var interval = setInterval(clock, 1000);
        }});
    $('#change_email_form').submit(function (event) {
        event.preventDefault();
        $.ajax({
            url: 'change/email/',
            type: 'POST',
            data:$(this).serialize(),
            cache: false,
            success: function (data) {
               if (data['status'] == 'EMAIL_EXIST') {
                   $('#change_email_form_errors').text('邮箱已存在')
               } else if (data['status'] == 'VERIFY_CODE_ERRORS') {
                   $('#change_email_form_errors').text('验证码错误')
               } else if (data['status'] == 'SUCCESS') {
                    window.location.reload();
               }
            }
        })
    });

    // 修改密码
    $('#change_password_link').click(function () {
        $('#id_old_password').val('');
        $('#id_new_password_1').val('');
        $('#id_new_password_2').val('');
        $('#change_password_form_errors').text('');
    });
    $('#change_password_form').submit(function (event) {
        event.preventDefault();
        var old_password = $('#id_old_passwird').val();
        var new_password_1 = $('#id_new_password_1').val();
        var new_password_2 = $('#id_new_password_2').val();
        $.ajax({
            url: 'change/password/',
            type: 'POST',
            cache: false,
            data: $(this).serialize(),
            success: function (data) {
                if (data['status'] == 'OLD_PASSWORD_ERROR') {
                    $('#change_password_form_errors').text('旧密码错误');
                } else if (data['status'] == 'NEW_PASSWORD_ERROR'){
                    $('#change_password_form_errors').text('新密码输入不一致');
                } else if (data['status'] == 'SUCCESS') {
                    $(window).attr('location', 'http://localhost:8000/accounts/login/')
                }
            }
        })
    })
});