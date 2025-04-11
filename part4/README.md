# HBNB Web Application - Part 4

A modern, responsive web application for browsing and booking places to stay, built with HTML, CSS, and JavaScript.

## Features

- **User Authentication**
  - Secure login and signup functionality
  - Session management with localStorage
  - Automatic logout on browser close
  - Protected routes for authenticated users

- **Place Management**
  - Browse available places
  - Filter places by price
  - View detailed place information
  - Responsive image gallery

- **Reviews System**
  - Add reviews for places
  - View existing reviews
  - Rating system

- **Modern UI/UX**
  - Apple-inspired design system
  - Responsive layout for all devices
  - Smooth animations and transitions
  - Intuitive navigation

## Project Structure

```
part4/
├── index.html          # Home page
├── login.html          # Login page
├── signup.html         # Signup page
├── place.html          # Place details page
├── add_review.html     # Add review page
├── about_us.html       # About us page
├── styles.css          # Main stylesheet
├── images/             # Image assets
│   ├── logo.png
│   └── icon.png
└── scripts/
    ├── auth.js         # Authentication logic
    ├── login.js        # Login form handling
    ├── signup.js       # Signup form handling
    ├── place.js        # Place details functionality
    └── add_review.js   # Review form handling
```

## Getting Started

1. Clone the repository
2. Open `index.html` in your web browser
3. Use the following test credentials to log in:
   - Email: test@example.com
   - Password: password123

## Authentication Flow

1. **Login**
   - Enter email and password
   - Successful login redirects to home page
   - Failed login shows error message

2. **Signup**
   - Enter name, email, and password
   - Password confirmation required
   - Email uniqueness validation
   - Successful signup redirects to home page

3. **Session Management**
   - Authentication state persists during navigation
   - Automatic logout when browser is closed
   - Protected routes redirect to login when not authenticated

## Browser Compatibility

- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)

## Technologies Used

- HTML5
- CSS3
- JavaScript (ES6+)
- localStorage for state management
- Font Awesome for icons

## Security Features

- Client-side authentication
- Protected routes
- Secure password handling
- Session management
- Automatic logout on browser close

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 