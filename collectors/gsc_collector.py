"""Google Search Console stats collector"""

from datetime import timedelta
import logging

logger = logging.getLogger(__name__)


class GSCCollector:
    """Collects Google Search Console statistics"""
    
    def __init__(self, credentials_file, property_url):
        self.credentials_file = credentials_file
        self.property_url = property_url
    
    def collect(self, start_date, end_date):
        """
        Collect GSC stats for date range
        
        Args:
            start_date: datetime object for start of period
            end_date: datetime object for end of period
            
        Returns:
            dict with stats: clicks, impressions, ctr, clicks_us
        """
        logger.info(f"Collecting Google Search Console stats for {self.property_url}")
        
        if not self.credentials_file or not self.property_url:
            logger.warning("Google Search Console credentials not configured")
            return self._empty_stats()
        
        try:
            from google.oauth2 import service_account
            from googleapiclient.discovery import build
            
            # Load credentials
            credentials = service_account.Credentials.from_service_account_file(
                self.credentials_file,
                scopes=['https://www.googleapis.com/auth/webmasters.readonly']
            )
            
            service = build('searchconsole', 'v1', credentials=credentials)
            
            # Get search analytics
            request = {
                'startDate': start_date.strftime('%Y-%m-%d'),
                'endDate': (end_date - timedelta(days=1)).strftime('%Y-%m-%d'),
                'dimensions': ['country'],
                'rowLimit': 1000
            }
            
            response = service.searchanalytics().query(
                siteUrl=self.property_url,
                body=request
            ).execute()
            
            rows = response.get('rows', [])
            
            # Calculate metrics
            us_clicks = 0
            total_impressions = 0
            total_clicks = 0
            
            for row in rows:
                if row['keys'][0] == 'usa':
                    us_clicks = row['clicks']
                total_impressions += row['impressions']
                total_clicks += row['clicks']
            
            ctr = (total_clicks / total_impressions * 100) if total_impressions > 0 else 0
            
            return {
                'clicks': total_clicks,
                'impressions': total_impressions,
                'ctr': round(ctr, 2),
                'clicks_us': us_clicks
            }
            
        except Exception as e:
            logger.error(f"Error collecting GSC stats: {e}")
            return self._empty_stats()
    
    def _empty_stats(self):
        """Return empty stats structure"""
        return {
            'clicks': 0,
            'impressions': 0,
            'ctr': 0,
            'clicks_us': 0
        }

