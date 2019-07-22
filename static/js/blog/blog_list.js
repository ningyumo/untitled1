$(document).ready(function () {
    $(document).scroll(function () {
        var scroH = $(document).scrollTop();
        if (scroH > 83) {
            $('#tags').addClass('tags_second');
            $('#tags').removeClass('tags_first');
        } else {
            $('#tags').addClass('tags_first');
            $('#tags').removeClass('tags_second');
        }

    })
});