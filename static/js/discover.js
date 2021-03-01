$(document).ready(function(){
    var gists = []
    $.ajax({
        url: '/api/gist',
        type: 'GET',
        dataType: 'json',
        async: false,
        success: function(data) {
            gists = data
        }
    })

    var gist_list = $('#gists')
    gists.forEach(function(gist, index){
        var div = document.createElement('div')
        div.setAttribute('id', gist.gist_id)
        // append user_name and gist_name
        var names = document.createElement('h3')
        names.innerHTML = "<span id="+gist.user_id+"><a href=/user/"+gist.user_id+" style='text-decoration:none;'>"+gist.user_name+"</span> / <span id="
                          +gist.gist_id+"><a href=/gist/"+gist.gist_id+" style='text-decoration:none;'>"+gist.gist_name+"</span>"
        names.setAttribute('id', 'name'+(index+1))
        div.appendChild(names)
        // append description
        var description = document.createElement('p')
        description.innerHTML = 'Description' + ': ' + gist.description
        description.setAttribute('id', 'desc'+(index+1))
        div.appendChild(description)
        // append gist content
        var content = document.createElement('textarea')
        content.value = gist.content
        content.setAttribute('id', 'content'+(index+1))
        div.appendChild(content)

        gist_list.append(div)
    })
})
