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

    let modelist = ace.require('ace/ext/modelist');

    $('.gist').each(function(i, obj) {
        let filename = obj.parentNode.childNodes[1].childNodes[3].childNodes[1].textContent;
        let editor = ace.edit(obj.id, {
            theme: 'ace/theme/crimson_editor',
            maxLines: 20,
            minLines: 5,
            wrap: true,
            autoScrollEditorIntoView: true,
            mode: modelist.getModeForPath(filename).mode,
            readOnly: true,
        });
    });
})
