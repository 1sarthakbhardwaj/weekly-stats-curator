"""LinkedIn organization stats collector"""

import requests
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class LinkedInCollector:
    """Collects LinkedIn organization statistics"""
    
    def __init__(self, access_token, organization_id):
        self.access_token = access_token
        self.organization_id = organization_id
    
    def collect(self, start_date, end_date):
        """
        Collect LinkedIn organization stats for date range
        
        Args:
            start_date: datetime object for start of period
            end_date: datetime object for end of period
            
        Returns:
            dict with stats: posts_count, likes, comments, shares, impressions
        """
        logger.info(f"Collecting LinkedIn stats for organization {self.organization_id}")
        
        if not self.access_token or not self.organization_id:
            logger.warning("LinkedIn credentials not configured")
            return self._empty_stats()
        
        try:
            headers = {
                'Authorization': f'Bearer {self.access_token}',
                'Content-Type': 'application/json',
                'X-Restli-Protocol-Version': '2.0.0'
            }
            
            org_urn = f"urn:li:organization:{self.organization_id}"
            
            # Get organization posts
            response = requests.get(
                'https://api.linkedin.com/v2/ugcPosts',
                headers=headers,
                params={
                    'q': 'authors',
                    'authors': f'List({org_urn})',
                    'count': 100
                }
            )
            
            if response.status_code != 200:
                logger.error(f"Failed to fetch LinkedIn posts: {response.status_code}")
                logger.debug(f"Response: {response.text}")
                return self._empty_stats()
            
            data = response.json()
            posts = data.get('elements', [])
            
            # Filter posts from date range
            start_time = int(start_date.timestamp() * 1000)
            end_time = int(end_date.timestamp() * 1000)
            
            week_posts = []
            total_likes = 0
            total_comments = 0
            total_shares = 0
            total_impressions = 0
            
            for post in posts:
                created_time = post.get('created', {}).get('time', 0)
                
                if start_time <= created_time <= end_time:
                    week_posts.append(post)
                    
                    # Try to get analytics for this post
                    post_id = post.get('id', '')
                    
                    try:
                        analytics_response = requests.get(
                            'https://api.linkedin.com/v2/organizationalEntityShareStatistics',
                            headers=headers,
                            params={
                                'q': 'organizationalEntity',
                                'organizationalEntity': org_urn,
                                'shares': f'List({post_id})'
                            }
                        )
                        
                        if analytics_response.status_code == 200:
                            analytics_data = analytics_response.json()
                            elements = analytics_data.get('elements', [])
                            
                            for element in elements:
                                stats = element.get('totalShareStatistics', {})
                                total_likes += stats.get('likeCount', 0)
                                total_comments += stats.get('commentCount', 0)
                                total_shares += stats.get('shareCount', 0)
                                total_impressions += stats.get('impressionCount', 0)
                    except Exception as e:
                        logger.debug(f"Could not fetch analytics for post: {e}")
            
            return {
                'posts_count': len(week_posts),
                'likes': total_likes,
                'comments': total_comments,
                'shares': total_shares,
                'impressions': total_impressions,
                'engagement_rate': (total_likes + total_comments + total_shares) / total_impressions * 100 if total_impressions > 0 else 0
            }
            
        except Exception as e:
            logger.error(f"Error collecting LinkedIn stats: {e}")
            return self._empty_stats()
    
    def _empty_stats(self):
        """Return empty stats structure"""
        return {
            'posts_count': 0,
            'likes': 0,
            'comments': 0,
            'shares': 0,
            'impressions': 0,
            'engagement_rate': 0
        }

