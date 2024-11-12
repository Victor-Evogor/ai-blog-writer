import praw                                                                                                                
from typing import Dict                                                                                                    
import sys
from dotenv import load_dotenv
load_dotenv()                                                                                                                  

class RedditParser:                                                                                                        
    def __init__(self):                                                                                                    
        # Initialize Reddit API client (you'll need to set up your Reddit API credentials)                                 
        self.reddit = praw.Reddit(                                                                                         
            client_id="YOUR_CLIENT_ID",                                                                                    
            client_secret="YOUR_CLIENT_SECRET",                                                                            
            user_agent="your_user_agent"                                                                                   
        )                                                                                                                  
                                                                                                                            
    def parse(self, subreddit_or_url: str) -> Dict:                                                                        
        """Parse content from a subreddit or Reddit post URL."""                                                           
        try:                                                                                                               
            content = {                                                                                                    
                'title': '',                                                                                               
                'text': '',                                                                                                
                'comments': [],                                                                                            
                'images': []                                                                                               
            }                                                                                                              
                                                                                                                            
            # Check if it's a full post URL or just a subreddit name                                                       
            if 'reddit.com/r/' in subreddit_or_url and '/comments/' in subreddit_or_url:                                   
                # It's a specific post                                                                                     
                submission = self.reddit.submission(url=subreddit_or_url)                                                  
                self._process_submission(submission, content)                                                              
            else:                                                                                                          
                # It's a subreddit                                                                                         
                subreddit = self.reddit.subreddit(subreddit_or_url)                                                        
                for submission in subreddit.hot(limit=5):  # Get top 5 hot posts                                           
                    self._process_submission(submission, content)                                                          
                                                                                                                            
            return content                                                                                                 
                                                                                                                            
        except Exception as e:                                                                                             
            raise Exception(f"Failed to parse Reddit content: {str(e)}")                                                   
                                                                                                                            
    def _process_submission(self, submission, content: Dict):                                                              
        """Process a single Reddit submission."""                                                                          
        content['title'] += submission.title + '\n'                                                                        
        content['text'] += submission.selftext + '\n'                                                                      
                                                                                                                            
        # Get comments                                                                                                     
        submission.comments.replace_more(limit=0)                                                                          
        for comment in submission.comments.list()[:10]:  # Get top 10 comments                                             
            content['comments'].append(comment.body)                                                                       
                                                                                                                            
        # Get images if any                                                                                                
        if hasattr(submission, 'preview'):                                                                                 
            if 'images' in submission.preview:                                                                             
                for image in submission.preview['images']:                                                                 
                    content['images'].append({                                                                             
                        'url': image['source']['url'],                                                                     
                        'current_alt': ''                                                                                  
                    })