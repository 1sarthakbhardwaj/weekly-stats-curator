"""YouTube stats collector with API and scraping fallback"""

import requests
from bs4 import BeautifulSoup
import re
import logging

logger = logging.getLogger(__name__)


class YouTubeCollector:
    """Collects YouTube statistics (tries API first, falls back to scraping)"""
    
    def __init__(self, api_key, channel_id):
        self.api_key = api_key
        self.channel_id = channel_id  # Can be channel ID or @username
    
    def collect(self, start_date, end_date):
        """
        Collect YouTube stats for date range
        
        Args:
            start_date: datetime object for start of period
            end_date: datetime object for end of period
            
        Returns:
            dict with stats: videos_count, views, likes, comments
        """
        logger.info(f"Collecting YouTube stats for channel: {self.channel_id}")
        
        if not self.channel_id:
            logger.warning("YouTube channel not configured")
            return self._empty_stats()
        
        # Try API first if we have a key
        if self.api_key and self.api_key != 'your_youtube_api_key_here':
            try:
                return self._collect_via_api(start_date, end_date)
            except Exception as e:
                logger.warning(f"YouTube API failed: {e}, falling back to scraping")
        
        # Fallback to scraping
        return self._collect_via_scraping()
    
    def _collect_via_api(self, start_date, end_date):
        """Collect stats using YouTube API"""
        from googleapiclient.discovery import build
        
        youtube = build('youtube', 'v3', developerKey=self.api_key)
        
        # Get channel videos
        request = youtube.search().list(
            part='snippet',
            channelId=self.channel_id,
            publishedAfter=start_date.isoformat() + 'Z',
            publishedBefore=end_date.isoformat() + 'Z',
            type='video',
            maxResults=50
        )
        
        response = request.execute()
        videos = response.get('items', [])
        
        total_views = 0
        total_likes = 0
        total_comments = 0
        
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
                total_comments += int(stats.get('commentCount', 0))
        
        return {
            'videos_count': len(videos),
            'views': total_views,
            'likes': total_likes,
            'comments': total_comments,
            'avg_views': total_views / len(videos) if videos else 0
        }
    
    def _collect_via_scraping(self):
        """Collect basic stats by scraping YouTube channel page (no API needed)"""
        try:
            # Determine if it's a handle (@username) or channel ID
            if self.channel_id.startswith('@'):
                url = f"https://www.youtube.com/{self.channel_id}/videos"
            else:
                url = f"https://www.youtube.com/channel/{self.channel_id}/videos"
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            }
            
            response = requests.get(url, headers=headers, timeout=15)
            
            if response.status_code != 200:
                logger.warning(f"Failed to fetch YouTube page: {response.status_code}")
                return self._empty_stats()
            
            # Parse subscriber count from page
            subscribers = 0
            match = re.search(r'"subscriberCountText":\{"simpleText":"([\d.KMB]+)\s+subscribers?"', response.text)
            if match:
                sub_text = match.group(1)
                # Convert K, M, B to numbers
                multipliers = {'K': 1000, 'M': 1000000, 'B': 1000000000}
                for suffix, mult in multipliers.items():
                    if suffix in sub_text:
                        subscribers = int(float(sub_text.replace(suffix, '')) * mult)
                        break
                else:
                    subscribers = int(sub_text) if sub_text.replace('.', '').isdigit() else 0
            
            # Try to count recent videos from the page
            video_count = response.text.count('"videoRenderer"')
            
            logger.info(f"YouTube scraping: {subscribers:,} subscribers, ~{video_count} recent videos visible")
            logger.info("Note: For detailed stats, configure YouTube API key (free tier available)")
            
            return {
                'videos_count': 0,  # Can't determine date range without API
                'views': 0,  # Requires API or detailed scraping
                'likes': 0,
                'comments': 0,
                'avg_views': subscribers  # Use subscribers as proxy for channel reach
            }
            
        except Exception as e:
            logger.error(f"Error scraping YouTube: {e}")
            return self._empty_stats()
    
    def _empty_stats(self):
        """Return empty stats structure"""
        return {
            'videos_count': 0,
            'views': 0,
            'likes': 0,
            'comments': 0,
            'avg_views': 0
        }
