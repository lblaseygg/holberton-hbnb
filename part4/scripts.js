// Authentication check - runs immediately before anything else
(function() {
    // Check if user is logged in
    const isLoggedIn = localStorage.getItem('isLoggedIn') === 'true';
    
    // Get current page
    const currentPath = window.location.pathname;
    
    // List of public pages that don't require authentication
    const publicPages = ['login.html', 'signup.html'];
    const isPublicPage = publicPages.some(page => currentPath.endsWith(page));

    // If not logged in and not on a public page, redirect to login
    if (!isLoggedIn && !isPublicPage) {
        window.location.replace('login.html');
    }
})();

// Authentication check
function isAuthenticated() {
    return localStorage.getItem('isLoggedIn') === 'true';
}

// Initialize test user
function initializeTestUser() {
    const testUser = {
        email: 'test@example.com',
        password: 'password123',
        name: 'Test User'
    };
    localStorage.setItem('users', JSON.stringify([testUser]));
}

// Main initialization
document.addEventListener('DOMContentLoaded', () => {
    // Initialize test user if not already initialized
    if (!localStorage.getItem('users')) {
        initializeTestUser();
    }

    // Only setup page functionality if authenticated
    if (window.auth && window.auth.isAuthenticated()) {
        setupPageFunctionality();
    }
});

// Places management functions
async function fetchPlaces() {
    try {
        const response = await fetch('http://localhost:5001/api/v1/places');
        if (!response.ok) {
            throw new Error(`Failed to fetch places: ${response.status} ${response.statusText}`);
        }
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Error fetching places:', error);
        throw error;
    }
}

function createPlaceElement(place) {
    const placeElement = document.createElement('div');
    placeElement.className = 'place';
    placeElement.dataset.price = place.price;

    placeElement.innerHTML = `
        <h3>${place.name}</h3>
        <p class="description">${place.description}</p>
        <p class="location">Location: ${place.city}, ${place.state}</p>
        <p class="price">$${place.price} per night</p>
        <a href="place.html?id=${place.id}" class="view-details">View Details</a>
    `;

    return placeElement;
}

function displayPlaces(places) {
    const placesList = document.getElementById('places-list');
    if (!placesList) return;

    placesList.innerHTML = ''; // Clear existing content

    if (!places || places.length === 0) {
        placesList.innerHTML = '<p class="no-places">No places available.</p>';
        return;
    }

    places.forEach(place => {
        const placeElement = createPlaceElement(place);
        placesList.appendChild(placeElement);
    });
}

function filterPlaces(price) {
    const places = document.querySelectorAll('.place');
    places.forEach(place => {
        const placePrice = parseFloat(place.dataset.price);
        if (price === 'all' || placePrice <= price) {
            place.style.display = 'block';
        } else {
            place.style.display = 'none';
        }
    });
}

function setupPriceFilter() {
    const priceFilter = document.getElementById('price-filter');
    if (priceFilter) {
        priceFilter.addEventListener('change', (event) => {
            const selectedPrice = event.target.value;
            filterPlaces(selectedPrice === 'all' ? 'all' : parseFloat(selectedPrice));
        });
    }
}

function setupPageFunctionality() {
    // Handle places display if on index page
    if (window.location.pathname.endsWith('index.html')) {
        fetchPlaces()
            .then(places => displayPlaces(places))
            .catch(error => {
                console.error('Error:', error);
                const placesList = document.getElementById('places-list');
                if (placesList) {
                    placesList.innerHTML = '<p class="error">Failed to load places. Please try again later.</p>';
                }
            });

        setupPriceFilter();
    }

    // Handle search and filter functionality
    const searchBox = document.querySelector('.search-box input');
    const searchButton = document.querySelector('.search-box button');
    if (searchBox && searchButton) {
        searchButton.addEventListener('click', function() {
            const searchTerm = searchBox.value;
            if (searchTerm) {
                alert(`Searching for: ${searchTerm}`);
            }
        });
    }

    const filterSelects = document.querySelectorAll('.filter-options select');
    filterSelects.forEach(select => {
        select.addEventListener('change', function() {
            const selectedValue = this.value;
            if (selectedValue) {
                alert(`Filtering by: ${selectedValue}`);
            }
        });
    });
}

function logout() {
    if (window.auth) {
        window.auth.handleLogout();
    }
    window.location.href = 'login.html';
}

// Get current user
function getCurrentUser() {
    const users = JSON.parse(localStorage.getItem('users') || '[]');
    const currentUser = users.find(user => user.email === localStorage.getItem('currentUserEmail'));
    return currentUser || null;
} 