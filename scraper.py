import requests                                                                                                            
from bs4 import BeautifulSoup                                                                                              
from typing import Dict                                                                                                    
                                                                                                                            
class WebScraper:                                                                                                          
    def scrape(self, url: str) -> Dict:                                                                                    
        """Scrape content from a website URL."""                                                                           
        try:                                                                                                               
            response = requests.get(url)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, 'html.parser')                                                             

            # Extract main content (customize based on typical website structure)                                          
            content = {                                                                                                    
                'title': soup.title.string if soup.title else '',                                                          
                'text': '',                                                                                                
                'images': []                                                                                               
            }                                                                                                              

            # Get main text content                                                                                        
            main_content = soup.find('main') or soup.find('article') or soup.body                                          
            if main_content:                                                                                               
                content['text'] = ' '.join([p.get_text().strip() for p in main_content.find_all('p')])                     
                                                                                                                            
            # Get images with their current alt text                                                                       
            for img in soup.find_all('img'):                                                                               
                if img.get('src'):                                                                                         
                    content['images'].append({                                                                             
                        'url': img['src'],                                                                                 
                        'current_alt': img.get('alt', ''),                                                                 
                    })                                                                                                     
                                                                                                                            
            return content                                                                                                 
                                                                                                                            
        except Exception as e:                                                                                             
            raise Exception(f"Failed to scrape {url}: {str(e)}")