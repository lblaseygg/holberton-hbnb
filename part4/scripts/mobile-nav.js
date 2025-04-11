// Mobile Navigation
function setupMobileNavigation() {
    const mobileMenuButton = document.querySelector('.mobile-menu-button');
    const nav = document.querySelector('nav');
    
    if (mobileMenuButton && nav) {
        // Toggle menu on button click
        mobileMenuButton.addEventListener('click', (event) => {
            event.stopPropagation();
            nav.classList.toggle('active');
            mobileMenuButton.classList.toggle('active');
        });

        // Close menu when clicking outside
        document.addEventListener('click', (event) => {
            if (!nav.contains(event.target) && !mobileMenuButton.contains(event.target)) {
                nav.classList.remove('active');
                mobileMenuButton.classList.remove('active');
            }
        });

        // Close menu when clicking a link
        nav.querySelectorAll('a').forEach(link => {
            link.addEventListener('click', () => {
                nav.classList.remove('active');
                mobileMenuButton.classList.remove('active');
            });
        });
    }
}

// Initialize mobile navigation when the DOM is loaded
document.addEventListener('DOMContentLoaded', setupMobileNavigation);

// Also try to initialize if the DOM is already loaded
if (document.readyState === 'complete' || document.readyState === 'interactive') {
    setupMobileNavigation();
} 