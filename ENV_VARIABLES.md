# 🔐 Environment Variables Guide for Render

## Setting Up Environment Variables on Render

After creating your web service on Render, configure these environment variables:

### How to Add Environment Variables:

1. Go to your Render Dashboard: https://dashboard.render.com
2. Click on your **gestura** service
3. Click **"Environment"** in the left sidebar
4. Click **"Add Environment Variable"**
5. Add each variable below

---

## Required Environment Variables

### 1. SECRET_KEY (Required)
- **Key**: `SECRET_KEY`
- **Value**: Generate a secure random string (see below)
- **Purpose**: Flask session security

**Generate a secure key:**
```python
python -c "import secrets; print(secrets.token_hex(32))"
```

### 2. PYTHON_VERSION (Optional)
- **Key**: `PYTHON_VERSION`
- **Value**: `3.10.0`
- **Purpose**: Specify Python version

---

## Optional Environment Variables

### 3. FLASK_ENV
- **Key**: `FLASK_ENV`
- **Value**: `production`
- **Purpose**: Set Flask environment mode

### 4. DEBUG
- **Key**: `DEBUG`
- **Value**: `False`
- **Purpose**: Disable debug mode in production

### 5. DEPLOYMENT_MODE
- **Key**: `DEPLOYMENT_MODE`
- **Value**: `demo`
- **Purpose**: Indicate this is demo deployment

### 6. GITHUB_REPO
- **Key**: `GITHUB_REPO`
- **Value**: `https://github.com/veldorq/GesturaPrototype`
- **Purpose**: Link to repository

### 7. ALLOWED_ORIGINS
- **Key**: `ALLOWED_ORIGINS`
- **Value**: `*` (for testing) or `https://yourdomain.com` (for production)
- **Purpose**: CORS configuration

---

## 📋 Quick Setup Checklist

### Minimum Required (Start Here):
```
✅ SECRET_KEY = <your-generated-key>
```

### Recommended for Production:
```
✅ SECRET_KEY = <your-generated-key>
✅ PYTHON_VERSION = 3.10.0
✅ FLASK_ENV = production
✅ DEBUG = False
```

### Optional (Nice to Have):
```
⭕ DEPLOYMENT_MODE = demo
⭕ GITHUB_REPO = https://github.com/veldorq/GesturaPrototype
⭕ ALLOWED_ORIGINS = *
```

---

## 🔧 How Environment Variables Work in Code

Your `app_web.py` reads these variables:

```python
# Example from app_web.py
SECRET_KEY = os.environ.get('SECRET_KEY', 'default-fallback')
DEBUG = os.environ.get('DEBUG', 'False').lower() == 'true'
```

If a variable isn't set, it uses the fallback value.

---

## 🚨 Security Best Practices

### ✅ DO:
- Generate unique SECRET_KEY for production
- Use environment variables for all secrets
- Set DEBUG=False in production
- Restrict ALLOWED_ORIGINS in production

### ❌ DON'T:
- Commit `.env` files to Git
- Share SECRET_KEY publicly
- Use default/example keys in production
- Enable DEBUG in production

---

## 🧪 Testing Locally with Environment Variables

### Option 1: Command Line (Windows)
```powershell
$env:SECRET_KEY="your-secret-key"
$env:DEBUG="True"
python app_web.py
```

### Option 2: .env File (with python-dotenv)
1. Install: `pip install python-dotenv`
2. Copy `.env.example` to `.env`
3. Edit `.env` with your values
4. Add to app_web.py:
```python
from dotenv import load_dotenv
load_dotenv()
```

---

## 📊 Verifying Environment Variables

After deployment, check: `https://your-app.onrender.com/api/status`

You should see your configured values in the response.

---

## 🔄 Updating Environment Variables

1. Go to Render Dashboard
2. Select your service
3. Click "Environment"
4. Edit/add variables
5. Click "Save Changes"
6. Service will automatically restart

---

## 🆘 Troubleshooting

### Problem: Site won't load
- **Check**: SECRET_KEY is set
- **Check**: PYTHON_VERSION matches (3.10.0)

### Problem: CORS errors
- **Check**: ALLOWED_ORIGINS includes your domain
- **Try**: Set to `*` temporarily for testing

### Problem: Variables not working
- **Check**: Variable names match exactly (case-sensitive)
- **Check**: Service restarted after adding variables
- **Try**: View logs in Render dashboard

---

Need help? Check Render docs: https://render.com/docs/environment-variables
