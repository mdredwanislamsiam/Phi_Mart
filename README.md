Below is a **professional, production-ready README.md** tailored for a **Django REST Framework e-commerce backend** like **Phi_Mart**, reflecting your actual stack (DRF, JWT via Djoser, Swagger via drf_yasg).
You can copy this directly into your `README.md` and adjust URLs or settings names if needed.

---

# 🛒 Phi_Mart — E-Commerce Backend API

**Phi_Mart** is a scalable and secure **e-commerce backend API** built using **Django REST Framework (DRF)**.
It provides RESTful endpoints for managing products, categories, carts, orders, and user authentication using **JWT**.
The project is fully documented with **Swagger (OpenAPI)** for easy testing and integration.

---

## Features

* **Product Management**

  * Create, retrieve, update, and delete products
  * Product categorization support

* **Category Management**

  * Hierarchical and reusable categories
  * Category-wise product filtering

* **Cart System**

  * Add/remove products to cart
  * Quantity management
  * User-specific carts

* **Order Management**

  * Create orders from cart

* **Authentication & Authorization**

  * JWT-based authentication
  * Implemented using **Djoser**

* **API Documentation**

  * Interactive Swagger UI
  * OpenAPI schema generation using **drf_yasg**

---

## 🧰 Tech Stack

| Technology            | Description                     |
| --------------------- | ------------------------------- |
| Python                | Core programming language       |
| Django                | Web framework                   |
| Django REST Framework | RESTful API development         |
| Djoser                | Authentication & JWT handling   |
| SimpleJWT             | Token-based authentication      |
| drf_yasg              | Swagger / OpenAPI documentation |
---

## 📁 Project Structure (Simplified)

```
Phi_Mart/
│
├── accounts/        # Authentication & user management
├── products/        # Product & category APIs
├── cart/            # Cart logic
├── orders/          # Order processing
├── core/            # Core settings and utilities
├── manage.py
└── requirements.txt
```

---

## ⚙️ Installation & Setup

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/mdredwanislamsiam/Phi_Mart.git
cd Phi_Mart
```

### 2️⃣ Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate   # Linux / macOS
venv\Scripts\activate      # Windows
```

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Configure Environment Variables

Create a `.env` file (if applicable):

```env
SECRET_KEY=your_secret_key
DEBUG=True
```

### 5️⃣ Apply Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 6️⃣ Create Superuser

```bash
python manage.py createsuperuser
```

### 7️⃣ Run Development Server

```bash
python manage.py runserver
```

---

## 🔐 Authentication (JWT)

JWT authentication is implemented using **Djoser** and **SimpleJWT**.

### Token Endpoints

| Endpoint             | Method | Description                    |
| -------------------- | ------ | ------------------------------ |
| `api/auth/jwt/create/`  | POST   | Obtain access & refresh tokens |
| `api/auth/jwt/refresh/` | POST   | Refresh access token           |
| `api/auth/jwt/verify/`  | POST   | Verify token                   |
| `api/auth/users/`       | POST   | Register new user              |

Add token to request headers:

```
Authorization: Bearer <access_token>
```

---

## 📚 API Documentation (Swagger)

Interactive API documentation is available at:

```
http://127.0.0.1:8000/swagger/
```

Alternative Redoc view:

```
http://127.0.0.1:8000/redoc/
```

Swagger is generated using **drf_yasg** and includes:

* Authentication endpoints
* Product, cart, and order APIs
* Request/response schemas

---

## 🧪 Example API Endpoints

| Resource   | Endpoint           |
| ---------- | ------------------ |
| Products   | `/api/products/`   |
| Categories | `/api/categories/` |
| Cart       | `/api/cart/`       |
| Orders     | `/api/orders/`     |

(Exact URLs may vary based on routing configuration.)

---

## 🔒 Security Considerations

* JWT authentication for protected routes
* User-specific data isolation
* Django permissions & serializers validation
* CSRF protection disabled only for API usage

---

## 📌 Future Improvements

* Payment gateway integration
* Product reviews & ratings
* Inventory management
* Admin dashboard frontend
* Caching with Redis
* Dockerization

---

## 👨‍💻 Author

**Redwan Islam Siam**

Backend Developer | Django & DRF Enthusiast

---

## 📄 License

This project is licensed under the **MIT License**.
You are free to use, modify, and distribute it.

