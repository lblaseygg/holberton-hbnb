// Handle review form submission
document.addEventListener('DOMContentLoaded', () => {
    const reviewForm = document.getElementById('reviewForm');
    if (reviewForm) {
        reviewForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            // Get form values
            const rating = document.getElementById('rating').value;
            const comment = document.getElementById('comment').value;
            
            // Here you would typically send the review to a server
            // For now, we'll just show a success message
            alert('Review submitted successfully!');
            window.location.href = 'place.html';
        });
    }

    // Handle cancel button
    const cancelButton = document.querySelector('.cancel-button');
    if (cancelButton) {
        cancelButton.addEventListener('click', function() {
            window.location.href = 'place.html';
        });
    }
}); 