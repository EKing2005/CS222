import unittest
from unittest.mock import Mock, patch, MagicMock
import sys
import json
from io import StringIO
import requests

try:
    from wiki_tracker import WikipediaEditTracker, main
except ImportError:
    print("Error: Please ensure wiki_tracker.py is in the same directory")
    sys.exit(1)


class TestWikipediaEditTracker(unittest.TestCase):
    """Test cases for WikipediaEditTracker class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.tracker = WikipediaEditTracker()
    
    def test_init(self):
        """Test initialization of WikipediaEditTracker."""
        self.assertIsInstance(self.tracker.session, requests.Session)
        self.assertIn('User-Agent', self.tracker.session.headers)
    
    def test_format_timestamp(self):
        """Test timestamp formatting."""
        # Test valid timestamp
        timestamp = "2023-09-23T17:28:39Z"
        result = self.tracker.format_timestamp(timestamp)
        self.assertEqual(result, "2023-09-23 17:28:39")
        
        # Test invalid timestamp (should return original)
        invalid_timestamp = "invalid-timestamp"
        result = self.tracker.format_timestamp(invalid_timestamp)
        self.assertEqual(result, invalid_timestamp)
    
    @patch('requests.Session.get')
    def test_get_page_revisions_success(self, mock_get):
        """Test successful page revision retrieval."""
        # Mock response data
        mock_response_data = {
            "query": {
                "pages": {
                    "12345": {
                        "pageid": 12345,
                        "title": "Test Page",
                        "revisions": [
                            {
                                "user": "TestUser1",
                                "timestamp": "2023-09-23T17:28:39Z"
                            },
                            {
                                "user": "TestUser2",
                                "timestamp": "2023-09-22T15:30:00Z"
                            }
                        ]
                    }
                }
            }
        }
        
        mock_response = Mock()
        mock_response.json.return_value = mock_response_data
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        revisions, redirect_title = self.tracker.get_page_revisions("Test Page")
        
        self.assertEqual(len(revisions), 2)
        self.assertEqual(revisions[0]['user'], 'TestUser1')
        self.assertIsNone(redirect_title)
    
    @patch('requests.Session.get')
    def test_get_page_revisions_with_redirect(self, mock_get):
        """Test page revision retrieval with redirect."""
        mock_response_data = {
            "query": {
                "redirects": [
                    {"from": "Old Name", "to": "New Name"}
                ],
                "pages": {
                    "12345": {
                        "pageid": 12345,
                        "title": "New Name",
                        "revisions": [
                            {
                                "user": "TestUser1",
                                "timestamp": "2023-09-23T17:28:39Z"
                            }
                        ]
                    }
                }
            }
        }
        
        mock_response = Mock()
        mock_response.json.return_value = mock_response_data
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        revisions, redirect_title = self.tracker.get_page_revisions("Old Name")
        
        self.assertEqual(len(revisions), 1)
        self.assertEqual(redirect_title, "New Name")
    
    @patch('requests.Session.get')
    def test_get_page_revisions_page_not_found(self, mock_get):
        """Test handling of non-existent pages."""
        mock_response_data = {
            "query": {
                "pages": {
                    "-1": {
                        "ns": 0,
                        "title": "NonExistentPage",
                        "missing": ""
                    }
                }
            }
        }
        
        mock_response = Mock()
        mock_response.json.return_value = mock_response_data
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        with self.assertRaises(ValueError) as context:
            self.tracker.get_page_revisions("NonExistentPage")
        
        self.assertIn("Page not found", str(context.exception))
    
    @patch('requests.Session.get')
    def test_get_page_revisions_network_error(self, mock_get):
        """Test handling of network errors."""
        mock_get.side_effect = requests.RequestException("Connection failed")
        
        with self.assertRaises(requests.RequestException) as context:
            self.tracker.get_page_revisions("Test Page")
        
        self.assertIn("Network error", str(context.exception))
    
    @patch('requests.Session.get')
    def test_get_page_revisions_api_error(self, mock_get):
        """Test handling of API errors."""
        mock_response_data = {
            "error": {
                "code": "nosuchpage",
                "info": "The page you specified doesn't exist."
            }
        }
        
        mock_response = Mock()
        mock_response.json.return_value = mock_response_data
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        with self.assertRaises(ValueError) as context:
            self.tracker.get_page_revisions("Test Page")
        
        self.assertIn("API error", str(context.exception))
    
    @patch('requests.Session.get')
    def test_run_success(self, mock_get):
        """Test successful run method."""
        mock_response_data = {
            "query": {
                "pages": {
                    "12345": {
                        "pageid": 12345,
                        "title": "Test Page",
                        "revisions": [
                            {
                                "user": "TestUser1",
                                "timestamp": "2023-09-23T17:28:39Z"
                            }
                        ]
                    }
                }
            }
        }
        
        mock_response = Mock()
        mock_response.json.return_value = mock_response_data
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        # Capture stdout
        old_stdout = sys.stdout
        sys.stdout = captured_output = StringIO()
        
        try:
            result = self.tracker.run("Test Page")
            output = captured_output.getvalue()
            
            self.assertEqual(result, 0)
            self.assertIn("TestUser1", output)
            self.assertIn("2023-09-23 17:28:39", output)
        finally:
            sys.stdout = old_stdout
    
    @patch('requests.Session.get')
    def test_run_with_redirect(self, mock_get):
        """Test run method with redirect."""
        mock_response_data = {
            "query": {
                "redirects": [
                    {"from": "Old Name", "to": "New Name"}
                ],
                "pages": {
                    "12345": {
                        "pageid": 12345,
                        "title": "New Name",
                        "revisions": [
                            {
                                "user": "TestUser1",
                                "timestamp": "2023-09-23T17:28:39Z"
                            }
                        ]
                    }
                }
            }
        }
        
        mock_response = Mock()
        mock_response.json.return_value = mock_response_data
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        # Capture stdout
        old_stdout = sys.stdout
        sys.stdout = captured_output = StringIO()
        
        try:
            result = self.tracker.run("Old Name")
            output = captured_output.getvalue()
            
            self.assertEqual(result, 0)
            self.assertIn("Redirected to New Name", output)
        finally:
            sys.stdout = old_stdout
    
    @patch('requests.Session.get')
    def test_run_page_not_found(self, mock_get):
        """Test run method with non-existent page."""
        mock_response_data = {
            "query": {
                "pages": {
                    "-1": {
                        "ns": 0,
                        "title": "NonExistentPage",
                        "missing": ""
                    }
                }
            }
        }
        
        mock_response = Mock()
        mock_response.json.return_value = mock_response_data
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        result = self.tracker.run("NonExistentPage")
        self.assertEqual(result, 2)
    
    @patch('requests.Session.get')
    def test_run_network_error(self, mock_get):
        """Test run method with network error."""
        mock_get.side_effect = requests.RequestException("Connection failed")
        
        result = self.tracker.run("Test Page")
        self.assertEqual(result, 3)


class TestMainFunction(unittest.TestCase):
    """Test cases for main function."""
    
    @patch('sys.argv', ['wiki_tracker.py'])
    def test_main_no_arguments(self):
        """Test main function with no arguments."""
        result = main()
        self.assertEqual(result, 1)
    
    @patch('sys.argv', ['wiki_tracker.py', 'Test Page'])
    @patch('wiki_tracker.WikipediaEditTracker.run')
    def test_main_with_arguments(self, mock_run):
        """Test main function with proper arguments."""
        mock_run.return_value = 0
        
        result = main()
        
        self.assertEqual(result, 0)
        mock_run.assert_called_once_with('Test Page')
    
    @patch('sys.argv', ['wiki_tracker.py', ''])
    def test_main_empty_argument(self):
        """Test main function with empty argument."""
        result = main()
        self.assertEqual(result, 1)


if __name__ == '__main__':
    # Run the tests
    unittest.main(verbosity=2)