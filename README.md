# Fitness and Nutrition Platform
**CSE471: System Analysis and Design (group project)**

Our Fitness & Nutrition platform is a comprehensive digital ecosystem that empowers users to reach their health goals through personalized programs, educational content, and community support. The system delivers tailored workout and meal plans with media-rich content, automated BMI and progress tracking, and integrated subscription payments, all accessible from intuitive role-based dashboards (clients, trainers, owners). Users also benefit from tutorial modules, a highly scalable discussion forum, and an AI chatbot for on-demand coaching and support.

## 🚀 Technology Stack & Architecture

- **Languages:** HTML, CSS, JS, Python
- **Framework:** Django 5.1, Bootstrap
- **Database:** PostgreSQL (Production on Supabase) / SQLite (Local Development)
- **Deployment:** Render (PaaS Hosting)
- **Static Asset Management:** WhiteNoise
- **Payments:** Stripe API (International), UDDOKTAPAY/bKash (Local)
- **Authentication:** Django Allauth (Google & GitHub OAuth)
- **AI Integration:** OpenRouter (DeepSeek/LLMs)
- **Nutrition Data:** Official USDA FoodData Central API

## 🏗️ Architectural Highlights (Deep Analysis)

- **Scalable Community Forum:** The discussion forum utilizes PostgreSQL's robust concurrency control. This completely eliminates the `database is locked` errors common in SQLite, allowing thousands of users to upvote and reply simultaneously without crashing the application.
- **Secure Premium Content Delivery:** The Diet (`Plan`) and Workout (`wPlan`) architectures use a Parent-Child relationship. More importantly, they employ `uuid.uuid4` (Universally Unique Identifiers) for their Primary Keys instead of auto-incrementing integers. This prevents URL manipulation and securely protects premium content from unauthorized access.
- **Environment-Driven Configuration:** All sensitive secrets, API keys, and database URLs have been completely decoupled from the source code and are injected dynamically via `.env` files in development and Environment Variables in production.
- **Progress Tracking:** The `BMIRecord` system accurately tracks user health data over time, ordering records chronologically to provide seamless frontend charting.

---

## 🛠️ Local Development Setup

To run the server locally, clone the repository and run the following commands in the root directory:

```bash
# Install dependencies
pip install django django-jazzmin middleware django-allauth django-mathfilters requests PyJWT cryptography pillow stripe gunicorn whitenoise dj-database-url python-dotenv psycopg2-binary

# Apply migrations
python manage.py migrate

# Run the server
python manage.py runserver
```

## 🔑 Environment Variables & API Configuration

For the platform to function correctly, you **MUST** create a `.env` file in your root folder (where `manage.py` is located) and configure the following variables.

### 1. Payment Gateways (Stripe & UDDOKTAPAY)
```env
STRIPE_PUBLISHABLE_KEY=pk_test_...
STRIPE_SECRET_KEY=sk_test_...

UDDOKTAPAY_API_KEY=your_api_key_here
UDDOKTAPAY_BASE_URL=https://your-uddoktapay-url.com
```

### 2. FitBot AI Chatbot (OpenRouter)
Our AI Chatbot features a LocalStorage memory to remember conversation context. To enable the AI brain, get a free key from [OpenRouter](https://openrouter.ai/).
```env
OPENROUTER_API_KEY=sk-or-v1-...
```

### 3. Social Authentication (Google & GitHub)
Social logins are configured directly via Environment Variables to prevent database synchronization issues during deployment.
```env
GOOGLE_CLIENT_ID=your_google_client_id
GOOGLE_CLIENT_SECRET=your_google_client_secret

GITHUB_CLIENT_ID=your_github_client_id
GITHUB_CLIENT_SECRET=your_github_client_secret
```

### 4. Nutrition Tracker (USDA API)
The nutrition tracking feature uses the official USDA API. It works with a default `DEMO_KEY`, but you can configure your own key for higher rate limits.
```env
USDA_API_KEY=your_usda_api_key_here
```

---

## 👤 Default Login Information

### Clients
- **Username:** nazia | **Password:** 1
- **Username:** shuvo | **Password:** 12345578p

### Trainers
- **Username:** apple | **Password:** apple123apple

### Owner
- **Username:** aa | **Password:** 147852mm

### Admin
- **Username:** admin | **Password:** admin

---

## 🌟 Project Features

### Module 1: Authentication & User Management
- Log in, Log out, Sign Up
- View & Edit Profile
- Reset Password
- Google & GitHub OAuth Authentication
- Secure Profile Deletion

### Module 2: Health, Content & Community
- Notification reminders
- BMI Tracking & History page
- Exercise video tutorial player
- Real-time Nutrition Tracker (Powered by the official USDA FoodData Central Database)
- Support and FAQs
- **Community Discussion Forum:** Post, view, and reply to discussions with view tracking and one-time upvoting.
- **AI-Powered FitBot Chatbot:** Features conversational memory, real-time fitness guidance, and form correction via OpenRouter AI.

### Module 3: Premium Plans & Payments
- Subscription management and renewal
- Stripe Payment Gateway (International Cards)
- bKash Payment Gateway (Local Mobile Banking)
- Secure, UUID-protected Workout Plans
- Secure, UUID-protected Nutrition Plans

---

## 💳 Payment Testing (Sandbox Mode)

### bKash Test Credentials (Simulated Sandbox)
- **Phone Number:** Any valid 11-digit number starting with 01 (e.g., `01712345678`)
- **PIN:** Any 5-digit number (e.g., `12345`)
- **OTP:** Use the 6-digit auto-generated OTP shown on screen
- *Note: No real money is charged in sandbox mode.*

### Stripe Test Credentials
- Use official Stripe test cards for simulating successful or declined payments.

---

## 🧪 Quality Assurance Test
A comprehensive Quality Assurance test was performed on this project. 
[Click here to view the QA Test Report](#) *(Link to be updated)*

---

## 👥 Contributors
[Faisal Ahmed](https://github.com/FaisalAhmed21) | [MD. Shafiur Rahman](https://github.com/ShafiurShuvo) | [Nazia Mumtahina](https://github.com/NaziaMumtahina) | [Sara Jerin Prithila](https://github.com/jerinsync)
