$(document).ready(function(){
   $('#logout').click(function () {
       var result = confirm('确定退出吗');
       if (result){
           $.ajax({
               url: "/account/logout/",
               type:"GET",
               data: $(this).serialize(),
               cache: false,
               success: function (data) {
                    $("#was_login").replaceWith(
                        '<li><a href="account/register/">注册</a></li>' + '<li><a href="account/login/">登陆</a></li>'
                    )
               },
           })
       }
   }) ;
});

