# 🚀 Deployment Guide - Social Media Stats Dashboard

This guide will help you deploy your dashboard to **Render** (free hosting) so you can share it with a public URL without exposing your credentials.

## 📋 Prerequisites

- GitHub account with your repository pushed
- Render account (free) - Sign up at [render.com](https://render.com)

## 🎯 Quick Deploy to Render

### Step 1: Sign Up/Login to Render
1. Go to [render.com](https://render.com)
2. Sign up or login with your GitHub account

### Step 2: Create a New Web Service
1. Click **"New +"** button in the top right
2. Select **"Web Service"**
3. Connect your GitHub repository: `1sarthakbhardwaj/weekly-stats-curator`
4. Click **"Connect"**

### Step 3: Configure Your Service

**Basic Settings:**
- **Name**: `social-media-stats-dashboard` (or any name you prefer)
- **Region**: Choose closest to you
- **Branch**: `main`
- **Runtime**: `Python 3`
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `gunicorn stats:app`

**Instance Type:**
- Select **"Free"** (perfect for this use case)

### Step 4: Add Environment Variables

Click **"Advanced"** and add these environment variables (without exposing them in code):

#### Reddit Accounts
```
REDDIT_USERNAME_1 = Full_Piano_3448
REDDIT_DISPLAY_NAME_1 = Sarthak

REDDIT_USERNAME_2 = Street-Lie-2584
REDDIT_DISPLAY_NAME_2 = Sohan Lal

REDDIT_USERNAME_3 = Ok-Ant8646
REDDIT_DISPLAY_NAME_3 = Yash Suman
```

#### YouTube
```
YOUTUBE_API_KEY = AIzaSyCGh6vJKBKkFosvhTrFbrb-ZNHl3WyNl34
YOUTUBE_CHANNEL_ID = UCjhU25KnROlMdC2oXUL3rGg
```

#### Google Search Console
```
GSC_CREDENTIALS_FILE = 
GSC_PROPERTY_URL = https://labellerr.com/
```

#### GitHub
```
GITHUB_USERNAME = Labellerr
GITHUB_TOKEN = (optional - leave empty or add token)
```

#### Flask Secret Key
```
FLASK_SECRET_KEY = (Render will auto-generate this)
```

### Step 5: Deploy!
1. Click **"Create Web Service"**
2. Wait 2-3 minutes for the build to complete
3. Your dashboard will be live at: `https://your-app-name.onrender.com`

## 🔗 Your Shareable Link

Once deployed, you'll get a URL like:
```
https://social-media-stats-dashboard.onrender.com
```

This link is:
- ✅ **Public** - Anyone can view it
- ✅ **Secure** - Credentials are stored as environment variables
- ✅ **Free** - No cost for basic usage
- ✅ **Auto-updates** - Redeploys when you push to GitHub

## 🎨 Alternative Deployment Options

### Option 2: Vercel (Serverless)
1. Install Vercel CLI: `npm i -g vercel`
2. Run: `vercel`
3. Follow the prompts

### Option 3: Railway (Easy Setup)
1. Go to [railway.app](https://railway.app)
2. Click "Deploy from GitHub"
3. Select your repository
4. Add environment variables
5. Deploy!

### Option 4: Heroku (Classic)
1. Create `Procfile`: `web: gunicorn stats:app`
2. Install Heroku CLI
3. Run:
   ```bash
   heroku create your-app-name
   heroku config:set REDDIT_USERNAME_1=Full_Piano_3448
   # ... add all env vars
   git push heroku main
   ```

## 🔒 Security Notes

- ✅ Never commit `.env` file to GitHub (already in `.gitignore`)
- ✅ Use environment variables on hosting platform
- ✅ Keep API keys and tokens secure
- ✅ Rotate tokens periodically

## 📊 Monitoring

- **Render Dashboard**: View logs, metrics, and deployments
- **Auto-deploys**: Automatically redeploys when you push to GitHub
- **Free tier**: 750 hours/month (enough for 24/7 operation)

## 🆘 Troubleshooting

### Build Fails
- Check `requirements.txt` has all dependencies
- Verify Python version compatibility

### App Crashes
- Check logs in Render dashboard
- Verify all environment variables are set

### Slow Loading
- Free tier sleeps after 15 minutes of inactivity
- First request after sleep takes ~30 seconds
- Upgrade to paid tier for always-on service

## 🎉 You're Done!

Share your dashboard link with anyone - they can view your stats without accessing your credentials!

Example: `https://social-media-stats-dashboard.onrender.com`
