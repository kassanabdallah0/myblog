# My Blog

[![Python Version](https://img.shields.io/badge/python-3.x-blue.svg)](https://www.python.org/)
[![Django Version](https://img.shields.io/badge/django-4.x-green.svg)](https://www.djangoproject.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A comprehensive Django-based blog site where users can read articles, stay updated with events, and contact the site admin. This project includes user authentication, JWT-based API authentication, and full backend functionality using Django.

## Table of Contents

- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Running the Project](#running-the-project)
- [Running with Daphne](#running-with-daphne)
- [MailHog Setup](#mailhog-setup)
- [Nginx Setup](#nginx-setup)
- [Managing Static and Media Files](#managing-static-and-media-files)
- [Running Tests](#running-tests)
- [API Documentation](#api-documentation)

## Features

- **User Authentication:** JWT for API authentication and session-based authentication for web login.
- **Article Management:** Create, view, update, and delete articles with images.
- **Event Management:** Manage events with start and end dates and images.
- **Contact Form:** Submit contact requests with email and message.
- **Responsive Design:** The site is responsive and mobile-friendly.
- **Swagger API Documentation:** Integrated API documentation using drf_yasg.
- **Asynchronous Support:** Serve the project asynchronously using Daphne.

## Prerequisites

- Python 3.x
- pip
- Virtualenv (recommended)
- Nginx (for production)
- MailHog (for local email testing)
- Daphne (for ASGI support)

## Installation

1. **Clone the repository:**

    ```bash
    git clone https://github.com/kassanabdallah0/myblog.git
    cd myblog
    ```

2. **Create a virtual environment:**

    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install the dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4. **Set up environment variables:**

    Create a `.env` file in the root directory and add the necessary environment variables.

    ```bash
    cp .env.example .env
    ```

    Edit `.env` to include your configurations.

5. **Apply migrations:**

    ```bash
    python manage.py migrate
    ```

6. **Create a superuser:**

    ```bash
    python manage.py createsuperuser
    ```

7. **Collect static files:**

    ```bash
    python manage.py collectstatic
    ```

## Running the Project

1. **Run the development server:**

    ```bash
    python manage.py runserver
    ```

    Visit the site at `http://127.0.0.1:8000`.

2. **Access the Admin Panel:**

    Visit `http://127.0.0.1:8000/admin` to manage articles, events, and users.

## Running with Daphne

Daphne is used to serve your Django application asynchronously whith nginx.

1. **Install Daphne:**

    ```bash
    pip install daphne
    ```

2. **Run Daphne server:**

    ```bash
    daphne -b 0.0.0.0 -p 8000 my_blog.asgi:application
    ```

    This command will serve your project at `http://127.0.0.1:8000` with asynchronous support.

## MailHog Setup

MailHog is used to test email functionality locally.

1. **Install MailHog:**

    - For Linux:

      ```bash
      wget https://github.com/mailhog/MailHog/releases/download/v1.0.0/MailHog_linux_amd64
      chmod +x MailHog_linux_amd64
      sudo mv MailHog_linux_amd64 /usr/local/bin/mailhog
      ```

    - For macOS:

      ```bash
      brew install mailhog
      ```

2. **Run MailHog:**

    ```bash
    mailhog
    ```

3. **Configure Django to use MailHog:**

    In your `settings.py` or `.env`, add:

    ```python
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    EMAIL_HOST = 'localhost'
    EMAIL_PORT = 1025
    ```

4. **Access MailHog Web UI:**

    Visit `http://127.0.0.1:8025` to see the emails.

## Nginx Setup

To serve your Django application in production, set up Nginx:

1. **Install Nginx:**

    ```bash
    sudo apt update
    sudo apt install nginx
    ```

2. **Create an Nginx configuration file:**

    ```bash
    sudo nano /etc/nginx/sites-available/my_blog_project
    ```

    Add the following configuration:

    ```nginx
    server {
        listen 80;
        server_name your_domain_or_IP;

        location /static/ {
            alias /path/to/your/staticfiles/;
        }

        location /media/ {
            alias /path/to/your/mediafiles/;
        }

        location / {
            proxy_pass http://127.0.0.1:8000;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }
    }
    ```

3. **Enable the site and restart Nginx:**

    ```bash
    sudo ln -s /etc/nginx/sites-available/my_blog_project /etc/nginx/sites-enabled/
    sudo nginx -t
    sudo systemctl restart nginx
    ```

## Managing Static and Media Files

1. **Collect static files:**

    ```bash
    python manage.py collectstatic
    ```

2. **Serve media files:**

    Ensure your Nginx configuration correctly points to your media files:

    ```nginx
    location /media/ {
        alias /path/to/your/mediafiles/;
    }
    ```

## Running Tests

1. **Run all tests:**

    ```bash
    python manage.py test
    ```

2. **Testing with static and media files:**

    Ensure that static and media files are properly configured before running the tests.

## API Documentation

1. **Swagger API Documentation:**

    The Swagger UI can be accessed at `http://127.0.0.1:8000/swagger/`.

2. **ReDoc API Documentation:**

    The ReDoc UI can be accessed at `http://127.0.0.1:8000/redoc/`.
