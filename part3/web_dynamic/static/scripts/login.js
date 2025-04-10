document.addEventListener('DOMContentLoaded', () => {
    const loginForm = document.getElementById('login-form');
    const errorMessage = document.getElementById('error-message');
    const submitButton = loginForm ? loginForm.querySelector('button[type="submit"]') : null;

    function showError(message) {
        errorMessage.textContent = message;
        errorMessage.style.display = 'block';
        errorMessage.style.color = 'red';
        errorMessage.style.marginBottom = '10px';
    }

    function clearError() {
        errorMessage.style.display = 'none';
        errorMessage.textContent = '';
    }

    if (loginForm) {
        loginForm.addEventListener('submit', async (event) => {
            event.preventDefault();
            clearError();

            // Get form data
            const email = document.getElementById('email').value.trim();
            const password = document.getElementById('password').value;

            // Basic validation
            if (!email) {
                showError('Please enter your email address');
                return;
            }
            if (!password) {
                showError('Please enter your password');
                return;
            }

            // Disable submit button and show loading state
            if (submitButton) {
                submitButton.disabled = true;
                submitButton.textContent = 'Logging in...';
            }

            try {
                // Make API request
                const response = await fetch('http://localhost:5001/api/v1/auth/login', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'Accept': 'application/json'
                    },
                    credentials: 'include', // Include cookies in the request
                    body: JSON.stringify({ email, password })
                });

                const data = await response.json();

                if (!response.ok) {
                    throw new Error(data.error || 'Invalid email or password');
                }

                // Store token in cookie
                const secure = window.location.protocol === 'https:' ? 'secure;' : '';
                document.cookie = `token=${data.access_token}; path=/; ${secure} SameSite=Lax`;
                
                // Redirect to main page
                window.location.href = 'index.html';
            } catch (error) {
                console.error('Error:', error);
                showError(error.message || 'An error occurred. Please try again.');
            } finally {
                // Re-enable submit button
                if (submitButton) {
                    submitButton.disabled = false;
                    submitButton.textContent = 'Login';
                }
            }
        });
    }
}); 