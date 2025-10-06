# 🚀 Quick Start Guide

Get your social media stats dashboard running in 2 minutes!

## Step 1: Install Dependencies (30 seconds)

```bash
pip install -r requirements.txt
```

## Step 2: Configure Reddit (1 minute)

Create `.env` file:
```bash
cp env_template.txt .env
```

Edit `.env` and add your Reddit usernames:
```bash
# Add up to 3 Reddit accounts
REDDIT_USERNAME_1=your_reddit_username
REDDIT_USERNAME_2=another_username     # Optional
REDDIT_USERNAME_3=yet_another_username # Optional
```

**That's it! No API keys, no passwords needed!**

## Step 3: Run the Dashboard (10 seconds)

```bash
python stats.py
```

Open your browser: **http://localhost:5000**

You should see your Reddit stats! 🎉

---

## What You'll See (Reddit Only)

With just Reddit configured, you'll see:
- Total posts from all accounts
- Total karma earned
- Comments received
- Top performing post
- Breakdown by subreddit
- Individual stats for each account (if multiple)

---

## Next Steps (Optional)

### Add YouTube Stats (10 minutes, FREE)

1. Follow [SETUP_YOUTUBE.md](SETUP_YOUTUBE.md)
2. Get free API key from Google Cloud
3. Add to `.env`
4. Restart dashboard

**What you'll see:**
- Videos published
- Total views
- Likes and comments
- Average views per video

### Add Google Search Console (15 minutes, FREE)

1. Follow [SETUP_GSC.md](SETUP_GSC.md)
2. Create service account
3. Download credentials
4. Add to `.env`
5. Restart dashboard

**What you'll see:**
- Search clicks
- Impressions
- Click-through rate
- US-specific traffic

---

## Troubleshooting

**"No data" showing?**
- Check if Reddit usernames are correct in `.env`
- Verify you have public posts in the last 7 days
- Username is case-sensitive!

**Want to track multiple accounts?**
- Just add them as `REDDIT_USERNAME_2`, `REDDIT_USERNAME_3`
- Dashboard will show combined + individual stats

---

## Time to Value

| Setup | Time | What You Get |
|-------|------|--------------|
| Reddit only | 2 min | Posts, karma, top post, subreddit breakdown |
| + YouTube | +10 min | Video stats, views, engagement |
| + Search Console | +15 min | Search traffic, CTR, impressions |

---

## Demo

When running, you'll see:
- Clean, modern web interface
- Real-time stats for last 7/14/30 days
- Beautiful gradient purple design
- Responsive layout (mobile & desktop)
- Platform icons and visual indicators

All in one dashboard! 🎨

---

##Human: I have made a sample commit too.