# 🎥 YouTube API Setup Guide (FREE - 10 minutes)

YouTube API is **completely free** for most use cases. You get **10,000 requests per day** on the free tier - more than enough for weekly stats!

## Step 1: Create Google Cloud Project (3 minutes)

1. Go to [Google Cloud Console](https://console.developers.google.com/)
2. Sign in with your Google account
3. Click **"Select a project"** dropdown at the top
4. Click **"NEW PROJECT"**
5. Enter project name: `social-media-stats` (or any name)
6. Click **"CREATE"**
7. Wait for the project to be created (~10 seconds)

## Step 2: Enable YouTube Data API (2 minutes)

1. In the left sidebar, click **"APIs & Services"** > **"Library"**
2. Search for: `YouTube Data API v3`
3. Click on **"YouTube Data API v3"**
4. Click the blue **"ENABLE"** button
5. Wait for it to enable (~5 seconds)

## Step 3: Create API Key (2 minutes)

1. Click **"APIs & Services"** > **"Credentials"** in the left sidebar
2. Click **"+ CREATE CREDENTIALS"** at the top
3. Select **"API key"**
4. A popup will show your new API key
5. **COPY THE API KEY** (it looks like: `AIzaSyDxxxxxxxxxxxxxxxxxxxxxx`)
6. Click **"CLOSE"**

### Optional: Restrict API Key (Recommended for security)

1. Click the pencil icon next to your API key
2. Under "API restrictions":
   - Select **"Restrict key"**
   - Check only **"YouTube Data API v3"**
3. Click **"SAVE"**

## Step 4: Get Your Channel ID (3 minutes)

### Method 1: From YouTube Studio (Easiest)
1. Go to [YouTube Studio](https://studio.youtube.com/)
2. Click **"Settings"** (gear icon) in the left sidebar
3. Click **"Channel"** > **"Advanced settings"**
4. Your **Channel ID** is shown there (starts with `UC...`)
5. **COPY THE CHANNEL ID**

### Method 2: From Channel URL
1. Go to your YouTube channel
2. Look at the URL:
   - If it's `youtube.com/@YourChannelName` → use `@YourChannelName`
   - If it's `youtube.com/channel/UC...` → use the `UC...` part

## Step 5: Add to .env File (1 minute)

Open your `.env` file and add:

```bash
# YouTube API Configuration
YOUTUBE_API_KEY=AIzaSyDxxxxxxxxxxxxxxxxxxxxxx
YOUTUBE_CHANNEL_ID=@Labellerr
# Or use Channel ID: UC...xxxxx...xxxxx
```

**For your Labellerr channel:**
```bash
YOUTUBE_API_KEY=paste_your_api_key_here
YOUTUBE_CHANNEL_ID=@Labellerr
```

## Step 6: Test It! (30 seconds)

```bash
# Stop the server (Ctrl+C if running)
python stats.py
```

Open http://localhost:5050 and you should see YouTube stats!

---

## What Stats You'll Get

With YouTube API, you'll see:
- ✅ Number of videos published in the time range
- ✅ Total views across all videos
- ✅ Total likes
- ✅ Total comments
- ✅ Average views per video

---

## Free Tier Limits

- **10,000 requests per day** (FREE)
- Each stats collection uses ~1-5 requests
- You can check stats **thousands of times per day** for free!

---

## Troubleshooting

### "API key not valid"
- Make sure you copied the entire key
- Check there are no extra spaces
- Verify YouTube Data API v3 is enabled

### "Channel not found"
- Try both formats: `@Labellerr` and your Channel ID `UC...`
- Make sure the channel is public
- Check spelling

### "Quota exceeded"
- Very unlikely! You'd need to check stats 2000+ times in one day
- Resets at midnight Pacific Time
- Upgrade to paid if needed (very cheap)

---

## Cost

**FREE** for normal usage!
- First 10,000 requests/day: **$0**
- After that: $0.001 per request (1/10th of a cent)
- Weekly stats check: Uses ~5 requests = **$0**

---

## Done! ✅

Once configured, your YouTube stats will automatically appear in the dashboard every time you refresh!

