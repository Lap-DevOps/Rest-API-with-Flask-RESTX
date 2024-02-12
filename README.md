# Flask REST API with Flask-RESTX

This repository contains a simple Flask REST API built with Flask-RESTX. It provides endpoints for user authentication and managing orders.

## Installation

1. Clone the repository:

   ```bash
   git clone <repository_url> 
   ```
   
2. Navigate to the project directory:

```bash
    Copy code
    cd <project_directory>
```
    
3. Install dependencies:

```bash
    Copy code
    pip install -r requirements.txt
    Configuration
    The application uses configuration settings from the config module. By default, it uses the development configuration. You can modify the configuration in the config.py file.
```
4. Usage
Run the Flask application:

```bash
Copy code
flask run

```
5. Access the Swagger documentation to explore available endpoints:

http://localhost:5000/docs

6. Endpoints
Authentication
/auth/register - Register a new user
/auth/login - Log in and obtain an access token
/auth/logout - Log out and revoke the access token
7. Orders
/orders - Get all orders or create a new order
/orders/<order_id> - Get, update, or delete a specific order
8. Error Handling
404 Not Found - Resource not found
405 Method Not Allowed - Method not allowed for the requested URL
9. Database Models
User - Represents a user in the system
Order - Represents an order placed by a user
10. Shell Context
The Flask application provides a shell context with access to the database and models. You can use the following objects in the shell:

db - SQLAlchemy database instance
User - User model class
Order - Order model class

11. License
This project is licensed under the MIT License. See the LICENSE file for details.