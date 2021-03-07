$(document).ready(function(){
    $('#gist_num').click(function(event) {
        $('.all_gists').show()
        $('.starred_gists').hide()
        event.preventDefault()
    })

    $('#star_num').click(function(event) {
        $('.all_gists').hide()
        $('.starred_gists').show()
        event.preventDefault()
    })
})
