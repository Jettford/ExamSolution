function cardCheck() {
    var selected = document.querySelector('#card:checked');
    document.getElementById('cardDetails').style = selected ? "display: block" : "display: none";

    var fields = document.getElementById('cardDetails').querySelectorAll('input');
    for (var i = 0; i < fields.length; i++) {
        fields[i].required = selected;
    }    
}

function startup() {
    var form = document.getElementById('submitForm');

    form.onchange = cardCheck;
    cardCheck();
}

document.addEventListener('DOMContentLoaded', startup);