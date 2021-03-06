$(document).ready(function () {
    let editor = ace.edit('editor', {
        theme: 'ace/theme/xcode',
        maxLines: 50,
        minLines: 20,
        wrap: true,
        autoScrollEditorIntoView: true,
    });

    var modelist = ace.require('ace/ext/modelist');

    $('#gistname').on('input', function (e) {
        let filePath = e.target.value;
        var mode = modelist.getModeForPath(filePath).mode;
        editor.session.setMode(mode);
    });

    $('#gist-form').submit(function (e) {
        e.preventDefault();
        let auth0_id = $('#current_user').attr('title');
        console.log(auth0_id);
        let user_id = '';
        let user_name = '';
        let gist_name = $('#gistname').val();
        let description = $('#description').val();
        let content = editor.getValue();

        var formData = new FormData();
        formData.append('auth0_id', auth0_id);

        axios
            .post(
                '/api/user',
                formData
            )
            .then((response) => {
                user_id = response.data.user_id;
                return axios.get('/api/user/' + user_id);
            })
            .then((response) => {
                user_name = response.data[0].user_name;

                let payload = new FormData();
                payload.append('user_id', user_id);
                payload.append('gist_name', gist_name);
                payload.append('user_name', user_name);
                payload.append('description', description);
                payload.append('content', content);

                return axios.post('api/gist', payload);
            })
            .then((response) => {
                console.log(response);
                document.location.href = "/";
            })
            .catch((error) => console.log(error.response));
    });
});
