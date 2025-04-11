// Update main image when thumbnail is clicked
function updateMainImage(src) {
    const mainImage = document.querySelector('.main-image img');
    if (mainImage) {
        mainImage.src = src;
    }

    // Update active state of thumbnails
    const thumbnails = document.querySelectorAll('.thumbnail-grid img');
    thumbnails.forEach(img => {
        img.classList.remove('active');
        if (img.src === src) {
            img.classList.add('active');
        }
    });
} 