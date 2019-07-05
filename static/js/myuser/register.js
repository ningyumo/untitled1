$(document).ready(function () {
    $('#send_email').click(function () {
        var email = $('#id_email').val();
        $.ajax({
            url: 'sendemail/',
            type: 'get',
            data: {
                'to': email,
            },
            cache: 'false',
            success: function () {
                alert("验证码发送成功，10 分钟内有效");
            }});
        $(this).addClass('disabled');
        $(this).attr('disabled', true);
        var time = 30;
        $(this).text(time + '秒后可重新发送')
        var interval = setInterval(() => {
            if (time < 0) {
                clearInterval(interval);
                $(this).removeClass('disabled');
                $(this).attr('disabled', false);
                $(this).text('发送验证码');
                return false
            }
            time --;
            $(this).text(time + '秒后可重新发送')
        }, 1000)
        return false
        })
});