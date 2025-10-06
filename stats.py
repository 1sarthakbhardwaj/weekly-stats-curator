#!/usr/bin/env python3
"""
Social Media Stats Dashboard
A simple web app to view your weekly social media statistics
"""

import os
from datetime import datetime, timedelta
from flask import Flask, render_template, request
from dotenv import load_dotenv
import logging

from collectors import (
    RedditCollector,
    LinkedInCollector,
    TwitterCollector,
    YouTubeCollector,
    GSCCollector
)

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

# Flask app
app = Flask(__name__)


def get_date_range(days=7):
    """Get date range for the last N days"""
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)
    return start_date, end_date


def collect_stats(platforms=None, days=7):
    """
    Collect stats from selected platforms
    
    Args:
        platforms: list of platform names (e.g. ['reddit', 'linkedin'])
                  If None, collects from all configured platforms
        days: number of days to look back
    
    Returns:
        dict with stats for each platform
    """
    start_date, end_date = get_date_range(days)
    results = {
        'start_date': start_date.strftime('%Y-%m-%d'),
        'end_date': end_date.strftime('%Y-%m-%d'),
        'platforms': {}
    }
    
    # Reddit
    if not platforms or 'reddit' in platforms:
        username = os.getenv('REDDIT_USERNAME')
        if username:
            collector = RedditCollector(username)
            results['platforms']['reddit'] = collector.collect(start_date, end_date)
    
    # LinkedIn
    if not platforms or 'linkedin' in platforms:
        access_token = os.getenv('LINKEDIN_ACCESS_TOKEN')
        org_id = os.getenv('LINKEDIN_ORGANIZATION_ID')
        if access_token and org_id:
            collector = LinkedInCollector(access_token, org_id)
            results['platforms']['linkedin'] = collector.collect(start_date, end_date)
    
    # Twitter/X
    if not platforms or 'twitter' in platforms:
        bearer_token = os.getenv('TWITTER_BEARER_TOKEN')
        username = os.getenv('TWITTER_USERNAME')
        if bearer_token and username:
            collector = TwitterCollector(bearer_token, username)
            results['platforms']['twitter'] = collector.collect(start_date, end_date)
    
    # YouTube
    if not platforms or 'youtube' in platforms:
        api_key = os.getenv('YOUTUBE_API_KEY')
        channel_id = os.getenv('YOUTUBE_CHANNEL_ID')
        if api_key and channel_id:
            collector = YouTubeCollector(api_key, channel_id)
            results['platforms']['youtube'] = collector.collect(start_date, end_date)
    
    # Google Search Console
    if not platforms or 'gsc' in platforms:
        credentials_file = os.getenv('GSC_CREDENTIALS_FILE')
        property_url = os.getenv('GSC_PROPERTY_URL')
        if credentials_file and property_url:
            collector = GSCCollector(credentials_file, property_url)
            results['platforms']['gsc'] = collector.collect(start_date, end_date)
    
    return results


@app.route('/')
def index():
    """Main dashboard page"""
    # Get selected platforms from query params
    selected = request.args.getlist('platform')
    days = int(request.args.get('days', 7))
    
    # Collect stats
    stats = collect_stats(platforms=selected if selected else None, days=days)
    
    return render_template('dashboard.html', 
                         stats=stats, 
                         selected=selected if selected else ['reddit', 'linkedin', 'twitter', 'youtube', 'gsc'],
                         days=days)


if __name__ == '__main__':
    print("\n" + "="*60)
    print("🚀 Social Media Stats Dashboard")
    print("="*60)
    print("\nStarting web server...")
    print("Open your browser and go to: http://localhost:5000")
    print("\nPress Ctrl+C to stop the server\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000)

