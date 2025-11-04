# Fitness and Nutrition Platform
**CSE471: System Analysis and Design (group project)**

## Language used:
HTML, CSS, JS, Python, SQLite

## Framework / Library:
Django, Bootstrap, Stripe API

## DBMS:
SQLite

## Used Django Features:
- Django Model
- Django Admin
- Django Static Files
- Django Templates
- Django Authentication
- Django Allauth (Social Authentication)
- Django Signals
- Django Middleware
- Django Session Management

## Brief Idea About Our Project:
Our platform is designed to empower individuals to achieve their health and wellness goals. It offers tailored fitness programs, nutritional plans, and valuable wellness resources. Users can explore the nutritional values of various food items and access workout tutorials to enhance their understanding of nutrition-enriched food and effective workouts. An interactive BMI tracker allows users to monitor their progress and compare current states with previous records. 

The platform features a premium subscription system with multiple payment options including Stripe (international cards) and bKash (local mobile banking). With seamless access via Google and GitHub sign-ins, users can easily manage their personalized dashboards. Regular notifications and reminders ensure that users stay committed to their fitness and nutrition journey.

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
```

## Important: Stripe API Configuration (Required for Payment Features)

After downloading the project, you **MUST** configure your Stripe API keys to enable payment features:

### Step 1: Get Your Stripe API Keys
1. Create a free account at [https://stripe.com](https://stripe.com)
2. Go to Stripe Dashboard → Developers → API Keys
3. Copy your **Publishable Key** (starts with `pk_test_...`)
4. Copy your **Secret Key** (starts with `sk_test_...`)

### Step 2: Update the Configuration File
1. Open the file: `hello/settings.py`
2. Find these lines (around line 160-165):
   ```python
   STRIPE_PUBLIC_KEY = 'your_stripe_publishable_key_here'
   STRIPE_SECRET_KEY = 'your_stripe_secret_key_here'
   ```
3. Replace `'your_stripe_publishable_key_here'` with your actual Publishable Key
4. Replace `'your_stripe_secret_key_here'` with your actual Secret Key


**Note:** Without configuring Stripe API keys, the Stripe payment option will not work. bKash sandbox mode will work without any configuration.

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
- Notification reminder
- BMI page
- Exercise video tutorial play
- Nutrition values
- Support and FAQs

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
- **OTP:** Any 6-digit number or use the auto-generated OTP shown on screen
- **Note:** No real money is charged in sandbox mode

### Stripe:
- Use Stripe test cards for testing payments

### Contributors
[Faisal Ahmed](https://github.com/FaisalAhmed21) | [MD. Shafiur Rahman](https://github.com/ShafiurShuvo) | [Nazia Mumtahina](https://github.com/NaziaMumtahina) | [Sara Jerin Prithila](https://github.com/jerinsync)
