# Fitness and Nutrition Platform
**CSE471: System Analysis and Design (group project)**

## Language used:
HTML, CSS, JS, Python, SQLite

## Framework / Library:
Django, Bootstrap, Stripe API

## DBMS:
PostgreSQL (Supabase) / SQLite (Local Development)

## Used Django Features:
- Django Model
- Django Admin
- Django Static Files
- Django Templates
- Django Authentication
- Django Allauth (Social Authentication - Google & GitHub)
- Django Signals
- Django Middleware
- Django Session Management
- **Deployment:** Render (Hosting) & Supabase (PostgreSQL)

## Brief Idea About Our Project:
Our Fitness & Nutrition platform is a comprehensive digital ecosystem that empowers users to reach their health goals through personalized programs, educational content, and community support. The system delivers tailored workout and meal plans with media-rich content, automated BMI and progress tracking, and integrated subscription payments, all accessible from intuitive role-based dashboards (clients, trainers, owners). Users also benefit from tutorial modules, a discussion forum for peer and expert interaction, and an AI chatbot for on-demand coaching and support.

## To Run the Server:
In VS Code, open the folder `Fitness and Nutrition platform/hello` and then type `python manage.py runserver` in a new terminal. Run this command from project directory (hello).

## Commands That May Be Required:
```bash
pip install django
pip install django-jazzmin
pip install mysql
pip install middleware
pip install django-allauth
pip install django-mathfilters
pip install requests
pip install PyJWT
pip install cryptography
pip install pillow
pip install stripe
pip install google-generativeai
```

## Important: API Configuration

### Stripe API Configuration (Required for Payment Features)

After downloading the project, you **MUST** configure your Stripe API keys to enable payment features:

**Step 1: Get Your Stripe API Keys**
1. Create a free account at [https://stripe.com](https://stripe.com)
2. Go to Stripe Dashboard → Developers → API Keys
3. Copy your **Publishable Key** (starts with `pk_test_...`)
4. Copy your **Secret Key** (starts with `sk_test_...`)

**Step 2: Update the Configuration File**
1. Open the file: `hello/settings.py`
2. Find these lines (around line 160-165):
   ```python
   STRIPE_PUBLIC_KEY = 'your_stripe_publishable_key_here'
   STRIPE_SECRET_KEY = 'your_stripe_secret_key_here'
   ```
3. Replace `'your_stripe_publishable_key_here'` with your actual Publishable Key
4. Replace `'your_stripe_secret_key_here'` with your actual Secret Key

**Note:** Without configuring Stripe API keys, the Stripe payment option will not work. bKash sandbox mode will work without any configuration.

### OpenRouter API Configuration (Required for AI Chatbot)

To enable the FitBot AI chatbot feature, you need a free OpenRouter API key:

**Step 1: Get Your OpenRouter API Key**
1. Visit [https://openrouter.ai/](https://openrouter.ai/)
2. Sign in with your Google account
3. Click on "Keys" and generate a new API key

**Step 2: Update the Configuration File**
Create a `.env` file in your root folder and add:
```
OPENROUTER_API_KEY=your_openrouter_api_key_here
```

### Social Authentication Configuration (Google & GitHub)
Social logins are configured directly via Environment Variables to prevent database synchronization issues during deployment.

Create a `.env` file in your root folder and add your OAuth keys:
```
GOOGLE_CLIENT_ID=your_google_client_id
GOOGLE_CLIENT_SECRET=your_google_client_secret

GITHUB_CLIENT_ID=your_github_client_id
GITHUB_CLIENT_SECRET=your_github_client_secret
```

### USDA FoodData Central API (Required for Nutrition Tracker)
The nutrition tracking feature uses the official USDA API. It works with a default DEMO_KEY, but you can configure your own key for higher rate limits.
Add this to your `.env` file:
```
USDA_API_KEY=your_usda_api_key_here
```

## Login Info:

### Clients' usernames are:
**Username:** nazia  
**Password:** 1

**Username:** shuvo  
**Password:** 12345578p

### Trainer username:
**Username:** apple  
**Password:** apple123apple

### Owner username:
**Username:** aa  
**Password:** 147852mm

### Admin:
**Username:** admin  
**Password:** admin

## Project Features:

### Module 1:
- Log in, Log out
- Sign Up / Registration
- View Profile
- Edit Profile
- Reset Password
- Gmail Authentication
- GitHub Authentication
- Delete Profile using the actual password

### Module 2:
### Module 2:
- Notification reminder
- BMI page
- Exercise video tutorial play
- Nutrition values (Powered by official USDA FoodData Central Database)
- Support and FAQs
- Community Discussion Forum
  - Post, view, and reply to discussions
  - One-time upvote and unique view tracking per user
- **AI-Powered FitBot Chatbot**
  - Real-time fitness and nutrition guidance
  - Powered by OpenRouter AI

### Module 3:
- Subscription management and renewal
- Stripe Payment Gateway (International Cards)
- bKash Payment Gateway (Local Mobile Banking - Sandbox Mode)
- Workout plan
- Nutrition plan

## Payment Testing (Sandbox Mode):

### bKash Test Credentials:
- **Phone Number:** Any valid 11-digit number starting with 01 (e.g., 01712345678)
- **PIN:** Any 5-digit number (e.g., 12345)
- **OTP:** Use the 6-digit auto-generated OTP shown on screen
- **Note:** No real money is charged in sandbox mode

### Stripe:
- Use Stripe test cards for testing payments

### Contributors
[Faisal Ahmed](https://github.com/FaisalAhmed21) | [MD. Shafiur Rahman](https://github.com/ShafiurShuvo) | [Nazia Mumtahina](https://github.com/NaziaMumtahina) | [Sara Jerin Prithila](https://github.com/jerinsync)
