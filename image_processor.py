from typing import Dict, List
from openai import OpenAI
from dotenv import load_dotenv
import os                                                                                                                  
load_dotenv()

class ImageProcessor:                                                                                                      
    def __init__(self):                                                                                                    
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    def process_images(self, content: List[Dict]) -> List[Dict]:                                                           
        """Process images and generate descriptive alt text."""                                                            
        for item in content:                                                                                               
            if 'images' in item:                                                                                           
                for image in item['images']:                                                                               
                    try:                                                                                                   
                        # Generate alt text using OpenAI's vision model
                        # print(image["url"], image["current_alt"])
                        # alt_text = self._generate_alt_text(image['url'])                                                   
                        # image['generated_alt'] = alt_text                 
                        pass                                                 
                    except Exception as e:                                                                                 
                        print(f"Failed to generate alt text for image: {str(e)}")                                          
                        image['generated_alt'] = image.get('current_alt', '')                                              
                                                                                                                            
        return content                                                                                                     
                                                                                                                            
    def _generate_alt_text(self, image_url: str) -> str:                                                                   
        """Generate alt text for an image using OpenAI's vision model."""                                                  
        try:                                                                                                               
            response = self.client.chat.completions.create(                                                                       
                model="gpt-4",                                                                              
                messages=[                                                                                                 
                    {                                                                                                      
                        "role": "user",                                                                                    
                        "content": [                                                                                       
                            {"type": "text", "text": "Generate a concise, descriptive alt text for this image."},          
                            {"type": "image_url", "image_url": image_url}                                                  
                        ],                                                                                                 
                    }                                                                                                      
                ]                                                                                                          
            )                                                                                                              
            return response.choices[0].message.content                                                                     
        except Exception as e:                                                                                             
            raise Exception(f"Failed to generate alt text: {str(e)}")                                                      