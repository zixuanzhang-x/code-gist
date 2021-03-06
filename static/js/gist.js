$(document).ready(function(){
    // get user_id by auth0_id if have session
    var auth0_id = $('#current_user').attr('title')
    var user_id = ""
    if (auth0_id) {
        $.ajax({
            url: '/api/user',
            type: 'POST',
            data: {
                auth0_id: auth0_id,
            },
            dataType: 'json',
            async: false,
            success: function(data) {
                user_id = data.user_id
            }
        })
    }

    // leave comment
    $('form').on('submit', function(event) {
        $.ajax({
            url: '/api/gist/'+location.pathname.split('gist/')[1]+'/comment',
            type: 'POST',
            data: {
                content: $('#content').val(),
                user_id: user_id,
            },
        }).done(function(response) {
            if (response.error) {
                $('#errorAlert').text(data.error).show()
            } else {
                window.location.reload()
            }
        })
        event.preventDefault()        
    })

    // gist star number
    var gist_stars = []
    $.ajax({
        url: '/api/gist/'+location.pathname.split('gist/')[1]+'/star',
        type: 'GET',
        dataType: 'json',
        async: false,
        success: function(data) {
            gist_stars = data
        }
    })
    document.getElementById('star_num').innerHTML = "<a href=/gist/"+location.pathname.split('gist/')[1]+
                                                    "/stargazers style='text-decoration:none; color:#333;'>Stared: "+gist_stars.length+"</a>"

    // star gist button
    $("#star_gist").click(function(event) {
        $.ajax({
            type: "POST",
            url: "/api/gist/"+location.pathname.split('gist/')[1]+'/star',
            data: { 
                user_id: user_id
            },
            success: function(data) {
                alert('ok')
            },
            error: function(data) {

            }
        })
        event.preventDefault()
    })
})
