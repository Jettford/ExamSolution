var titleInput = document.getElementById('title');
var bodyInput = document.getElementById('body');

var titlePreview = document.getElementById('titlePreview');
var bodyPreview = document.getElementById('bodyPreview');

function updateRender() {
    var title = titleInput.value;
    var body = bodyInput.value;
    
    titlePreview.innerHTML = title;

    // note on the use of dom purify
    // 
    // we don't want the admin accidentally being dumb and copying something malicious to themselves into this box and it running the script instantly, so we use dom purify to sanitize the html
    // it is also cleaned up later on the server in a Jinja filter before it reaches users. 

    var res = DOMPurify.sanitize(marked.parse(body));
    bodyPreview.innerHTML = res;
}

titleInput.addEventListener('input', updateRender);
bodyInput.addEventListener('input', updateRender);

updateRender();