document.addEventListener('DOMContentLoaded', () => {
    // Initialize the page
    checkAuthentication();
    initializePriceFilter();
});

// Function to get cookie value by name
function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
    return null;
}

// Check authentication and control login link visibility
function checkAuthentication() {
    const token = getCookie('token');
    const loginLink = document.getElementById('login-link');
    const placesSection = document.getElementById('places-section');

    if (!token) {
        loginLink.style.display = 'block';
        if (placesSection) {
            placesSection.innerHTML = '<p class="text-center">Please log in to view places</p>';
        }
    } else {
        loginLink.style.display = 'none';
        fetchPlaces(token);
    }
}

// Fetch places from the API
async function fetchPlaces(token) {
    try {
        const response = await fetch('http://localhost:5001/api/v1/places', {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${token}`,
                'Accept': 'application/json'
            }
        });

        if (!response.ok) {
            throw new Error('Failed to fetch places');
        }

        const places = await response.json();
        window.placesData = places; // Store places data globally for filtering
        displayPlaces(places);
    } catch (error) {
        console.error('Error:', error);
        document.getElementById('places-list').innerHTML = 
            '<p class="text-danger">Error loading places. Please try again later.</p>';
    }
}

// Display places in the list
function displayPlaces(places) {
    const placesList = document.getElementById('places-list');
    placesList.innerHTML = ''; // Clear current content

    if (!places || places.length === 0) {
        placesList.innerHTML = '<p class="text-center">No places available</p>';
        return;
    }

    places.forEach(place => {
        const placeElement = document.createElement('div');
        placeElement.className = 'place-item';
        placeElement.dataset.price = place.price_by_night;
        
        placeElement.innerHTML = `
            <div class="card mb-3">
                <div class="card-body">
                    <h5 class="card-title">${place.name}</h5>
                    <h6 class="card-subtitle mb-2 text-muted">$${place.price_by_night}/night</h6>
                    <p class="card-text">${place.description || 'No description available'}</p>
                    <div class="place-details">
                        <span class="badge bg-info">${place.max_guest} Guest${place.max_guest !== 1 ? 's' : ''}</span>
                        <span class="badge bg-info">${place.number_rooms} Room${place.number_rooms !== 1 ? 's' : ''}</span>
                        <span class="badge bg-info">${place.number_bathrooms} Bathroom${place.number_bathrooms !== 1 ? 's' : ''}</span>
                    </div>
                    <p class="card-text"><small class="text-muted">Location: ${place.city?.name || 'Unknown location'}</small></p>
                </div>
            </div>
        `;
        
        placesList.appendChild(placeElement);
    });
}

// Initialize price filter
function initializePriceFilter() {
    const priceFilter = document.getElementById('price-filter');
    if (!priceFilter) return;

    // Add price filter options
    const prices = ['All', '10', '50', '100'];
    prices.forEach(price => {
        const option = document.createElement('option');
        option.value = price;
        option.textContent = price === 'All' ? 'All Prices' : `$${price} or less`;
        priceFilter.appendChild(option);
    });

    // Add event listener for price filter
    priceFilter.addEventListener('change', (event) => {
        const selectedPrice = event.target.value;
        filterPlacesByPrice(selectedPrice);
    });
}

// Filter places by price
function filterPlacesByPrice(maxPrice) {
    const places = document.querySelectorAll('.place-item');
    
    places.forEach(place => {
        const price = parseInt(place.dataset.price);
        if (maxPrice === 'All' || price <= parseInt(maxPrice)) {
            place.style.display = 'block';
        } else {
            place.style.display = 'none';
        }
    });
}

// Add logout functionality
document.getElementById('logout-link')?.addEventListener('click', (event) => {
    event.preventDefault();
    document.cookie = 'token=; path=/; expires=Thu, 01 Jan 1970 00:00:01 GMT;';
    window.location.href = 'login.html';
}); 