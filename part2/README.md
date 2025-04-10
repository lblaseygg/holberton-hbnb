# HBnB Application

## Project Structure
The HBnB application follows a three-layer architecture:

### Presentation Layer (app/api/)
- Contains API endpoints organized by version
- Handles HTTP requests and responses
- Uses Flask-RESTX for API documentation

### Business Logic Layer (app/models/ & app/services/)
- Contains core business logic and domain models
- Implements the Facade pattern for layer communication
- Handles data validation and business rules

### Persistence Layer (app/persistence/)
- Manages data storage and retrieval
- Currently uses in-memory storage
- Will be replaced with SQL Alchemy in Part 3

## Directory Structure 