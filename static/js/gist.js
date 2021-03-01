$(document).ready(function(){
    // get user_id by auth0_id
    var user_id = ""
    // TODO: get user_id using ajax post
    // $.ajax({
    //     url: '/api/user',
    //     type: 'POST',
    //     data: {
    //         auth0_id: $('#auth0_id').val(),
    //     },
    //     dataType: 'json',
    //     async: false,
    //     success: function(data) {
    //         user_id = data
    //     }
    // })

    $('form').on('submit', function(event) {
        $.ajax({
            url: '/gist/'+location.pathname.split('gist/')[1]+'/comment',
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

    var commented_user_id = $('#commented_user').attr('title')
    var commented_user_name = ""

    $.ajax({
        url: '/api/user/'+ parseInt(commented_user_id),
        type: 'GET',
        dataType: 'json',
        async: false,
        success: function(data) {
            commented_user_name = data[0].user_name
        }
    })

    document.getElementById('commented_user').innerHTML = commented_user_name
})
