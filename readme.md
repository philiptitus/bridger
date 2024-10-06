
---

# Pirate API - Django Backend

[![Django](https://img.shields.io/badge/Django-3.2+-brightgreen)](https://www.djangoproject.com/)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](https://github.com/philiptitus/bridger/blob/main/LICENSE)
[![Backend CI](https://github.com/philiptitus/bridger/actions/workflows/backend.yml/badge.svg)](https://github.com/philiptitus/bridger/actions/workflows/backend.yml)

The **Pirate API** is the server-side backbone of the **MsBridger AI Budget Planner** app, responsible for handling all core functionalities, including user management, financial transactions, and communication with the AI engine powered by Google Gemini. This Django-based API delivers high performance, scalability, and security for managing financial data and powering personalized budget insights for users.

---

## 📖 Overview

The **Pirate API** is the powerhouse of the **MsBridger** mobile app, offering a comprehensive backend for handling user data, financial tracking, and budget management. The API is designed using Django’s robust framework to ensure high availability and secure data handling.

This API serves the frontend mobile application, developed using [React Native](https://github.com/philiptitus/MsBridger), and communicates with the **Pirate AI** engine for intelligent financial planning and budget predictions.

### Key Features

- **User Authentication:** Secure user authentication using Django's built-in system, with additional layers for permission management.
- **Income & Expense Management:** Handle income and expense transactions via RESTful APIs, providing a seamless flow for frontend interactions.
- **Budget & Savings Tracking:** Track user budgets, create custom savings plans, and monitor progress through REST endpoints.
- **AI-Driven Financial Insights:** Real-time data integration with the **Google Gemini** AI engine for personalized advice and predictive financial insights.
- **Django Admin Integration:** Full admin interface for managing users, transactions, and AI configurations.
- **RESTful API Architecture:** Follows REST conventions, offering predictable and well-structured routes for all resources.
- **Mobile Frontend Integration:** Seamlessly connects with the [MsBridger mobile app](https://github.com/philiptitus/msbridger-mobile), ensuring smooth data exchange and an intuitive user experience.

---

## 🛠️ Tech Stack

- **Backend Framework:** Django (with Django REST Framework)
- **Database:** PostgreSQL (or SQLite for local development)
- **Authentication:** Token-based authentication (with Django Rest Framework JWT)
- **AI Integration:** Google Gemini (connected via internal services for financial predictions)
- **API Documentation:** Fully documented with [Postman](https://documenter.getpostman.com/view/31401198/2sA3e1AV8h)

---

## 📂 Project Structure

```bash
pirate-api/
├── bridger/                     # Core Django project folder
│   ├── settings.py              # Configuration and settings
│   ├── urls.py                  # Route management
│   ├── wsgi.py                  # WSGI application for deployment
├── api/                         # Main app for handling API logic
│   ├── models.py                # Database models (User, Income, Expenses, Budgets)
│   ├── views.py                 # API view logic (CRUD operations)
│   ├── serializers.py           # Data serialization for API responses
│   ├── urls.py                  # API routing and endpoints
│   └── tests.py                 # Test cases for API functionality
├── manage.py                    # Django's utility script for management commands
├── requirements.txt             # Python dependencies
└── README.md                    # This README file
```

---

## 🔗 Important Links

- **Mobile Frontend Repository:** [MsBridger Mobile App](https://github.com/philiptitus/MsBridger)
- **API Documentation:** [Pirate API Documentation](https://documenter.getpostman.com/view/31401198/2sA3e1AV8h)
- **Backend Source Code:** [Pirate API Repository](https://github.com/philiptitus/bridger)

---

## 🚀 Quick Start

To get the **Pirate API** up and running locally, follow these steps:

### Prerequisites

Ensure you have the following installed on your system:

- Python 3.8+
- PostgreSQL (or SQLite for development)
- Git

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/philiptitus/bridger.git
   cd bridger
   ```

2. Set up a virtual environment and install dependencies:

   ```bash
   python -m venv env
   source env/bin/activate
   pip install -r requirements.txt
   ```

3. Set up your database (adjust your database credentials in `bridger/settings.py`):

   ```bash
   python manage.py migrate
   ```

4. Create a superuser for accessing the Django Admin:

   ```bash
   python manage.py createsuperuser
   ```

5. Run the server:

   ```bash
   python manage.py runserver
   ```

6. Navigate to `http://127.0.0.1:8000` to explore the API!

---

## 📄 API Documentation

Explore the full API documentation, including detailed routes and response formats, through the following link:

[Postman API Documentation](https://documenter.getpostman.com/view/31401198/2sA3e1AV8h)

This documentation includes:

- **Authentication & User Management**
- **Income & Expense Endpoints**
- **Budget Tracking**
- **Savings Plans**
- **AI-Driven Financial Insights**

---

## 📜 License

This project is licensed under the MIT License. See the [LICENSE](https://github.com/philiptitus/bridger/blob/main/LICENSE) file for more details.

---

## 👤 Contributors

- **Philip Titus** - [GitHub](https://github.com/philiptitus)

---

## 🔒 Security

For any security concerns, please contact me at [philip@example.com](mailto:mrphilipowade@gmail.com). I take security seriously and appreciate any vulnerabilities being reported responsibly.

---

## 📝 Copyright

**Pirate API** © 2024 Philip Titus. All rights reserved.
