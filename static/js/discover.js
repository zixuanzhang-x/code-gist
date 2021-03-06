$(document).ready(function(){
    var search = location.href.split('?q=')
    var gists = []
    $.ajax({
        url: search.length == 1 ? '/api/gist'  : '/api/gist?q=' + search[1],
        type: 'GET',
        dataType: 'json',
        async: false,
        success: function(data) {
            gists = data
        }
    })

    // render search bar content if searched
    if (search.length > 1) $('input:text').val(search[1])

    var gist_list = $('#gists')
    gists.forEach(function(gist, index){
        var div = document.createElement('div')
        div.setAttribute('id', gist.gist_id)
        // info_row contains user_name, gist_name, comments, and stars
        var info_row = document.createElement('div')
        info_row.setAttribute('class', "row")
        info_row.setAttribute('id', 'info_row')
        info_row.setAttribute('style', "height:30px")

        // append user_name and gist_name
        var name_row = document.createElement('div')
        name_row.setAttribute('style', "width:50%")
        name_row.setAttribute('id', 'name'+(index+1))

        var names = document.createElement('h3')

        var user_name = document.createElement('span')
        user_name.setAttribute('id', gist.user_id)
        user_name.innerHTML = "<a href=/user/"+gist.user_id+" style='text-decoration:none;'>"+gist.user_name+"</a>"
        var gist_name = document.createElement('span')
        gist_name.setAttribute('id', gist.gist_id)
        gist_name.innerHTML = "<a href=/gist/"+gist.gist_id+" style='text-decoration:none;'>"+gist.gist_name+"</a>"
        var slash = document.createElement('span')
        slash.innerHTML = " / "
        names.appendChild(user_name)
        names.appendChild(slash)
        names.appendChild(gist_name)

        name_row.appendChild(names)
        info_row.appendChild(name_row)

        // get comments and stars
        var gist_comments = []
        $.ajax({
            url: '/api/gist/'+gist.gist_id+'/comment',
            type: 'GET',
            dataType: 'json',
            async: false,
            success: function(data) {
                gist_comments = data
            }
        })

        var gist_stars = []
        $.ajax({
            url: '/api/gist/'+gist.gist_id+'/star',
            type: 'GET',
            dataType: 'json',
            async: false,
            success: function(data) {
                gist_stars = data
            }
        })

        // append comments and stars
        var feature_row = document.createElement('div')
        feature_row.setAttribute('style', 'margin-top: 2%; margin-left: 12%')
        feature_row.setAttribute('id', 'feature'+(index+1))

        var comments = document.createElement('button')
        var stars = document.createElement('button')
        comments.setAttribute('style', 'margin-right: 16px')

        comments.innerHTML= "<a href=/gist/"+gist.gist_id+" style='text-decoration:none; color:#333;'>"+gist_comments.length+" comments</a>"
        stars.innerHTML= "<a href=/gist/"+gist.gist_id+"/stargazers style='text-decoration:none; color:#333;'>"+gist_stars.length+" stars</a>"

        feature_row.appendChild(comments)
        feature_row.appendChild(stars)
        info_row.appendChild(feature_row)
        div.appendChild(info_row)

        // append created time 
        var created_time = document.createElement('p')
        created_time.innerHTML = 'Created at ' + gist.created
        created_time.setAttribute('id', 'created'+(index+1))
        div.appendChild(created_time)

        // append content
        var content = document.createElement('textarea')
        content.value = gist.content
        content.setAttribute('id', 'content'+(index+1))
        div.appendChild(content)

        // append current gist to gist_list
        gist_list.append(div)
    })
})
