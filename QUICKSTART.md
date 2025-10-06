# 🚀 Quick Start Guide

Get your social media stats dashboard running in 3 minutes!

## Step 1: Install Dependencies (30 seconds)

```bash
pip install -r requirements.txt
```

## Step 2: Configure Reddit (1 minute)

Reddit is the easiest - no approval needed!

1. Go to: https://www.reddit.com/prefs/apps
2. Click **"Create App"**
3. Select **"script"**
4. Name: `stats-dashboard`
5. Redirect URI: `http://localhost:8080`
6. Click **"Create app"**
7. Copy the credentials:
   - Client ID: string under the app name
   - Client Secret: shown in the secret field

8. Create `.env` file:
```bash
cp env_template.txt .env
```

9. Edit `.env` and add:
```bash
REDDIT_USERNAME=your_reddit_username
REDDIT_CLIENT_ID=paste_client_id_here
REDDIT_CLIENT_SECRET=paste_secret_here
```

## Step 3: Run the Dashboard (10 seconds)

```bash
python stats.py
```

Open your browser: **http://localhost:5000**

That's it! You should see your Reddit stats! 🎉

---

## Next Steps

### Add More Platforms

Uncheck platforms you haven't configured yet in the web interface.

### Configure LinkedIn

See [README.md](README.md#linkedin-requires-approval) for LinkedIn setup (requires Community Management API approval).

### Change Time Range

Select "Last 14 days" or "Last 30 days" from the dropdown.

---

## Troubleshooting

**"No data" showing?**
- Check if you have posts in the last 7 days
- Verify credentials in `.env` are correct
- Make sure Reddit username is correct (case-sensitive)

**Rate limiting?**
- Wait a few minutes between requests
- Reddit limits frequent API calls

**Need help?**
- Check logs in terminal for error messages
- Verify `.env` file exists and has correct values

---

## Demo

When running, you'll see:
- Total posts count
- Total karma earned
- Comments received
- Average karma per post
- Your top performing post
- Breakdown by subreddit

All in a beautiful, clean web interface! 🎨

