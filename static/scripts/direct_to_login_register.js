document.addEventListener('DOMContentLoaded', (event) => {
    document.getElementById('login_register_button').addEventListener('click', (e) => {
        sendRequest();
    });
});

function sendRequest() {
    fetch('/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ new_route: '/login' })
        })
        .then(response => response.json())
        .then(data => {
            console.log(data.message);
            window.location.href = data.new_route;
        })
        .catch(error => console.error('Error:', error));
}