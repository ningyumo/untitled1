$(document).ready(function () {
    $('#send_email').click(function () {
        $('#form_non_field_errors').text('');
        var email = $('#id_email').val();
        if (email == '') {
            $('#form_non_field_errors').text('请输入邮箱');
        } else {
            $.ajax({
            url: '/accounts/sendemail/',
            type: 'get',
            data: {
                'to': email,
                'action': 'find_password',
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
        }})
});