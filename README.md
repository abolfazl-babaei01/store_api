# Store API

## 📝 Project Overview

This project is a **RESTful API** developed using **Django Rest Framework**.  
It serves as the backend for both **mobile apps** and **web-based e-commerce platforms**.

The goal of this project is to follow **REST architecture principles** and implement **clean code practices** throughout
the codebase. It provides all the necessary endpoints for a store application, including user management, product
handling, and other e-commerce features.

This API is designed to be easily scalable and maintainable, and can be connected to any frontend or mobile app that
communicates via HTTP.

---

## ⚙️ How to Set Up the Project

Follow the steps below to set up and run the project locally:

1. **Clone the repository:**

```bash
git clone https://github.com/abolfazl-babaei01/store_api.git
cd store_api
```

2. **Create a virtual environment:**

```bash
py -3.12 -m venv venv
```

Or Use this :

```bash
python -m venv venv
```

3. **Activate the virtual environment:**
   On Windows:

```bash
venv\Scripts\activate
```

On macOS/Linux:

```bash
source venv/bin/activate
```

4. **Install the dependencies:**

```bash
pip install -r requirements.txt
```

5. **Create initial migrations (since migration files are not included in the repo):**

```bash
python manage.py makemigrations
```

6. **Apply the migrations:**

```bash
python manage.py migrate
```

7. **Run the development server:**

```bash
python manage.py runserver
```
## 📚 API Documentation

This project includes interactive and auto-generated API documentation using **Swagger UI** and **Redoc**.

After running the server, you can access the documentation at the following URLs:

- **Swagger UI**:  
  [http://localhost:8000/schema/swagger-ui/](http://localhost:8000/schema/swagger-ui/)

- **Redoc**:  
  [http://localhost:8000/schema/redoc/](http://localhost:8000/schema/redoc/)

These interfaces allow you to explore, test, and understand all available endpoints and their request/response formats.
They are extremely helpful for both frontend developers and API testers.

## 👤 Create a Superuser (Admin)

To create an admin user (superuser), run the following command:

```bash
python manage.py createsuperuser
```
- **You will be prompted to enter a username and password.**
- **💡 Note: Email address is optional (you can skip it).**

This user is essential for accessing Django’s built-in admin panel, where you can manage your models (like users, products, etc.) through a user-friendly web interface.

After creating the superuser, start the development server if it's not already running:
```bash
python manage.py runserver
```
- **Admin panel**:
  [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)

and log in with the credentials you created.

