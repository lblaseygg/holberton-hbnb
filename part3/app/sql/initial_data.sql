-- Insert admin user
-- Password hash for 'admin1234' generated using bcrypt
INSERT INTO users (id, first_name, last_name, email, password, is_admin)
VALUES (
    '36c9050e-ddd3-4c3b-9731-9f487208bbc1',
    'Admin',
    'HBnB',
    'admin@hbnb.io',
    '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewKy7P2p5KQwHq4y',
    TRUE
);

-- Insert initial amenities
INSERT INTO amenities (id, name, description) VALUES
    ('a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11', 'WiFi', 'High-speed wireless internet access'),
    ('a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a12', 'Swimming Pool', 'Outdoor swimming pool'),
    ('a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a13', 'Air Conditioning', 'Central air conditioning system');

-- Insert a sample place (owned by admin)
INSERT INTO places (id, title, description, price, latitude, longitude, user_id)
VALUES (
    'a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a14',
    'Luxury Villa',
    'Beautiful villa with ocean view',
    250.00,
    37.7749,
    -122.4194,
    '36c9050e-ddd3-4c3b-9731-9f487208bbc1'
);

-- Associate amenities with the sample place
INSERT INTO place_amenity (place_id, amenity_id) VALUES
    ('a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a14', 'a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11'),
    ('a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a14', 'a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a12'),
    ('a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a14', 'a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a13');

-- Insert a sample review
INSERT INTO reviews (id, text, rating, user_id, place_id)
VALUES (
    'a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a15',
    'Amazing place with great amenities!',
    5,
    '36c9050e-ddd3-4c3b-9731-9f487208bbc1',
    'a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a14'
); 