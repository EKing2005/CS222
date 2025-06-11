import sys
import requests
import json
from datetime import datetime
from typing import Dict, List, Optional, Tuple


class WikipediaEditTracker:
    """Main class for tracking Wikipedia edits."""
    
    BASE_URL = "https://en.wikipedia.org/w/api.php"
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'WikipediaEditTracker/1.0 (Educational Project)'
        })
    
    def get_page_revisions(self, page_title: str, limit: int = 30) -> Tuple[List[Dict], Optional[str]]:
        """
        Retrieve recent revisions for a Wikipedia page.
        
        Args:
            page_title: The title of the Wikipedia page
            limit: Maximum number of revisions to retrieve (default: 30)
            
        Returns:
            Tuple of (revisions_list, redirect_title)
            
        Raises:
            requests.RequestException: For network errors
            ValueError: For invalid page titles or API errors
        """
        params = {
            'action': 'query',
            'format': 'json',
            'prop': 'revisions',
            'titles': page_title,
            'rvprop': 'timestamp|user',
            'rvlimit': limit,
            'redirects': 1
        }
        
        try:
            response = self.session.get(self.BASE_URL, params=params, timeout=10)
            response.raise_for_status()
        except requests.RequestException as e:
            raise requests.RequestException(f"Network error: {e}")
        
        try:
            data = response.json()
        except json.JSONDecodeError:
            raise ValueError("Invalid response from Wikipedia API")
        
        # Check for API errors
        if 'error' in data:
            error_code = data['error'].get('code', 'unknown')
            error_info = data['error'].get('info', 'Unknown error')
            raise ValueError(f"API error ({error_code}): {error_info}")
        
        # Check for redirects
        redirect_title = None
        if 'redirects' in data.get('query', {}):
            redirects = data['query']['redirects']
            if redirects:
                redirect_title = redirects[0]['to']
        
        # Extract page data
        pages = data.get('query', {}).get('pages', {})
        
        if not pages:
            raise ValueError("No page data found")
        
        # Get the first (and should be only) page
        page_data = next(iter(pages.values()))
        
        # Check if page exists
        if 'missing' in page_data:
            raise ValueError("Page not found")
        
        # Extract revisions
        revisions = page_data.get('revisions', [])
        
        return revisions, redirect_title
    
    def format_timestamp(self, timestamp: str) -> str:
        """
        Format ISO timestamp to a more readable format.
        
        Args:
            timestamp: ISO format timestamp string
            
        Returns:
            Formatted timestamp string
        """
        try:
            dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
            return dt.strftime('%Y-%m-%d %H:%M:%S')
        except ValueError:
            return timestamp
    
    def run(self, page_title: str) -> int:
        """
        Main execution method.
        
        Args:
            page_title: Wikipedia page title to analyze
            
        Returns:
            Exit code (0 for success, 2 for page not found, 3 for network error)
        """
        try:
            revisions, redirect_title = self.get_page_revisions(page_title)
            
            # Print redirect message if applicable
            if redirect_title:
                print(f"Redirected to {redirect_title}")
            
            # Print revisions in reverse chronological order (already sorted by API)
            for revision in revisions:
                timestamp = self.format_timestamp(revision['timestamp'])
                user = revision.get('user', 'Unknown')
                print(f"{timestamp} {user}")
            
            return 0
            
        except ValueError as e:
            if "Page not found" in str(e):
                print(f"Error: No Wikipedia page found for '{page_title}'", file=sys.stderr)
                return 2
            else:
                print(f"Error: {e}", file=sys.stderr)
                return 3
                
        except requests.RequestException as e:
            print(f"Network error: {e}", file=sys.stderr)
            return 3


def main():
    """Main entry point for the application."""
    if len(sys.argv) != 2:
        print("Usage: python wiki_tracker.py <article_name>", file=sys.stderr)
        print("Example: python wiki_tracker.py 'Ball State University'", file=sys.stderr)
        return 1
    
    page_title = sys.argv[1]
    
    if not page_title.strip():
        print("Error: Article name cannot be empty", file=sys.stderr)
        return 1
    
    tracker = WikipediaEditTracker()
    return tracker.run(page_title)


if __name__ == "__main__":
    sys.exit(main())
