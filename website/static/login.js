function startup() {
    var form = document.getElementById('registerForm');
    form.onsubmit = function (e) {
        var form = document.getElementById('registerForm');
        var formData = new FormData(form);

        if (formData.get("password") !== formData.get("password2")) {
            e.preventDefault();
            alert('Passwords do not match!');
            return;
        }
    };
}

document.addEventListener('DOMContentLoaded', startup);