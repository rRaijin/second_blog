$(document).ready(function() {
    $('.like-inject').click(function(){
        var add_like = $(".like-inject").data('add-like-url');
        var data = {
            add_likes : add_like,
        };
        console.log(data);
        var csrf_token = $('#csrf_getting_form [name="csrfmiddlewaretoken"]').val();
            data["csrfmiddlewaretoken"] = csrf_token;
        $.ajax({
            url : add_like,
            type : "POST",
            data: data,
            success: function (data) {
                $(".like_count").text(data.likes);
            },
            error: function (data) {
                console.log(data + "ERROR");
            }
        });
    });

    $('.dislike-inject').click(function(){
        var add_dislike = $(".dislike-inject").data('add-dislike-url');
        var data = {
            add_dislike : add_dislike,
        };
        var csrf_token = $('#csrf_getting_form [name="csrfmiddlewaretoken"]').val();
            data["csrfmiddlewaretoken"] = csrf_token;
        $.ajax({
            url : add_dislike,
            type : "POST",
            data: data,
            success: function (data) {
                $(".dislike_count").text(data.dislikes);
            },
            error: function (data) {
                console.log(data + "ERROR");
            }
        });
    });
});