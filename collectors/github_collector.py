"""GitHub stats collector"""

import requests
from datetime import datetime
import logging
import os

logger = logging.getLogger(__name__)


class GitHubCollector:
    """Collects GitHub statistics"""
    
    def __init__(self, username, token=None):
        self.username = username
        self.token = token
        self.base_url = "https://api.github.com"
    
    def collect(self, start_date, end_date):
        """
        Collect GitHub stats for date range
        
        Args:
            start_date: datetime object for start of period
            end_date: datetime object for end of period
            
        Returns:
            dict with stats: commits, repositories, stars, followers, contributions
        """
        logger.info(f"Collecting GitHub stats for {self.username}")
        
        try:
            headers = {
                'User-Agent': 'SocialMediaStatsDashboard/1.0',
                'Accept': 'application/vnd.github.v3+json'
            }
            
            if self.token:
                headers['Authorization'] = f'token {self.token}'
            
            # Get user profile info
            profile = self._get_user_profile(headers)
            
            # Get repository stats
            repo_stats = self._get_repository_stats(headers)
            
            # Get commit activity (approximate)
            commit_stats = self._get_commit_stats(headers, start_date, end_date)
            
            return {
                'username': self.username,
                'public_repos': profile.get('public_repos', 0),
                'followers': profile.get('followers', 0),
                'following': profile.get('following', 0),
                'total_stars': repo_stats.get('total_stars', 0),
                'total_forks': repo_stats.get('total_forks', 0),
                'commits_count': commit_stats.get('commits_count', 0),
                'recent_activity': commit_stats.get('recent_activity', [])
            }
            
        except Exception as e:
            logger.error(f"Error collecting GitHub stats: {e}")
            return self._empty_stats()
    
    def _get_user_profile(self, headers):
        """Get user profile information"""
        response = requests.get(
            f'{self.base_url}/users/{self.username}',
            headers=headers,
            timeout=10
        )
        
        if response.status_code == 200:
            return response.json()
        else:
            logger.warning(f"Failed to fetch GitHub profile: {response.status_code}")
            return {}
    
    def _get_repository_stats(self, headers):
        """Get repository statistics"""
        response = requests.get(
            f'{self.base_url}/users/{self.username}/repos?per_page=100',
            headers=headers,
            timeout=10
        )
        
        if response.status_code == 200:
            repos = response.json()
            total_stars = sum(repo.get('stargazers_count', 0) for repo in repos)
            total_forks = sum(repo.get('forks_count', 0) for repo in repos)
            
            return {
                'total_stars': total_stars,
                'total_forks': total_forks,
                'repos_count': len(repos)
            }
        else:
            logger.warning(f"Failed to fetch GitHub repositories: {response.status_code}")
            return {'total_stars': 0, 'total_forks': 0, 'repos_count': 0}
    
    def _get_commit_stats(self, headers, start_date, end_date):
        """Get commit statistics (approximate using events API)"""
        # This is an approximation since GitHub's commit API is complex
        # We'll use the events API to get recent activity
        response = requests.get(
            f'{self.base_url}/users/{self.username}/events?per_page=100',
            headers=headers,
            timeout=10
        )
        
        if response.status_code == 200:
            events = response.json()
            commits_count = 0
            recent_activity = []
            
            for event in events:
                event_date = datetime.strptime(event['created_at'], '%Y-%m-%dT%H:%M:%SZ')
                if start_date <= event_date <= end_date:
                    if event['type'] == 'PushEvent':
                        commits_count += len(event.get('payload', {}).get('commits', []))
                    recent_activity.append({
                        'type': event['type'],
                        'repo': event['repo']['name'],
                        'created_at': event['created_at']
                    })
            
            return {
                'commits_count': commits_count,
                'recent_activity': recent_activity
            }
        else:
            logger.warning(f"Failed to fetch GitHub events: {response.status_code}")
            return {'commits_count': 0, 'recent_activity': []}
    
    def _empty_stats(self):
        """Return empty stats structure"""
        return {
            'username': self.username,
            'public_repos': 0,
            'followers': 0,
            'following': 0,
            'total_stars': 0,
            'total_forks': 0,
            'commits_count': 0,
            'recent_activity': [],
            'error': 'API not configured or failed'
        }

