#!/usr/bin/env python3
"""
Weekly Stats Curator Script
Collects metrics from various social media platforms and Google Search Console
for weekly reporting starting from September 22nd.
"""

import os
import csv
import json
import requests
import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import logging
from dataclasses import dataclass
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

@dataclass
class WeeklyStats:
    """Data class for weekly statistics"""
    channel: str
    posts_count: int
    karma: Optional[int] = None
    impressions: Optional[int] = None
    ctr: Optional[float] = None
    likes: Optional[int] = None
    clicks_us: Optional[int] = None

class WeeklyStatsCurator:
    """Main class for curating weekly statistics from various platforms"""
    
    def __init__(self):
        self.start_date = datetime(2024, 9, 22)  # Week starting September 22nd
        self.end_date = self.start_date + timedelta(days=7)
        self.stats: List[WeeklyStats] = []
        
        # API configurations
        self.reddit_config = {
            'client_id': os.getenv('REDDIT_CLIENT_ID'),
            'client_secret': os.getenv('REDDIT_CLIENT_SECRET'),
            'user_agent': os.getenv('REDDIT_USER_AGENT', 'WeeklyStatsCurator/1.0'),
            'username': os.getenv('REDDIT_USERNAME'),
            'password': os.getenv('REDDIT_PASSWORD')
        }
        
        self.linkedin_config = {
            'access_token': os.getenv('LINKEDIN_ACCESS_TOKEN'),
            'organization_id': os.getenv('LINKEDIN_ORGANIZATION_ID')
        }
        
        self.twitter_config = {
            'bearer_token': os.getenv('TWITTER_BEARER_TOKEN'),
            'api_key': os.getenv('TWITTER_API_KEY'),
            'api_secret': os.getenv('TWITTER_API_SECRET'),
            'access_token': os.getenv('TWITTER_ACCESS_TOKEN'),
            'access_token_secret': os.getenv('TWITTER_ACCESS_TOKEN_SECRET')
        }
        
        self.youtube_config = {
            'api_key': os.getenv('YOUTUBE_API_KEY'),
            'channel_id': os.getenv('YOUTUBE_CHANNEL_ID')
        }
        
        self.gsc_config = {
            'credentials_file': os.getenv('GSC_CREDENTIALS_FILE'),
            'property_url': os.getenv('GSC_PROPERTY_URL')
        }

    def get_reddit_stats(self) -> WeeklyStats:
        """Get Reddit statistics for the week"""
        logger.info("Fetching Reddit stats...")
        
        try:
            # Reddit API authentication
            auth = requests.auth.HTTPBasicAuth(
                self.reddit_config['client_id'], 
                self.reddit_config['client_secret']
            )
            
            data = {
                'grant_type': 'password',
                'username': self.reddit_config['username'],
                'password': self.reddit_config['password']
            }
            
            headers = {'User-Agent': self.reddit_config['user_agent']}
            
            # Get access token
            response = requests.post(
                'https://www.reddit.com/api/v1/access_token',
                auth=auth,
                data=data,
                headers=headers
            )
            
            if response.status_code != 200:
                logger.warning("Reddit authentication failed")
                return WeeklyStats(channel="reddit", posts_count=0)
            
            token = response.json()['access_token']
            headers['Authorization'] = f'bearer {token}'
            
            # Get user's posts
            response = requests.get(
                f'https://oauth.reddit.com/user/{self.reddit_config["username"]}/submitted',
                headers=headers,
                params={'limit': 100}
            )
            
            if response.status_code != 200:
                logger.warning("Failed to fetch Reddit posts")
                return WeeklyStats(channel="reddit", posts_count=0)
            
            posts = response.json()['data']['children']
            
            # Filter posts from the specified week
            week_posts = []
            total_karma = 0
            
            for post in posts:
                post_date = datetime.fromtimestamp(post['data']['created_utc'])
                if self.start_date <= post_date < self.end_date:
                    week_posts.append(post)
                    total_karma += post['data']['score']
            
            return WeeklyStats(
                channel="reddit",
                posts_count=len(week_posts),
                karma=total_karma
            )
            
        except Exception as e:
            logger.error(f"Error fetching Reddit stats: {e}")
            return WeeklyStats(channel="reddit", posts_count=0)

    def get_linkedin_stats(self) -> WeeklyStats:
        """Get LinkedIn statistics for the week"""
        logger.info("Fetching LinkedIn stats...")
        
        try:
            headers = {
                'Authorization': f'Bearer {self.linkedin_config["access_token"]}',
                'Content-Type': 'application/json'
            }
            
            # Get organization shares
            url = f'https://api.linkedin.com/v2/shares'
            params = {
                'q': 'owners',
                'owners': f'urn:li:organization:{self.linkedin_config["organization_id"]}',
                'count': 100
            }
            
            response = requests.get(url, headers=headers, params=params)
            
            if response.status_code != 200:
                logger.warning("Failed to fetch LinkedIn posts")
                return WeeklyStats(channel="linkedin", posts_count=0)
            
            data = response.json()
            posts = data.get('elements', [])
            
            # Filter posts from the specified week
            week_posts = []
            total_likes = 0
            total_impressions = 0
            
            for post in posts:
                post_date = datetime.fromtimestamp(post['created']['time'] / 1000)
                if self.start_date <= post_date < self.end_date:
                    week_posts.append(post)
                    # Note: Detailed engagement metrics require additional API calls
            
            return WeeklyStats(
                channel="linkedin",
                posts_count=len(week_posts),
                likes=total_likes,
                impressions=total_impressions
            )
            
        except Exception as e:
            logger.error(f"Error fetching LinkedIn stats: {e}")
            return WeeklyStats(channel="linkedin", posts_count=0)

    def get_twitter_stats(self) -> WeeklyStats:
        """Get X (Twitter) statistics for the week"""
        logger.info("Fetching Twitter stats...")
        
        try:
            headers = {
                'Authorization': f'Bearer {self.twitter_config["bearer_token"]}',
                'Content-Type': 'application/json'
            }
            
            # Get user's tweets
            user_id = self._get_twitter_user_id()
            if not user_id:
                return WeeklyStats(channel="x", posts_count=0)
            
            url = f'https://api.twitter.com/2/users/{user_id}/tweets'
            params = {
                'start_time': self.start_date.isoformat() + 'Z',
                'end_time': self.end_date.isoformat() + 'Z',
                'max_results': 100,
                'tweet.fields': 'public_metrics,created_at'
            }
            
            response = requests.get(url, headers=headers, params=params)
            
            if response.status_code != 200:
                logger.warning("Failed to fetch Twitter posts")
                return WeeklyStats(channel="x", posts_count=0)
            
            data = response.json()
            tweets = data.get('data', [])
            
            total_likes = sum(tweet['public_metrics']['like_count'] for tweet in tweets)
            total_impressions = sum(tweet['public_metrics']['impression_count'] for tweet in tweets)
            
            return WeeklyStats(
                channel="x",
                posts_count=len(tweets),
                likes=total_likes,
                impressions=total_impressions
            )
            
        except Exception as e:
            logger.error(f"Error fetching Twitter stats: {e}")
            return WeeklyStats(channel="x", posts_count=0)

    def _get_twitter_user_id(self) -> Optional[str]:
        """Get Twitter user ID from username"""
        try:
            headers = {
                'Authorization': f'Bearer {self.twitter_config["bearer_token"]}',
                'Content-Type': 'application/json'
            }
            
            username = os.getenv('TWITTER_USERNAME')
            if not username:
                return None
            
            url = f'https://api.twitter.com/2/users/by/username/{username}'
            response = requests.get(url, headers=headers)
            
            if response.status_code == 200:
                return response.json()['data']['id']
            return None
            
        except Exception as e:
            logger.error(f"Error getting Twitter user ID: {e}")
            return None

    def get_youtube_stats(self) -> WeeklyStats:
        """Get YouTube statistics for the week"""
        logger.info("Fetching YouTube stats...")
        
        try:
            from googleapiclient.discovery import build
            
            youtube = build('youtube', 'v3', developerKey=self.youtube_config['api_key'])
            
            # Get channel videos
            request = youtube.search().list(
                part='snippet',
                channelId=self.youtube_config['channel_id'],
                publishedAfter=self.start_date.isoformat() + 'Z',
                publishedBefore=self.end_date.isoformat() + 'Z',
                type='video',
                maxResults=50
            )
            
            response = request.execute()
            videos = response.get('items', [])
            
            total_views = 0
            total_likes = 0
            
            for video in videos:
                video_id = video['id']['videoId']
                
                # Get video statistics
                stats_request = youtube.videos().list(
                    part='statistics',
                    id=video_id
                )
                stats_response = stats_request.execute()
                
                if stats_response['items']:
                    stats = stats_response['items'][0]['statistics']
                    total_views += int(stats.get('viewCount', 0))
                    total_likes += int(stats.get('likeCount', 0))
            
            return WeeklyStats(
                channel="youtube",
                posts_count=len(videos),
                impressions=total_views,
                likes=total_likes
            )
            
        except Exception as e:
            logger.error(f"Error fetching YouTube stats: {e}")
            return WeeklyStats(channel="youtube", posts_count=0)

    def get_gsc_stats(self) -> WeeklyStats:
        """Get Google Search Console statistics for the week"""
        logger.info("Fetching Google Search Console stats...")
        
        try:
            from google.oauth2 import service_account
            from googleapiclient.discovery import build
            
            # Load credentials
            credentials = service_account.Credentials.from_service_account_file(
                self.gsc_config['credentials_file'],
                scopes=['https://www.googleapis.com/auth/webmasters.readonly']
            )
            
            service = build('searchconsole', 'v1', credentials=credentials)
            
            # Get search analytics
            request = {
                'startDate': self.start_date.strftime('%Y-%m-%d'),
                'endDate': (self.end_date - timedelta(days=1)).strftime('%Y-%m-%d'),
                'dimensions': ['country'],
                'rowLimit': 1000
            }
            
            response = service.searchanalytics().query(
                siteUrl=self.gsc_config['property_url'],
                body=request
            ).execute()
            
            rows = response.get('rows', [])
            
            # Calculate US-specific metrics
            us_clicks = 0
            total_impressions = 0
            total_clicks = 0
            
            for row in rows:
                if row['keys'][0] == 'usa':  # US country code
                    us_clicks = row['clicks']
                total_impressions += row['impressions']
                total_clicks += row['clicks']
            
            ctr = (total_clicks / total_impressions * 100) if total_impressions > 0 else 0
            
            return WeeklyStats(
                channel="google search console",
                posts_count=0,  # GSC doesn't track posts
                impressions=total_impressions,
                ctr=round(ctr, 2),
                clicks_us=us_clicks
            )
            
        except Exception as e:
            logger.error(f"Error fetching GSC stats: {e}")
            return WeeklyStats(channel="google search console", posts_count=0)

    def collect_all_stats(self) -> List[WeeklyStats]:
        """Collect statistics from all platforms"""
        logger.info("Starting weekly stats collection...")
        
        # Collect stats from each platform
        self.stats = [
            self.get_reddit_stats(),
            self.get_linkedin_stats(),
            self.get_twitter_stats(),
            self.get_youtube_stats(),
            self.get_gsc_stats()
        ]
        
        return self.stats

    def export_to_csv(self, filename: str = None) -> str:
        """Export statistics to CSV file"""
        if not filename:
            filename = f"weekly_stats_{self.start_date.strftime('%Y%m%d')}.csv"
        
        filepath = os.path.join(os.getcwd(), filename)
        
        with open(filepath, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = [
                'Channel', 'Posts Count', 'Karma', 'Impressions', 
                'CTR', 'Likes', 'Clicks (US)'
            ]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            writer.writeheader()
            for stat in self.stats:
                writer.writerow({
                    'Channel': stat.channel,
                    'Posts Count': stat.posts_count,
                    'Karma': stat.karma or '',
                    'Impressions': stat.impressions or '',
                    'CTR': stat.ctr or '',
                    'Likes': stat.likes or '',
                    'Clicks (US)': stat.clicks_us or ''
                })
        
        logger.info(f"Stats exported to {filepath}")
        return filepath

    def print_summary(self):
        """Print a summary of collected statistics"""
        print("\n" + "="*80)
        print("WEEKLY STATS SUMMARY")
        print(f"Week starting: {self.start_date.strftime('%B %d, %Y')}")
        print("="*80)
        
        for stat in self.stats:
            print(f"\n{stat.channel.upper()}:")
            print(f"  Posts: {stat.posts_count}")
            if stat.karma is not None:
                print(f"  Karma: {stat.karma}")
            if stat.impressions is not None:
                print(f"  Impressions: {stat.impressions:,}")
            if stat.ctr is not None:
                print(f"  CTR: {stat.ctr}%")
            if stat.likes is not None:
                print(f"  Likes: {stat.likes:,}")
            if stat.clicks_us is not None:
                print(f"  Clicks (US): {stat.clicks_us:,}")

def main():
    """Main function to run the weekly stats curator"""
    curator = WeeklyStatsCurator()
    
    try:
        # Collect all statistics
        stats = curator.collect_all_stats()
        
        # Print summary
        curator.print_summary()
        
        # Export to CSV
        csv_file = curator.export_to_csv()
        print(f"\nDetailed stats exported to: {csv_file}")
        
    except Exception as e:
        logger.error(f"Error in main execution: {e}")
        print(f"Error: {e}")
        print("Please check your environment configuration and API credentials.")

if __name__ == "__main__":
    main()
