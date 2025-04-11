// Authentication state management
const AUTH_STORAGE_KEY = 'isLoggedIn';
const CURRENT_USER_KEY = 'currentUserEmail';
const PUBLIC_PAGES = ['login.html', 'signup.html'];
let isNavigating = false;

// Check if current page is public
function isPublicPage() {
    const currentPath = window.location.pathname;
    return PUBLIC_PAGES.some(page => currentPath.endsWith(page));
}

// Check if user is authenticated
function isAuthenticated() {
    return localStorage.getItem(AUTH_STORAGE_KEY) === 'true' && localStorage.getItem(CURRENT_USER_KEY);
}

// Handle authentication state
function handleAuthState() {
    const authenticated = isAuthenticated();
    const isPublic = isPublicPage();

    // If not authenticated and not on a public page, redirect to login
    if (!authenticated && !isPublic) {
        window.location.replace('login.html');
        return;
    }

    // If authenticated and on login/signup page, redirect to index
    if (authenticated && isPublic) {
        window.location.replace('index.html');
        return;
    }
}

// Handle login
function handleLogin(email, password) {
    const users = JSON.parse(localStorage.getItem('users') || '[]');
    const user = users.find(u => u.email === email);

    if (user && user.password === password) {
        localStorage.setItem(AUTH_STORAGE_KEY, 'true');
        localStorage.setItem(CURRENT_USER_KEY, email);
        isNavigating = true;
        return true;
    }
    return false;
}

// Handle signup
function handleSignup(name, email, password) {
    const users = JSON.parse(localStorage.getItem('users') || '[]');
    
    if (users.some(user => user.email === email)) {
        return false;
    }
    
    const newUser = { name, email, password };
    users.push(newUser);
    localStorage.setItem('users', JSON.stringify(users));
    localStorage.setItem(AUTH_STORAGE_KEY, 'true');
    localStorage.setItem(CURRENT_USER_KEY, email);
    isNavigating = true;
    return true;
}

// Handle logout
function handleLogout() {
    localStorage.removeItem(AUTH_STORAGE_KEY);
    localStorage.removeItem(CURRENT_USER_KEY);
}

// Clear auth state when page is closed
window.addEventListener('unload', () => {
    if (!isNavigating) {
        handleLogout();
    }
});

// Initialize authentication
document.addEventListener('DOMContentLoaded', () => {
    // Run initial auth check
    handleAuthState();

    // Handle login form
    const loginForm = document.getElementById('loginForm');
    if (loginForm) {
        loginForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const email = document.getElementById('email').value;
            const password = document.getElementById('password').value;
            
            if (handleLogin(email, password)) {
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

    // Handle signup form
    const signupForm = document.getElementById('signupForm');
    if (signupForm) {
        signupForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const name = document.getElementById('name').value;
            const email = document.getElementById('email').value;
            const password = document.getElementById('password').value;
            const confirmPassword = document.getElementById('confirm-password').value;
            
            if (password !== confirmPassword) {
                alert('Passwords do not match!');
                return;
            }
            
            if (handleSignup(name, email, password)) {
                window.location.href = 'index.html';
            } else {
                alert('Email already registered!');
            }
        });
    }

    // Prevent navigation when not authenticated
    document.addEventListener('click', function(e) {
        const link = e.target.closest('a');
        if (!link) return;

        const href = link.getAttribute('href');
        if (!href) return;

        // Allow navigation to public pages
        if (PUBLIC_PAGES.some(page => href.includes(page))) {
            return;
        }

        // Prevent navigation if not authenticated
        if (!isAuthenticated()) {
            e.preventDefault();
            window.location.href = 'login.html';
        }
    });
});

// Export functions for use in other scripts
window.auth = {
    isAuthenticated,
    handleAuthState,
    handleLogin,
    handleSignup,
    handleLogout
}; 