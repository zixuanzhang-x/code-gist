$(document).ready(function(){
    var gist_id = location.pathname.split('gist/')[1]
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
            url: '/api/gist/'+ gist_id +'/comment',
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

    // check whether user stared this gist
    if (user_id) {
        var stared_gists = []
        $.ajax({
            url: '/api/user/'+ user_id +'/star',
            type: 'GET',
            dataType: 'json',
            async: false,
            success: function(data) {
                stared_gists = data
            }
        })
        document.getElementById('star_gist').innerHTML = 'To star'
        stared_gists.forEach(el => {
            if (el.gist_id == gist_id) {
                document.getElementById('star_gist').innerHTML = 'Unstar'
            }
        })
    }

        $('#star_gist').click(function(event) {
            if (document.getElementById('star_gist').innerHTML == 'To star') {
                // star gist
                $.ajax({
                    type: 'POST',
                    url: '/api/gist/'+ gist_id +'/star',
                    data: { 
                        user_id: user_id
                    },
                    success: function(data) {
                        document.getElementById('star_gist').innerHTML = 'Unstar'
                    }
                })
            } else {
                // delete gist star
                $.ajax({
                    type: 'DELETE',
                    url: '/api/gist/'+ gist_id +'/star',
                    data: {
                        user_id: user_id
                    },
                    success: function(data) {
                        document.getElementById('star_gist').innerHTML = 'To star'
                    }
                })
            }
            // update gist star number
            var gists = []
            $.ajax({
                url: '/api/gist/'+ gist_id,
                type: 'GET',
                dataType: 'json',
                async: false,
                success: function(data) {
                    gists = data
                }
            })
            document.getElementById('star_num').innerHTML = 'Stared: ' + gists[0].stars
            event.preventDefault()
        })
})
