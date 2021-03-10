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
        div.classList.add('gist');
        // info_row contains user pic, user_name, gist_name, comments, and stars
        var info_row = document.createElement('div')
        info_row.setAttribute('class', "row")
        info_row.setAttribute('id', 'info_row')

        // append profile picture, user_name and gist_name
        var user_gist_row = get_user_and_gist(gist, index)
        info_row.appendChild(user_gist_row)
        // append comments and stars
        var feature_row = get_comment_and_star(gist, index)
        info_row.appendChild(feature_row)

        div.appendChild(info_row)

        // append created time 
        var created_time = document.createElement('p')
        created_time.innerHTML = 'Created at ' + gist.created
        created_time.setAttribute('id', 'created'+(index+1))
        div.appendChild(created_time)

        // append content
        let content = document.createElement('textarea');
        content.value = gist.content
        content.setAttribute('id', 'content'+(index+1))
        div.appendChild(content)

        // append current gist to gist_list
        gist_list.append(div)
    })

    function get_user_and_gist(gist, index) {
        var user_gist_row = document.createElement('div')
        user_gist_row.setAttribute('id', 'name'+(index+1))

        var pic_names = document.createElement('h3')

        var user_pic = document.createElement('span')
        user_pic.setAttribute('id', gist.user_pic)
        user_pic.innerHTML = "<img src='" + gist.picture + "' class='gists-userpic'>"

        var user_name = document.createElement('span')
        user_name.setAttribute('id', gist.user_id)
        user_name.innerHTML = "<a href=/user/"+gist.user_id+" class='gists-username'>"+gist.user_name+"</a>"

        var gist_name = document.createElement('span')
        gist_name.setAttribute('id', gist.gist_id)
        gist_name.innerHTML = "<a href=/gist/"+gist.gist_id+" class='gists-gistname'>"+gist.gist_name+"</a>"

        var slash = document.createElement('span')
        slash.innerHTML = " / "

        pic_names.appendChild(user_pic)  
        pic_names.appendChild(user_name)
        pic_names.appendChild(slash)
        pic_names.appendChild(gist_name)

        user_gist_row.appendChild(pic_names)
        return user_gist_row
    }

    function get_comment_and_star(gist, index) {
        var feature_row = document.createElement('div')

        feature_row.setAttribute('id', 'feature'+(index+1))

        var comments = document.createElement('button')
        var stars = document.createElement('button')
        comments.setAttribute('style', 'margin-right: 16px')

        comments.innerHTML = "<a href=/gist/"+gist.gist_id+" ><img src='../static/img/comment.png' class='btn' >"
                             +gist.comments+" comments</a>"
        stars.innerHTML = "<a href=/gist/"+gist.gist_id+"/stargazers ><img src='../static/img/star.png' class='btn' >"
                          +gist.stars+" stars</a>"

        feature_row.appendChild(comments)
        feature_row.appendChild(stars)
        return feature_row
    }

    let modelist = ace.require('ace/ext/modelist');

    gists.forEach((gist, index) => {
        let editor = ace.edit('content' + (index + 1), {
            theme: 'ace/theme/crimson_editor',
            maxLines: 20,
            minLines: 5,
            wrap: true,
            autoScrollEditorIntoView: true,
            mode: modelist.getModeForPath(gist.gist_name).mode,
            readOnly: true,
        });
    });
})
