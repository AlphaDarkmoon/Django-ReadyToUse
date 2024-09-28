# Authentication System

A fully functional authentication system built with Django and Python.

## Description

This authentication system utilizes Django, along with Celery and Redis, to manage asynchronous email handling efficiently. It includes the following features:

- **User Registration:** Allows users to create an account.
- **User Login:** Enables users to log into their accounts securely.
- **Email Verification:** Sends a verification email to users upon registration.
- **Password Recovery:** Facilitates password reset via email.
- **Custom Email Templates:** Utilizes tailored email templates for a better user experience.


## Getting Started

To set up the authentication system, you'll need to install the following dependencies:

### Dependencies

- **Django:** A high-level Python web framework for rapid development.
- **Celery:** An asynchronous task queue/job queue that is focused on real-time operation.
- **Redis:** An in-memory data structure store, used as a message broker for Celery.
- **Python Decouple:** A library to help you manage settings in a simple way, keeping your configurations separate from your code.

### Installation

* Clone Repository ```git clone https://github.com/AlphaDarkmoon/Django-ReadyToUse.git```
* Go to `Auth_webApp` directory 
* Install all requirements from ```requiremtns.txt``` file

To install the required dependencies, you can use pip:

```bash
pip install django celery redis python-decouple
```

### Executing Commands

To set up and run the authentication system, execute the following commands:

- **Make Migrations:**
    ```bash
    python manage.py makemigrations
    ```

- **Migrate the Project Database:**
    ```bash
    python manage.py migrate
    ```

- **Create a Superuser Account:**
    Follow the on-screen instructions to set up an admin account.
    ```bash
    python manage.py createsuperuser
    ```

- **Start the Celery Worker:**
    ```bash
    celery -A Auth_webApp worker --loglevel=info
    ```

- **Start Redis Server:**
    ```bash
    redis-server
    ```

- **Start the Django Development Server:**
    ```bash
    python manage.py runserver
    ```

## Help

For detailed modification instructions, please refer to the `instructions.md` file.

## Authors

- [AlphaDarkmoon](https://github.com/AlphaDarkmoon)

