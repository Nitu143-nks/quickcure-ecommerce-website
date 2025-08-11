# **QuickCure eCommerce Website** 🛒💊

QuickCure is a **full-stack Python eCommerce platform** built with **Django** for buying and selling medicines online. It offers a smooth shopping experience for customers, a robust admin panel for managing inventory, and a **secure payment gateway** for transactions.

---

## **🚀 Features**

### **User Features**

* 🛍 **Browse & Search Medicines** – Easy product discovery with search functionality.
* 📝 **User Registration & Login** – Secure authentication system.
* 🛒 **Cart & Checkout** – Add items to the cart, place orders, and make secure payments.
* 💳 **Payment Gateway Integration** – Secure online payments via Razorpay / PayPal / Stripe.
* 📦 **Order Tracking** – Real-time order status updates.

### **Admin Features**

* 📋 **Manage Products** – Add, update, and delete medicines.
* 🧾 **Manage Orders** – View and update order statuses.
* 👥 **Manage Users** – Control customer accounts and access.

---

## **🛠 Tech Stack**

**Frontend**

* HTML, CSS, JavaScript
* Bootstrap (Responsive UI)

**Backend**

* Python (Django Framework)
* Django ORM

**Database**

* SQLite (development) / PostgreSQL (production)

**Payment Gateway**

* Razorpay / Stripe / PayPal API

**Other Tools**

* Git & GitHub for version control

---

## **📂 Project Structure**

```
quickcure-ecommerce-website/
│── accounts/       # User authentication & profile management  
│── core/           # Main project settings & configurations  
│── inventory/      # Product and inventory management  
│── static/         # CSS, JS, and images  
│── templates/      # HTML templates  
│── manage.py       # Django management script  
│── .gitignore      # Ignored files  
```

---

## **⚙️ Installation & Setup**

1. **Clone the repository**

   ```bash
   git clone https://github.com/yourusername/quickcure-ecommerce-website.git
   cd quickcure-ecommerce-website
   ```

2. **Create a virtual environment & activate it**

   ```bash
   python -m venv venv
   source venv/bin/activate  # Mac/Linux
   venv\Scripts\activate     # Windows
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Payment Gateway**

   * Sign up for **Razorpay / Stripe / PayPal**
   * Get your API keys
   * Add them to your Django `.env` or `settings.py` file

5. **Run migrations**

   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Create a superuser**

   ```bash
   python manage.py createsuperuser
   ```

7. **Run the development server**

   ```bash
   python manage.py runserver
   ```

8. **Access the site**

   * **Frontend** → `http://127.0.0.1:8000/`
   * **Admin Panel** → `http://127.0.0.1:8000/admin/`



---

## **👨‍💻 Author**

**Nitesh Ku. Sahoo**

