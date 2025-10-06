# Weekly Stats Curator

A Python script to automatically collect and curate weekly statistics from various social media platforms and Google Search Console.

## Features

- **Multi-platform support**: Reddit, LinkedIn, X (Twitter), YouTube, Google Search Console
- **Automated data collection**: Fetches posts, engagement metrics, and performance data
- **CSV export**: Generates formatted reports for easy analysis
- **Environment-based configuration**: Secure API key management
- **Customizable date ranges**: Defaults to week starting September 22nd, 2024

## Metrics Collected

| Platform | Posts | Karma | Impressions | CTR | Likes | Clicks (US) |
|----------|-------|-------|-------------|-----|-------|-------------|
| Reddit   | ✅    | ✅    | ❌          | ❌  | ❌    | ❌          |
| LinkedIn | ✅    | ❌    | ✅          | ❌  | ✅    | ❌          |
| X (Twitter) | ✅ | ❌    | ✅          | ❌  | ✅    | ❌          |
| YouTube  | ✅    | ❌    | ✅          | ❌  | ✅    | ❌          |
| Google Search Console | ❌ | ❌ | ✅ | ✅ | ❌ | ✅ |

## Installation

1. **Clone or download the script**
   ```bash
   # If you have git
   git clone <repository-url>
   cd weekly-stats-curator
   
   # Or simply download the files
   ```

2. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   ```bash
   # Copy the template
   cp env_template.txt .env
   
   # Edit .env with your actual API credentials
   nano .env
   ```

## API Setup Instructions

### Reddit API
1. Go to [Reddit App Preferences](https://www.reddit.com/prefs/apps)
2. Click "Create App" or "Create Another App"
3. Choose "script" as the app type
4. Note down the client ID and secret
5. Add your Reddit username and password to the .env file

### LinkedIn API
1. Go to [LinkedIn Developers](https://www.linkedin.com/developers/apps)
2. Create a new app
3. Request access to "Share on LinkedIn" and "Read organization content"
4. Generate an access token
5. Find your organization ID in LinkedIn Analytics

### X (Twitter) API
1. Go to [Twitter Developer Portal](https://developer.twitter.com/en/portal/dashboard)
2. Create a new project/app
3. Generate API keys and access tokens
4. Ensure you have read permissions for your account

### YouTube API
1. Go to [Google Cloud Console](https://console.developers.google.com/)
2. Enable the YouTube Data API v3
3. Create credentials (API key)
4. Find your channel ID in YouTube Studio settings

### Google Search Console
1. Go to [Google Cloud Console](https://console.developers.google.com/)
2. Enable the Search Console API
3. Create a service account
4. Download the JSON credentials file
5. Add the property URL to Google Search Console

## Usage

### Basic Usage
```bash
python weekly_stats_curator.py
```

### Custom Date Range
You can modify the script to use different date ranges by editing the `start_date` variable in the `WeeklyStatsCurator` class:

```python
# In weekly_stats_curator.py
self.start_date = datetime(2024, 9, 22)  # Change this date
self.end_date = self.start_date + timedelta(days=7)
```

### Output
The script will:
1. Print a summary to the console
2. Generate a CSV file with detailed metrics
3. Log any errors or warnings

## Output Format

The script generates a CSV file with the following columns:
- **Channel**: Platform name
- **Posts Count**: Number of posts published in the week
- **Karma**: Total karma/score (Reddit only)
- **Impressions**: Total impressions/views
- **CTR**: Click-through rate percentage
- **Likes**: Total likes/upvotes
- **Clicks (US)**: US-specific clicks (GSC only)

## Troubleshooting

### Common Issues

1. **API Rate Limits**
   - Some APIs have rate limits. The script includes basic error handling
   - Consider adding delays between API calls if you hit limits

2. **Authentication Errors**
   - Verify your API credentials in the .env file
   - Check that tokens haven't expired
   - Ensure proper permissions are granted

3. **Missing Data**
   - Some platforms may not return all requested metrics
   - Check API documentation for available fields
   - Verify your account has access to the required data

4. **Date Range Issues**
   - Ensure your date range is valid
   - Some APIs may have restrictions on historical data
   - Check timezone settings

### Debug Mode
Enable debug logging by modifying the logging level:
```python
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
```

## Customization

### Adding New Platforms
To add support for new platforms:

1. Create a new method in the `WeeklyStatsCurator` class
2. Add the platform configuration to the `__init__` method
3. Call the new method in `collect_all_stats()`
4. Update the environment template with new API credentials

### Modifying Metrics
To collect different metrics:

1. Update the `WeeklyStats` dataclass
2. Modify the platform-specific methods
3. Update the CSV export fieldnames
4. Adjust the summary output

## Security Notes

- Never commit your `.env` file to version control
- Keep your API credentials secure
- Regularly rotate your API keys
- Use environment-specific credentials for different deployments

## Contributing

Feel free to submit issues, feature requests, or pull requests to improve the script.

## License

This project is open source. Please check the license file for details.
