window.addEventListener('DOMContentLoaded', function() {

    var form = document.querySelector('#customer-form');
    form.addEventListener('submit', function(event) {
        event.preventDefault();
        //read it from text
    var username = document.querySelector('#username').value;
    alert('Welcome, ' + username + '!');
    })

})