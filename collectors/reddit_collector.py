"""Reddit stats collector"""

import requests
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class RedditCollector:
    """Collects Reddit statistics"""
    
    def __init__(self, username):
        self.username = username
    
    def collect(self, start_date, end_date):
        """
        Collect Reddit stats for date range
        
        Args:
            start_date: datetime object for start of period
            end_date: datetime object for end of period
            
        Returns:
            dict with stats: posts_count, karma, comments, top_post, subreddits
        """
        logger.info(f"Collecting Reddit stats for u/{self.username}")
        
        try:
            # Use public API with browser-like headers
            headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
            }
            
            response = requests.get(
                f'https://www.reddit.com/user/{self.username}/submitted.json?limit=100',
                headers=headers,
                timeout=10
            )
            
            if response.status_code != 200:
                logger.error(f"Failed to fetch Reddit posts: {response.status_code}")
                return self._empty_stats()
            
            data = response.json()
            posts = data.get('data', {}).get('children', [])
            
            # Filter posts from date range
            week_posts = []
            total_karma = 0
            total_comments = 0
            subreddit_stats = {}
            
            for post in posts:
                post_data = post.get('data', {})
                post_date = datetime.fromtimestamp(post_data.get('created_utc', 0))
                
                if start_date <= post_date <= end_date:
                    week_posts.append(post_data)
                    karma = post_data.get('score', 0)
                    comments = post_data.get('num_comments', 0)
                    
                    total_karma += karma
                    total_comments += comments
                    
                    # Track by subreddit
                    subreddit = post_data.get('subreddit', 'unknown')
                    if subreddit not in subreddit_stats:
                        subreddit_stats[subreddit] = {'posts': 0, 'karma': 0}
                    subreddit_stats[subreddit]['posts'] += 1
                    subreddit_stats[subreddit]['karma'] += karma
            
            # Find top post
            top_post = None
            if week_posts:
                top_post = max(week_posts, key=lambda x: x.get('score', 0))
            
            return {
                'posts_count': len(week_posts),
                'karma': total_karma,
                'comments': total_comments,
                'avg_karma': total_karma / len(week_posts) if week_posts else 0,
                'avg_comments': total_comments / len(week_posts) if week_posts else 0,
                'top_post': {
                    'title': top_post.get('title', '') if top_post else '',
                    'score': top_post.get('score', 0) if top_post else 0,
                    'subreddit': top_post.get('subreddit', '') if top_post else '',
                    'url': f"https://reddit.com{top_post.get('permalink', '')}" if top_post else ''
                } if top_post else None,
                'subreddits': subreddit_stats
            }
            
        except Exception as e:
            logger.error(f"Error collecting Reddit stats: {e}")
            return self._empty_stats()
    
    def _empty_stats(self):
        """Return empty stats structure"""
        return {
            'posts_count': 0,
            'karma': 0,
            'comments': 0,
            'avg_karma': 0,
            'avg_comments': 0,
            'top_post': None,
            'subreddits': {}
        }

