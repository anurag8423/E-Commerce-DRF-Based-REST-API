# E-commerce API

[![Django](https://img.shields.io/badge/Django-5.7-brightgreen.svg)](https://www.djangoproject.com/)
[![DRF](https://img.shields.io/badge/DRF-3.16-blue.svg)](https://www.django-rest-framework.org/)
[![Redis](https://img.shields.io/badge/Redis-5.2-red.svg)](https://redis.io/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-blue.svg)](https://www.postgresql.org/)

A robust e-commerce backend API built with Django REST Framework featuring:

- User authentication with JWT
- Product catalog management
- Shopping cart functionality
- Order processing system
- Redis caching layer
- Performance optimizations
- Pagination and Filter

## Features

- **User Management**
  - Registration & Authentication (JWT)
  - Profile management
  - Order history tracking
  
- **Product System**
  - Category organization
  - Inventory tracking
  - Product variants
  - Search & filtering

- **Order System**
  - Cart management
  - Checkout process
  - Order status tracking

- **Optimizations**
  - Redis caching
  - Database query optimization
  - Pagination

## Requirements

- Python 3.9+
- Redis 7.0+
- PostgreSQL 13+

## Installation

1. #### Clone repository:
   ```bash
   git clone https://github.com/anurag8423/E-Commerce-DRF-Based-REST-API.git
   cd E-Commerce-DRF-Based-REST-API

2. #### Create a Virtual Environment:
   ```bash
   python3 -m venv virtual

3. #### Activate the Virtual Environment:
   - On Windows:
     ```bash
     virtual\Scripts\activate
     
   - On macOS/Linux:
     ```bash
     virtual/bin/activate

5. #### Install Dependencies:
   ```bash
   pip install -r requirements.txt

6. #### Make Databse Migrations:
   ```bash
   pip manage.py makemigrations

7. ## Apply Database Migrations:
   ```bash
   python manage.py migrate

9. ## Create Superuser (if needed):
   ```bash
   python manage.py createsuperuser

11. #### Run the Development Server:
    ```bash
    python manage.py runserver

12. #### Access the Application:
    Open a web browser and go to `http://127.0.0.1:8000/` to view the application.

13. #### Access the Admin Panel:
    If you created a superuser, you can access the admin panel at `http://127.0.0.1:8000/admin/` and log in using the superuser credentials.

14. #### Deactivate the Virtual Environment:
    When you're done working on the project, deactivate the virtual environment.
    ```bash
    deactivate

## Important Note:

**Database Configuration Notice**  

Before running the project, you **must** update the PostgreSQL database settings in:  

`ecommerce/settings.py`  

Replace these values with your local PostgreSQL credentials:  

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'your_db_name',      # Replace with your database name
        'USER': 'your_db_user',      # Replace with your PostgreSQL username  
        'PASSWORD': 'your_db_pass',  # Replace with your PostgreSQL password
        'HOST': 'localhost',         # Update if using a remote host
        'PORT': '5432',              # Default PostgreSQL port
    }
}
```

**Or** configure these values in your `.env` file if using environment variables.  

*(The project won't run until you do this!)*  


