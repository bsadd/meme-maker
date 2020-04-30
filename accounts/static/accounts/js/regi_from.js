$(document).ready(function(){
    $('.login-box .nav li').click(function(){
        id = $(this).attr('id');
        $('.login-box .nav li.selected, .login-box form.selected').removeClass('selected');
        $('#' + id + ', .login-box form.' + id).addClass('selected');
        $('.login-box form.' + id + ' input').first().focus();
    });
    $('.login-box form .input input').on("focus", function(){
       $(this).parent('.input').addClass('selected'); 
    }).blur(function(){
        $(this).parent('.input').removeClass('selected');
        if($(this).val() !== "")
            $(this).parent('.input').addClass('good');
    });
});