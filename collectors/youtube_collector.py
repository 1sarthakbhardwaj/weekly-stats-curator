"""YouTube stats collector"""

import logging

logger = logging.getLogger(__name__)


class YouTubeCollector:
    """Collects YouTube statistics"""
    
    def __init__(self, api_key, channel_id):
        self.api_key = api_key
        self.channel_id = channel_id
    
    def collect(self, start_date, end_date):
        """
        Collect YouTube stats for date range
        
        Args:
            start_date: datetime object for start of period
            end_date: datetime object for end of period
            
        Returns:
            dict with stats: videos_count, views, likes, comments
        """
        logger.info(f"Collecting YouTube stats for channel {self.channel_id}")
        
        if not self.api_key or not self.channel_id:
            logger.warning("YouTube credentials not configured")
            return self._empty_stats()
        
        try:
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
            
        except Exception as e:
            logger.error(f"Error collecting YouTube stats: {e}")
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

