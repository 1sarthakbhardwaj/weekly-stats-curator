# Changelog

## Latest Update - Individual Account Cards & LinkedIn Manual Input

### ✨ New Features

1. **Individual Reddit Account Cards**
   - Each Reddit account now gets its own dedicated card
   - Support for up to 3 accounts with custom display names
   - Currently tracking:
     - **Sarthak** (u/Full_Piano_3448)
     - **Sohan Lal** (u/Street-Lie-2584)

2. **LinkedIn Manual Input**
   - New manual stats entry form for LinkedIn
   - Toggle button to show/hide the form
   - Fields: Posts, Likes, Comments, Shares, Impressions, Engagement Rate
   - Stats persist during the session
   - Beautiful LinkedIn-branded buttons

3. **Display Names**
   - Add custom display names for Reddit accounts in `.env`
   - Shows "Reddit - Display Name" on each card
   - Falls back to username if no display name provided

### 🗑️ Removed

- Twitter/X support (expensive API, unreliable scraping)
- LinkedIn API support (moved to manual entry)
- Unnecessary scraping dependencies (snscrape, playwright, selenium)

### 🎨 UI Improvements

- Separate cards for each Reddit account
- LinkedIn manual input form with gradient buttons
- Clean form styling with focus states
- Mobile-responsive design maintained

### 📁 Configuration

Update your `.env` file:
```bash
# Reddit accounts with display names
REDDIT_USERNAME_1=Full_Piano_3448
REDDIT_DISPLAY_NAME_1=Sarthak

REDDIT_USERNAME_2=Street-Lie-2584
REDDIT_DISPLAY_NAME_2=Sohan Lal

REDDIT_USERNAME_3=
REDDIT_DISPLAY_NAME_3=
```

### 🚀 How to Use

1. **Reddit**: Automatically fetches stats for all configured accounts
2. **LinkedIn**: 
   - Click "✏️ Enter LinkedIn Stats" button
   - Fill in your metrics manually
   - Click "💾 Save Stats"
   - Refresh to see updated dashboard
3. **YouTube**: Configure API key (optional, FREE)
4. **GSC**: Configure service account (optional, FREE)

### 📊 Dashboard Features

Each Reddit card shows:
- Total posts, karma, comments
- Average karma per post
- Top performing post
- Breakdown by subreddit
- Account's display name

LinkedIn card shows:
- Manual entry form
- All standard LinkedIn metrics
- "(Manual)" badge to indicate data source

### 🔧 Technical Changes

- Refactored `stats.py` to handle multiple accounts
- Updated `dashboard.html` with account iteration
- Added JavaScript for LinkedIn form handling
- New API endpoint `/api/linkedin` for saving stats
- Simplified requirements.txt

### 📝 Files Changed

- `stats.py`: Multi-account support + LinkedIn API
- `templates/dashboard.html`: Individual cards + form
- `env_template.txt`: Display name fields
- `collectors/__init__.py`: Removed Twitter/LinkedIn
- `requirements.txt`: Removed scraping libraries
- `README.md`: Updated documentation
- `QUICKSTART.md`: Simplified setup

### 🎯 Next Steps

If you want to add more Reddit accounts (beyond 3), just:
1. Update `.env` with `REDDIT_USERNAME_4`, etc.
2. Update `stats.py` loop range from `range(1, 4)` to `range(1, N+1)`
3. Each will get its own card automatically!

---

## Previous Updates

See git commit history for earlier changes.

