#!/usr/bin/env python3
"""
Social Media Stats Dashboard
A simple web app to view your weekly social media statistics
"""

import os
from datetime import datetime, timedelta
from flask import Flask, render_template, request, jsonify, session
from dotenv import load_dotenv
import logging

from collectors import (
    RedditCollector,
    YouTubeCollector,
    GSCCollector,
    GitHubCollector
)

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

# Flask app
app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'dev-secret-key-change-in-production')
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.jinja_env.auto_reload = True
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

# Store manual LinkedIn stats in memory (you could use a database instead)
linkedin_manual_stats = {}


def get_date_range(days=7):
    """Get date range for the last N days"""
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)
    return start_date, end_date


def collect_stats(platforms=None, days=7):
    """
    Collect stats from selected platforms
    
    Args:
        platforms: list of platform names (e.g. ['reddit', 'youtube'])
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
    
    # Reddit - Support up to 3 accounts
    if not platforms or 'reddit' in platforms:
        reddit_accounts = []
        for i in range(1, 4):  # Support 3 Reddit accounts
            username = os.getenv(f'REDDIT_USERNAME_{i}')
            display_name = os.getenv(f'REDDIT_DISPLAY_NAME_{i}', username)  # Default to username if no display name
            if username and username.strip():
                reddit_accounts.append({
                    'username': username,
                    'display_name': display_name if display_name and display_name.strip() else username
                })
        
        if reddit_accounts:
            # Collect stats for each Reddit account
            all_reddit_stats = []
            for account in reddit_accounts:
                collector = RedditCollector(account['username'])
                stats = collector.collect(start_date, end_date)
                stats['username'] = account['username']
                stats['display_name'] = account['display_name']
                all_reddit_stats.append(stats)
            
            # Always show individual accounts (even if only one)
            results['platforms']['reddit'] = {
                'accounts': all_reddit_stats,
                'total_posts': sum(s['posts_count'] for s in all_reddit_stats),
                'total_karma': sum(s['karma'] for s in all_reddit_stats),
                'total_comments': sum(s['comments'] for s in all_reddit_stats)
            }
    
    # YouTube
    if not platforms or 'youtube' in platforms:
        api_key = os.getenv('YOUTUBE_API_KEY')
        channel_id = os.getenv('YOUTUBE_CHANNEL_ID')
        if api_key and channel_id and api_key.strip() and api_key != 'your_youtube_api_key_here':
            try:
                collector = YouTubeCollector(api_key, channel_id)
                results['platforms']['youtube'] = collector.collect(start_date, end_date)
            except Exception as e:
                logger.error(f"YouTube collection failed: {e}")
                results['platforms']['youtube'] = {
                    'videos_count': 0, 'views': 0, 'likes': 0, 'comments': 0, 
                    'avg_views': 0, 'subscribers': 0, 'total_videos': 0, 'total_channel_views': 0
                }
        else:
            # Show placeholder if not configured
            results['platforms']['youtube'] = {
                'videos_count': 0, 'views': 0, 'likes': 0, 'comments': 0,
                'avg_views': 0, 'subscribers': 0, 'total_videos': 0, 'total_channel_views': 0,
                'error': 'API not configured'
            }
    
    # Google Search Console
    if not platforms or 'gsc' in platforms:
        credentials_file = os.getenv('GSC_CREDENTIALS_FILE')
        property_url = os.getenv('GSC_PROPERTY_URL')
        if credentials_file and property_url and credentials_file != 'path/to/gsc-credentials.json':
            try:
                collector = GSCCollector(credentials_file, property_url)
                results['platforms']['gsc'] = collector.collect(start_date, end_date)
            except Exception as e:
                logger.error(f"GSC collection failed: {e}")
                results['platforms']['gsc'] = {
                    'clicks': 0, 'impressions': 0, 'ctr': 0, 'clicks_us': 0
                }
        else:
            # Show placeholder if not configured
            results['platforms']['gsc'] = {
                'clicks': 0, 'impressions': 0, 'ctr': 0, 'clicks_us': 0,
                'error': 'API not configured'
            }
    
    # GitHub
    if not platforms or 'github' in platforms:
        github_username = os.getenv('GITHUB_USERNAME')
        github_token = os.getenv('GITHUB_TOKEN')  # Optional, but recommended for higher rate limits
        if github_username and github_username.strip():
            try:
                collector = GitHubCollector(github_username, github_token)
                results['platforms']['github'] = collector.collect(start_date, end_date)
            except Exception as e:
                logger.error(f"GitHub collection failed: {e}")
                results['platforms']['github'] = {
                    'username': github_username,
                    'public_repos': 0,
                    'followers': 0,
                    'following': 0,
                    'total_stars': 0,
                    'total_forks': 0,
                    'commits_count': 0,
                    'recent_activity': []
                }
        else:
            # Show placeholder if not configured
            results['platforms']['github'] = {
                'username': '',
                'public_repos': 0,
                'followers': 0,
                'following': 0,
                'total_stars': 0,
                'total_forks': 0,
                'commits_count': 0,
                'recent_activity': [],
                'error': 'Username not configured'
            }
    
    return results


@app.route('/')
def index():
    """Main dashboard page"""
    # Get selected platforms from query params
    selected = request.args.getlist('platform')
    days = int(request.args.get('days', 7))
    
    # Collect stats
    stats = collect_stats(platforms=selected if selected else None, days=days)
    
    # Add LinkedIn manual stats if available
    if linkedin_manual_stats:
        stats['platforms']['linkedin'] = linkedin_manual_stats
    
    return render_template('dashboard.html', 
                         stats=stats, 
                         selected=selected if selected else ['reddit', 'youtube', 'gsc', 'github'],
                         days=days)


@app.route('/api/linkedin', methods=['POST'])
def save_linkedin_stats():
    """Save manually entered LinkedIn stats"""
    global linkedin_manual_stats
    
    data = request.get_json()
    linkedin_manual_stats = {
        'posts_count': int(data.get('posts_count', 0)),
        'likes': int(data.get('likes', 0)),
        'comments': int(data.get('comments', 0)),
        'shares': int(data.get('shares', 0)),
        'impressions': int(data.get('impressions', 0)),
        'engagement_rate': float(data.get('engagement_rate', 0)),
        'manual': True
    }
    
    return jsonify({'success': True, 'message': 'LinkedIn stats saved!'})


if __name__ == '__main__':
    # Check if running in production or local
    is_production = os.getenv('RENDER') or os.getenv('RAILWAY_ENVIRONMENT') or os.getenv('VERCEL')
    
    if not is_production:
        print("\n" + "="*60)
        print("🚀 Social Media Stats Dashboard")
        print("="*60)
        print("\nStarting web server...")
        print("Open your browser and go to: http://localhost:5050")
        print("\nPress Ctrl+C to stop the server\n")
    
    # Get port from environment variable (for deployment) or use 5050 for local
    port = int(os.getenv('PORT', 5050))
    debug_mode = not is_production
    
    app.run(debug=debug_mode, host='0.0.0.0', port=port)

