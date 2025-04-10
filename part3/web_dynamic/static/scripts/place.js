document.addEventListener('DOMContentLoaded', () => {
    // Get place ID from URL
    const placeId = getPlaceIdFromURL();
    if (!placeId) {
        showError('Place ID not found in URL');
        return;
    }

    // Check authentication and initialize page
    checkAuthentication(placeId);
});

// Function to get cookie value by name
function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
    return null;
}

// Get place ID from URL query parameters
function getPlaceIdFromURL() {
    const urlParams = new URLSearchParams(window.location.search);
    return urlParams.get('id');
}

// Check authentication and control review form visibility
function checkAuthentication(placeId) {
    const token = getCookie('token');
    const addReviewBtn = document.getElementById('add-review-btn');
    const addReviewForm = document.getElementById('add-review-form');

    if (!token) {
        if (addReviewBtn) addReviewBtn.style.display = 'none';
        if (addReviewForm) addReviewForm.style.display = 'none';
    } else {
        if (addReviewBtn) addReviewBtn.style.display = 'block';
        if (addReviewForm) addReviewForm.style.display = 'block';
    }

    fetchPlaceDetails(token, placeId);
}

// Fetch place details from API
async function fetchPlaceDetails(token, placeId) {
    try {
        const response = await fetch(`http://localhost:5001/api/v1/places/${placeId}`, {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${token}`,
                'Accept': 'application/json'
            }
        });

        if (!response.ok) {
            throw new Error('Failed to fetch place details');
        }

        const place = await response.json();
        displayPlaceDetails(place);
    } catch (error) {
        console.error('Error:', error);
        showError('Error loading place details. Please try again later.');
    }
}

// Display place details
function displayPlaceDetails(place) {
    // Update basic information
    document.getElementById('place-name').textContent = place.name;
    document.getElementById('host-name').textContent = place.host?.name || 'Unknown host';
    document.getElementById('price').textContent = `$${place.price_by_night}/night`;
    document.getElementById('description').textContent = place.description || 'No description available';

    // Update amenities
    const amenitiesList = document.getElementById('amenities-list');
    if (amenitiesList) {
        amenitiesList.innerHTML = place.amenities?.map(amenity => `
            <div class="amenity">
                <span class="badge bg-info">${amenity.name}</span>
            </div>
        `).join('') || '<p>No amenities listed</p>';
    }

    // Update reviews
    const reviewsList = document.getElementById('reviews-list');
    if (reviewsList) {
        reviewsList.innerHTML = place.reviews?.map(review => `
            <div class="review-card">
                <h4>${review.user?.name || 'Anonymous'}</h4>
                <p>Rating: ${'★'.repeat(review.rating)}${'☆'.repeat(5 - review.rating)}</p>
                <p>${review.text}</p>
                <small class="text-muted">${new Date(review.created_at).toLocaleDateString()}</small>
            </div>
        `).join('') || '<p>No reviews yet</p>';
    }
}

// Handle review submission
async function submitReview(event) {
    event.preventDefault();
    
    const token = getCookie('token');
    if (!token) {
        showError('You must be logged in to submit a review');
        return;
    }

    const placeId = getPlaceIdFromURL();
    const rating = document.getElementById('rating').value;
    const comment = document.getElementById('comment').value;

    try {
        const response = await fetch(`http://localhost:5001/api/v1/places/${placeId}/reviews`, {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            },
            body: JSON.stringify({
                rating: parseInt(rating),
                text: comment
            })
        });

        if (!response.ok) {
            throw new Error('Failed to submit review');
        }

        // Refresh place details to show the new review
        fetchPlaceDetails(token, placeId);
        
        // Reset form
        event.target.reset();
        showSuccess('Review submitted successfully!');
    } catch (error) {
        console.error('Error:', error);
        showError('Failed to submit review. Please try again.');
    }
}

// Show error message
function showError(message) {
    const errorDiv = document.createElement('div');
    errorDiv.className = 'alert alert-danger';
    errorDiv.textContent = message;
    
    const container = document.querySelector('.container');
    container.insertBefore(errorDiv, container.firstChild);
    
    // Remove error message after 5 seconds
    setTimeout(() => errorDiv.remove(), 5000);
}

// Show success message
function showSuccess(message) {
    const successDiv = document.createElement('div');
    successDiv.className = 'alert alert-success';
    successDiv.textContent = message;
    
    const container = document.querySelector('.container');
    container.insertBefore(successDiv, container.firstChild);
    
    // Remove success message after 5 seconds
    setTimeout(() => successDiv.remove(), 5000);
}

// Add event listener for review form submission
document.getElementById('review-form')?.addEventListener('submit', submitReview); 