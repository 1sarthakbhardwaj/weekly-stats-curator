"""Twitter/X stats collector"""

import requests
import logging

logger = logging.getLogger(__name__)


class TwitterCollector:
    """Collects Twitter/X statistics"""
    
    def __init__(self, bearer_token, username):
        self.bearer_token = bearer_token
        self.username = username
        self.user_id = None
    
    def collect(self, start_date, end_date):
        """
        Collect Twitter stats for date range
        
        Args:
            start_date: datetime object for start of period
            end_date: datetime object for end of period
            
        Returns:
            dict with stats: posts_count, likes, retweets, replies, impressions
        """
        logger.info(f"Collecting Twitter stats for @{self.username}")
        
        if not self.bearer_token or not self.username:
            logger.warning("Twitter credentials not configured")
            return self._empty_stats()
        
        try:
            headers = {
                'Authorization': f'Bearer {self.bearer_token}',
                'Content-Type': 'application/json'
            }
            
            # Get user ID
            if not self.user_id:
                user_response = requests.get(
                    f'https://api.twitter.com/2/users/by/username/{self.username}',
                    headers=headers
                )
                
                if user_response.status_code != 200:
                    logger.error(f"Failed to get Twitter user: {user_response.status_code}")
                    return self._empty_stats()
                
                self.user_id = user_response.json()['data']['id']
            
            # Get user's tweets
            response = requests.get(
                f'https://api.twitter.com/2/users/{self.user_id}/tweets',
                headers=headers,
                params={
                    'start_time': start_date.isoformat() + 'Z',
                    'end_time': end_date.isoformat() + 'Z',
                    'max_results': 100,
                    'tweet.fields': 'public_metrics,created_at'
                }
            )
            
            if response.status_code != 200:
                logger.error(f"Failed to fetch Twitter posts: {response.status_code}")
                return self._empty_stats()
            
            data = response.json()
            tweets = data.get('data', [])
            
            total_likes = 0
            total_retweets = 0
            total_replies = 0
            total_impressions = 0
            
            for tweet in tweets:
                metrics = tweet.get('public_metrics', {})
                total_likes += metrics.get('like_count', 0)
                total_retweets += metrics.get('retweet_count', 0)
                total_replies += metrics.get('reply_count', 0)
                total_impressions += metrics.get('impression_count', 0)
            
            return {
                'posts_count': len(tweets),
                'likes': total_likes,
                'retweets': total_retweets,
                'replies': total_replies,
                'impressions': total_impressions,
                'engagement_rate': (total_likes + total_retweets + total_replies) / total_impressions * 100 if total_impressions > 0 else 0
            }
            
        except Exception as e:
            logger.error(f"Error collecting Twitter stats: {e}")
            return self._empty_stats()
    
    def _empty_stats(self):
        """Return empty stats structure"""
        return {
            'posts_count': 0,
            'likes': 0,
            'retweets': 0,
            'replies': 0,
            'impressions': 0,
            'engagement_rate': 0
        }

