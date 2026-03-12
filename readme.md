# Event Management System (EMS) Project

A powerful and modern Event Management System built with Django and React.

## 🚀 Recent Feature: Google OAuth & Customer Integration

We have successfully integrated **Google OAuth 2.0** for customer authentication and a robust **Role & Permission** system specifically for customers.

### Key Changes
- **Google Authentication**: Customers can now sign in using their Google accounts via `/api/v1/auth/google/`.
- **Automatic Account Creation**: New customers are automatically registered in the system upon their first Google login.
- **Universal JWT Authentication**: A unified token system (`CustomerJWTAuthentication`) that handles both standard Admins and Customers securely.
- **Role Management**: All customers are assigned a default **'User'** role with specific permissions (viewing events, creating bookings, etc.).

---

## 🛠 Setup Instructions

### 1. Environment Configuration
Create a `.env` file in the root directory (refer to `.env.Example`) and add your database and Google credentials:
```env
DB_NAME=emsdb
DB_USER=your_user
DB_PASSWORD=your_password
DB_HOST=127.0.0.1
DB_PORT=3306

# Google OAuth Credentials
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret
```

### 2. Installation
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Database & Roles Seeding
Ensure your database is up to date and roles are seeded:
```bash
python manage.py migrate
python manage.py seed_data
```

---

## 🔑 API Reference

### Authentication
- `POST /api/v1/auth/google/`: Login with Google (requires `id_token`).
- `GET /api/v1/customers/me/`: Retrieve the authenticated customer's profile (requires Bearer Token).

---

## 🌿 Git Workflow & Branches

The project uses a standard feature-branch workflow to keep the `master` branch stable.

### Main Branches
- **`master`**: The stable production-ready branch. Direct pushes are protected.
- **`feature/google-oauth-customer`**: The current development branch for Google OAuth and Customer roles.

### How to Contribute
1.  **Sync with Master**:
    ```bash
    git checkout master
    git pull origin master
    ```
2.  **Switch to Feature Branch**:
    ```bash
    git checkout feature/google-oauth-customer
    ```
3.  **Proposing Changes**:
    - Make your changes on the feature branch.
    - Push to GitHub: `git push origin feature/google-oauth-customer`.
    - Open a **Pull Request (PR)** on GitHub to merge into `master`.

---

## 🛡 Security Note
- Hardcoded secrets have been removed from the source code.
- All secrets are now managed via environment variables in the `.env` file.
- **Never commit your `.env` file to version control.**
- If you accidentally commit a secret, use `git reset --soft origin/master` to squash your history before pushing.