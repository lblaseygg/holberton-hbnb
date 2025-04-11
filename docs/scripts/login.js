// Initialize test user
function initializeTestUser() {
    const testUser = {
        email: 'test@example.com',
        password: 'password123',
        name: 'Test User'
    };
    localStorage.setItem('users', JSON.stringify([testUser]));
}

// Handle login form submission
document.addEventListener('DOMContentLoaded', () => {
    // Initialize test user
    initializeTestUser();

    const loginForm = document.getElementById('loginForm');
    if (loginForm) {
        loginForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const email = document.getElementById('email').value;
            const password = document.getElementById('password').value;
            
            // Get users from localStorage
            const users = JSON.parse(localStorage.getItem('users')) || [];
            
            // Find user with matching email
            const user = users.find(u => u.email === email);

            if (user && user.password === password) {
                localStorage.setItem('isLoggedIn', 'true');
                window.location.href = 'index.html';
            } else {
                const errorMessage = document.getElementById('error-message');
                if (errorMessage) {
                    errorMessage.textContent = 'Invalid email or password';
                    errorMessage.style.display = 'block';
                }
            }
        });
    }
}); 