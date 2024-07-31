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
                // Hier können Sie weitere Aktionen nach erfolgreicher Registrierung durchführen
            } else {
                alert('Error: ' + data.error);
            }
        })
        .catch(error => {
            alert('Error: ' + error.message);
        });
}

// Funktion zum Einloggen eines Benutzers
function loginUser(event) {
    event.preventDefault();
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;

    fetch('/login', {
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
                // Hier können Sie weitere Aktionen nach erfolgreichem Login durchführen
            } else {
                alert('Error: ' + data.error);
            }
        })
        .catch(error => {
            alert('Error: ' + error.message);
        });
}

// Event Listener für Registrierung und Login
document.getElementById('register').addEventListener('click', registerUser);
document.getElementById('login').addEventListener('click', loginUser);