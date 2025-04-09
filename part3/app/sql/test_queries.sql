-- Test 1: Verify admin user exists and has correct attributes
SELECT id, first_name, last_name, email, is_admin
FROM users
WHERE id = '36c9050e-ddd3-4c3b-9731-9f487208bbc1';

-- Test 2: Verify amenities were inserted correctly
SELECT id, name, description
FROM amenities
ORDER BY name;

-- Test 3: Verify sample place exists and has correct attributes
SELECT p.id, p.title, p.description, p.price, p.latitude, p.longitude, u.email as owner_email
FROM places p
JOIN users u ON p.user_id = u.id
WHERE p.id = 'a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a14';

-- Test 4: Verify place-amenity associations
SELECT p.title, a.name as amenity
FROM places p
JOIN place_amenity pa ON p.id = pa.place_id
JOIN amenities a ON pa.amenity_id = a.id
WHERE p.id = 'a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a14'
ORDER BY a.name;

-- Test 5: Verify review exists and has correct attributes
SELECT r.text, r.rating, u.email as reviewer_email, p.title as place_title
FROM reviews r
JOIN users u ON r.user_id = u.id
JOIN places p ON r.place_id = p.id
WHERE r.id = 'a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a15';

-- Test 6: Verify foreign key constraints (should fail)
INSERT INTO places (id, title, description, price, latitude, longitude, user_id)
VALUES (
    'a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a16',
    'Invalid Place',
    'This should fail',
    100.00,
    0.0,
    0.0,
    'invalid-user-id'
);

-- Test 7: Verify unique constraint on user-place review (should fail)
INSERT INTO reviews (id, text, rating, user_id, place_id)
VALUES (
    'a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a17',
    'Duplicate review',
    4,
    '36c9050e-ddd3-4c3b-9731-9f487208bbc1',
    'a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a14'
);

-- Test 8: Verify rating range constraint (should fail)
INSERT INTO reviews (id, text, rating, user_id, place_id)
VALUES (
    'a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a18',
    'Invalid rating',
    6,
    '36c9050e-ddd3-4c3b-9731-9f487208bbc1',
    'a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a14'
); 