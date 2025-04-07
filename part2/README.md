# HBnB - Part 2: Implementation of Business Logic and API Endpoints

## Project Overview
This repository contains Part 2 of the HBnB Project, focusing on the implementation of the Business Logic and API Endpoints. This phase builds upon the design developed in Part 1, bringing the application to life through Python and Flask implementation.

## Project Structure
The project is organized into a modular architecture following Python and Flask best practices:

```
hbnb/
├── api/
│   ├── __init__.py
│   ├── v1/
│   │   ├── __init__.py
│   │   ├── app.py
│   │   ├── views/
│   │   └── models/
├── models/
│   ├── __init__.py
│   ├── user.py
│   ├── place.py
│   ├── review.py
│   └── amenity.py
├── tests/
└── README.md
```

## Objectives
By the end of this project, you will be able to:

1. **Set Up Project Structure**
   - Organize the project into a modular architecture
   - Create packages for Presentation and Business Logic layers

2. **Implement Business Logic Layer**
   - Develop core classes (User, Place, Review, Amenity)
   - Implement entity relationships
   - Apply facade pattern for layer communication

3. **Build RESTful API Endpoints**
   - Implement CRUD operations for all entities
   - Use flask-restx for API documentation
   - Handle data serialization and extended attributes

4. **Test and Validate API**
   - Ensure proper endpoint functionality
   - Handle edge cases appropriately
   - Validate API responses

## Project Vision and Scope
This implementation focuses on creating a functional and scalable foundation for the application:

- **Presentation Layer**: Services and API endpoints using Flask and flask-restx
- **Business Logic Layer**: Core models and logic driving application functionality

## Learning Objectives
- Modular Design and Architecture
- API Development with Flask and flask-restx
- Business Logic Implementation
- Data Serialization and Composition Handling
- Testing and Debugging

## Technical Stack
- Python 3.x
- Flask
- flask-restx
- SQLAlchemy (for database operations)
- Pytest (for testing)

## Getting Started
1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Set up the development environment
4. Run the application:
   ```bash
   python -m api.v1.app
   ```

## API Documentation
The API documentation is available at `/api/v1/docs` when running the application.

## Testing
Run the test suite:
```bash
python -m pytest tests/
```

## Resources
- [Flask Official Documentation](https://flask.palletsprojects.com/)
- [flask-restx Documentation](https://flask-restx.readthedocs.io/)
- [RESTful API Design Best Practices](https://www.vinaysahni.com/best-practices-for-a-pragmatic-restful-api)
- [Python Project Structure](https://docs.python-guide.org/writing/structure/)

## Next Steps
- Part 3 will focus on implementing JWT authentication and role-based access control
- Integration of the services layer with the database
- Implementation of additional features and optimizations

## License
This project is part of the Holberton School curriculum. 