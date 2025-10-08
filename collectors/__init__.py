"""
Platform collectors for social media stats
"""

from .reddit_collector import RedditCollector
from .youtube_collector import YouTubeCollector
from .gsc_collector import GSCCollector
from .github_collector import GitHubCollector

__all__ = [
    'RedditCollector',
    'YouTubeCollector',
    'GSCCollector',
    'GitHubCollector'
]
