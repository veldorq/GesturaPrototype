# 🚀 Gestura - Deploy to Render

## Quick Deploy (5 Minutes)

### 1️⃣ Create Render Account
Go to: **https://render.com/register**
- Sign up with GitHub (recommended)
- No credit card required for free tier

### 2️⃣ Create New Web Service
1. Click **"New +"** button (top right)
2. Select **"Web Service"**
3. Click **"Connect Account"** to link GitHub
4. Find and select: **`veldorq/GesturaPrototype`**

### 3️⃣ Configure Deployment

**Fill in these settings:**

```
Name:                gestura
Region:              Oregon (US West) - or closest to you
Branch:              Souvik
Root Directory:      (leave blank)
Environment:         Python 3
Build Command:       pip install -r requirements-web.txt
Start Command:       gunicorn --worker-class eventlet -w 1 --bind 0.0.0.0:$PORT app_web:app
```

**Plan Selection:**
- Choose: **Free** (0$/month)
- ✅ 750 hours/month
- ✅ Automatic SSL
- ✅ Global CDN

### 4️⃣ Deploy!
1. Click **"Create Web Service"**
2. Wait 3-5 minutes for build
3. Your site will be live at: `https://gestura-xxxxx.onrender.com`

---

## 📋 Post-Deployment

### Your Live URLs:
- **Product Page**: `https://your-app.onrender.com/product`
- **Dashboard Demo**: `https://your-app.onrender.com/dashboard`
- **Homepage**: `https://your-app.onrender.com/` (redirects to product)

### ⚠️ Important Notes:
- **Cold Starts**: Free tier sleeps after 15 min of inactivity (15s wake-up time)
- **Camera Access**: Dashboard is demo-only online (full features require local install)
- **Always On**: Upgrade to $7/month plan to eliminate cold starts

---

## 🔄 Update Your Site

After making changes:
```bash
cd "c:\Users\Souvik\Desktop\Souvik project\SOuvikmeet"
git add .
git commit -m "Update website"
git push origin Souvik
```

Render auto-deploys from GitHub - changes go live in ~2 minutes!

---

## 🎨 Custom Domain (Optional)

1. Go to your Render dashboard
2. Click your service → "Settings"
3. Scroll to "Custom Domain"
4. Add your domain (e.g., `gestura.com`)
5. Update DNS records as shown

Free SSL certificate included!

---

## 📊 Monitor Your Site

**Render Dashboard**: https://dashboard.render.com
- View logs
- Check uptime
- Monitor traffic
- Restart service

---

Need help? Check deployment status on Render dashboard or ask me!
