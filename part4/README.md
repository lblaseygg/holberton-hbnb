# Part 4 - Simple Web Client

## Overview
This phase focuses on the front-end development of the application using HTML5, CSS3, and JavaScript ES6. The goal is to design and implement an interactive user interface that seamlessly connects with the back-end services developed in previous parts of the project.

## Objectives
- Develop a user-friendly interface following provided design specifications
- Implement client-side functionality to interact with the back-end API
- Ensure secure and efficient data handling using JavaScript
- Apply modern web development practices to create a dynamic web application

## Learning Goals
- Understand and apply HTML5, CSS3, and JavaScript ES6 in a real-world project
- Learn to interact with back-end services using AJAX/Fetch API
- Implement authentication mechanisms and manage user sessions
- Use client-side scripting to enhance user experience without page reloads

## Tasks Breakdown

### Task 1: Design
- Complete provided HTML and CSS files to match the given design specifications
- Create pages for:
  - Login
  - List of Places
  - Place Details
  - Add Review

### Task 2: Login
- Implement login functionality using the back-end API
- Store the JWT token returned by the API in a cookie for session management

### Task 3: List of Places
- Implement the main page to display a list of all places
- Fetch places data from the API
- Implement client-side filtering based on country selection
- Ensure the page redirects to the login page if the user is not authenticated

### Task 4: Place Details
- Implement the detailed view of a place
- Fetch place details from the API using the place ID
- Provide access to the add review form if the user is authenticated

### Task 5: Add Review
- Implement the form to add a review for a place
- Ensure the form is accessible only to authenticated users
- Redirect unauthenticated users to the index page

## CORS Configuration
When testing your client against your API, you may encounter Cross-Origin Resource Sharing (CORS) errors. You'll need to modify your API code to allow your client to fetch data from the API. Refer to the [CORS documentation](https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS) for a deeper understanding of CORS and how to configure your Flask API.

## Resources
- [HTML5 Documentation](https://developer.mozilla.org/en-US/docs/Web/HTML)
- [CSS3 Documentation](https://developer.mozilla.org/en-US/docs/Web/CSS)
- [JavaScript ES6 Features](https://developer.mozilla.org/en-US/docs/Web/JavaScript/New_in_JavaScript/ECMAScript_6_support_in_Mozilla)
- [Fetch API](https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API)
- [Responsive Web Design Basics](https://developer.mozilla.org/en-US/docs/Learn/CSS/CSS_layout/Responsive_Design)
- [Handling Cookies in JavaScript](https://developer.mozilla.org/en-US/docs/Web/API/Document/cookie)
- [Client-Side Form Validation](https://developer.mozilla.org/en-US/docs/Learn/Forms/Form_validation)

## Getting Started
1. Ensure your back-end API is running and properly configured for CORS
2. Open the HTML files in a modern web browser
3. Test the authentication flow and ensure proper session management
4. Verify all API endpoints are accessible and returning expected data
5. Test the filtering and review functionality

## Notes
- Make sure to handle all edge cases and error scenarios gracefully
- Implement proper error messages and user feedback
- Ensure the application is responsive and works well on different screen sizes
- Follow security best practices when handling user data and authentication 