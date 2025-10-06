# 📊 Social Media Stats Dashboard

A clean, minimalistic web dashboard to view your weekly social media statistics across multiple platforms.

## ✨ Features

- **Beautiful Web UI**: Clean, modern dashboard with gradient design
- **Multi-Platform Support**: Reddit, LinkedIn, Twitter/X, YouTube, Google Search Console
- **Flexible Time Ranges**: View stats for last 7, 14, or 30 days
- **Platform Selection**: Choose which platforms to display
- **Real-time Data**: Fetches fresh data from platform APIs

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure API Credentials

Copy `env_template.txt` to `.env` and add your credentials:

```bash
cp env_template.txt .env
# Edit .env with your API credentials
```

### 3. Run the Dashboard

```bash
python stats.py
```

Open your browser and go to: **http://localhost:5000**

## 🔑 API Setup

### Reddit (Easiest - No approval needed!)

1. Go to https://www.reddit.com/prefs/apps
2. Click "Create App" → Select "script"
3. Fill in any name and `http://localhost:8080` as redirect URI
4. Copy Client ID and Client Secret to `.env`
5. Add your Reddit username

**That's it! Reddit works immediately.**

### LinkedIn (Requires approval)

1. Go to https://www.linkedin.com/developers/apps
2. Create app and associate with your Company Page
3. Request "Community Management API" access in Products tab
4. Wait for approval (1-3 days)
5. Generate access token with `r_organization_admin` permission
6. Find your organization ID and add to `.env`

### Twitter/X (Requires approval)

1. Go to https://developer.twitter.com/en/portal/dashboard
2. Create project and app
3. Generate bearer token
4. Add to `.env` with your Twitter username

### YouTube (Requires API key)

1. Go to https://console.developers.google.com/
2. Enable YouTube Data API v3
3. Create API key
4. Add API key and channel ID to `.env`

### Google Search Console (Requires service account)

1. Go to https://console.developers.google.com/
2. Enable Search Console API
3. Create service account and download JSON credentials
4. Add file path and property URL to `.env`

## 📁 Project Structure

```
.
├── stats.py                 # Main Flask app
├── collectors/              # Platform collectors (modular)
│   ├── reddit_collector.py
│   ├── linkedin_collector.py
│   ├── twitter_collector.py
│   ├── youtube_collector.py
│   └── gsc_collector.py
├── templates/
│   └── dashboard.html       # Web UI
├── .env                     # Your credentials (not in git)
├── env_template.txt         # Template for .env
└── requirements.txt         # Python dependencies
```

## 💡 Usage Examples

### View All Platforms (Last 7 Days)
Just run `python stats.py` and open http://localhost:5000

### View Only Reddit and LinkedIn
Check/uncheck platforms in the web interface

### View Last 30 Days
Select "Last 30 days" from the dropdown

## 🎨 Dashboard Features

- **Platform Cards**: Each platform has its own card with key metrics
- **Top Posts**: See your best performing content
- **Subreddit Breakdown**: For Reddit, see stats by subreddit
- **Engagement Rates**: Calculate engagement percentages
- **Responsive Design**: Works on mobile and desktop

## 🔒 Security

- `.env` file is in `.gitignore` - never committed to git
- API credentials stay on your local machine
- No data is sent to external servers

## 🐛 Troubleshooting

### "No data" showing for a platform?
- Check if API credentials are in `.env`
- Verify credentials are correct
- Check if you have posts in the selected time range

### Reddit rate limiting?
- Wait a few minutes between requests
- Reddit public API has rate limits

### LinkedIn showing 0 posts?
- Make sure you have Community Management API access
- Verify you're an ADMINISTRATOR on the company page
- Check organization ID is correct

## 📊 Metrics Collected

| Platform | Metrics |
|----------|---------|
| Reddit | Posts, Karma, Comments, Top Post, Subreddit Breakdown |
| LinkedIn | Posts, Likes, Comments, Shares, Impressions, Engagement Rate |
| Twitter/X | Tweets, Likes, Retweets, Replies, Impressions, Engagement Rate |
| YouTube | Videos, Views, Likes, Comments, Avg Views per Video |
| Google Search | Clicks, Impressions, CTR, US Clicks |

## 🤝 Contributing

Feel free to open issues or submit pull requests!

## 📝 License

Open source - use as you like!
