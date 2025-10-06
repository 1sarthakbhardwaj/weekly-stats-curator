# 📊 Social Media Stats Dashboard

A clean, minimalistic web dashboard to view your weekly social media statistics.

## ✨ Features

- **Beautiful Web UI**: Clean, modern dashboard with gradient design
- **Multiple Reddit Accounts**: Track up to 3 Reddit accounts
- **YouTube Analytics**: Video stats with free API
- **Google Search Console**: SEO and search performance tracking
- **Flexible Time Ranges**: View stats for last 7, 14, or 30 days
- **Real-time Data**: Fetches fresh data from platform APIs

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Accounts

Copy `env_template.txt` to `.env` and add your usernames:

```bash
cp env_template.txt .env
# Edit .env with your accounts
```

### 3. Run the Dashboard

```bash
python stats.py
```

Open your browser and go to: **http://localhost:5000**

## 🔑 Setup Guide

### ✅ Reddit (No API needed - Works immediately!)

Just add your Reddit usernames to `.env`:
```bash
REDDIT_USERNAME_1=your_username_1
REDDIT_USERNAME_2=your_username_2  # Optional
REDDIT_USERNAME_3=your_username_3  # Optional
```

**That's it!** Uses public Reddit API - no authentication needed.

### 🎥 YouTube (10 minutes, FREE)

**See [SETUP_YOUTUBE.md](SETUP_YOUTUBE.md) for detailed instructions.**

Quick steps:
1. Go to [Google Cloud Console](https://console.developers.google.com/)
2. Create project & enable "YouTube Data API v3"
3. Create API key (FREE - 10,000 requests/day)
4. Get your channel ID from YouTube Studio
5. Add to `.env`:
```bash
YOUTUBE_API_KEY=your_api_key
YOUTUBE_CHANNEL_ID=@YourChannelName
```

### 🔍 Google Search Console (15 minutes, FREE)

**See [SETUP_GSC.md](SETUP_GSC.md) for detailed instructions.**

Quick steps:
1. Go to [Google Cloud Console](https://console.developers.google.com/)
2. Enable "Google Search Console API"
3. Create service account & download JSON key
4. Add service account email to Search Console users
5. Add to `.env`:
```bash
GSC_CREDENTIALS_FILE=/path/to/gsc-credentials.json
GSC_PROPERTY_URL=https://your-domain.com/
```

## 📁 Project Structure

```
.
├── stats.py                 # Main Flask app
├── collectors/              # Platform collectors (modular)
│   ├── reddit_collector.py
│   ├── youtube_collector.py
│   └── gsc_collector.py
├── templates/
│   └── dashboard.html       # Web UI
├── .env                     # Your credentials (not in git)
├── env_template.txt         # Template for .env
├── SETUP_YOUTUBE.md         # YouTube setup guide
├── SETUP_GSC.md             # Google Search Console setup guide
└── requirements.txt         # Python dependencies
```

## 💡 Usage Examples

### View All Platforms (Last 7 Days)
Just run `python stats.py` and open http://localhost:5000

### View Only Reddit
Uncheck YouTube and GSC in the web interface

### View Last 30 Days
Select "Last 30 days" from the dropdown

## 🎨 Dashboard Features

- **Platform Cards**: Each platform has its own card with key metrics
- **Multiple Reddit Accounts**: Shows combined stats + individual breakdowns
- **Top Posts**: See your best performing content
- **Subreddit Breakdown**: For Reddit, see stats by subreddit
- **Responsive Design**: Works on mobile and desktop

## 📊 Metrics Collected

| Platform | Metrics |
|----------|---------|
| Reddit | Posts, Karma, Comments, Top Post, Subreddit Breakdown |
| YouTube | Videos, Views, Likes, Comments, Avg Views per Video |
| Google Search | Clicks, Impressions, CTR, US Clicks |

## 🔒 Security

- `.env` file is in `.gitignore` - never committed to git
- API credentials stay on your local machine
- No data is sent to external servers

## 🐛 Troubleshooting

### "No data" showing for a platform?
- Check if API credentials are in `.env`
- Verify credentials are correct
- Check if you have posts/videos in the selected time range

### Reddit not working?
- Verify username is correct (case-sensitive)
- Check if profile is public
- Make sure you have posts in the time range

### YouTube showing "No videos"?
- Verify API key is correct
- Check YouTube Data API v3 is enabled
- Try both `@ChannelName` and `UC...` channel ID formats

### Google Search Console errors?
- Verify credentials file path is correct
- Check service account email is added to GSC users
- Ensure property URL matches exactly

## 🆓 Cost

**Everything is FREE!**
- Reddit API: FREE (no limits)
- YouTube API: FREE (10,000 requests/day)
- Google Search Console API: FREE (unlimited)

## 🤝 Contributing

Feel free to open issues or submit pull requests!

## 📝 License

Open source - use as you like!
