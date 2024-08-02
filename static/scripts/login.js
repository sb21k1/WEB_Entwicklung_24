document.addEventListener('DOMContentLoaded', function() {
    const signupButton = document.getElementById('signup');
    if (signupButton) {
        signupButton.addEventListener('click', registerUser);
    }
});

document.addEventListener('DOMContentLoaded', function() {
    const signupButton = document.getElementById('login');
    if (signupButton) {
        signupButton.addEventListener('click', loginUser);
    }
});

function registerUser(event) {
    event.preventDefault();
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
    const fullName = document.getElementById('full_name').value;

    fetch('/create_user', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ email, password, full_name: fullName }),
        })
        .then(response => response.json())
        .then(data => {
            if (data.uid) {
                alert('User created successfully');
                window.location.href = '/login';
            } else {
                alert('Error: ' + data.error);
            }
        })
        .catch(error => {
            alert('Error: ' + error.message);
        });
}

document.getElementById('login').addEventListener('click', (e) => {
    e.preventDefault();
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;

    if (!email || !password) {
        alert('Please fill all fields');
        return;
    }

    fetch('/login_user', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ email, password }),
        })
        .then(response => response.json())
        .then(data => {
            if (data.uid) {
                alert('User logged in successfully');
                window.location.href = '/';
            } else {
                alert('Error: ' + data.error);
            }
        })
        .catch(error => {
            alert('Error: ' + error.message);
        });
});


document.addEventListener('DOMContentLoaded', function() {
    const registerForm = document.getElementById('register-form');
    const loginForm = document.getElementById('login-form');

    if (registerForm) {
        registerForm.addEventListener('submit', registerUser);
    }

    if (loginForm) {
        loginForm.addEventListener('login', loginUser);
    }
});