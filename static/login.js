document.addEventListener('DOMContentLoaded', function() {
    const loginForm = document.querySelector('form');

    loginForm.addEventListener('submit', function(event) {
        event.preventDefault();

        const username = document.getElementById('username').value;
        const password = document.getElementById('password').value;

        // Simple client-side validation (optional)
        if (username === 'admin' && password === 'password') {
            // Redirect to home page if credentials are correct
            window.location.href = '/home';
        } else {
            // Show an error message
            document.getElementById('login-message').innerText = 'Invalid username or password';
        }
    });
});
