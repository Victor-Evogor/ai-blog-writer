from typing import Dict, List
from openai import OpenAI
from anthropic import Anthropic                                                                                            
import os                                                                                                                  

class OpenAIBlogGenerator:                                                                                                 
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    def generate(self, content: List[Dict]) -> str:                                                                        
        """Generate blog content using OpenAI."""                                                                          
        try:
            # Prepare the content for the prompt                                                                           
            combined_content = self._prepare_content(content)                                                              
            
            # Generate blog using OpenAI                                                                                   
            response = self.client.chat.completions.create(                                                                       
                model="gpt-4",                                                                                             
                messages=[                                                                                                 
                    {"role": "system", "content": "You are a professional blog writer. Create a well-structured, engaging  blog post from the provided content."},                                                                                    
                    {"role": "user", "content": f"Create a blog post from this content: {combined_content}\n\nInclude images with alt text accurately describing what the image is all about. The blog should be formatted in markdown syntax"}
                ]                                                                                                          
            )                                                                                                              

            return response.choices[0].message.content                                                                     

        except Exception as e:                                                                                             
            raise Exception(f"Failed to generate blog with OpenAI: {str(e)}")                                              

    def _prepare_content(self, content: List[Dict]) -> str:                                                                
        """Prepare content for the AI prompt."""                                                                           
        combined = ""                                                                                                      
        for item in content:                                                                                               
            combined += f"Title: {item.get('title', '')}\n"                                                                
            combined += f"Content: {item.get('text', '')}\n"                                                               
            if 'comments' in item:                                                                                         
                combined += f"Comments: {' '.join(item['comments'])}\n"                                                    
        return combined                                                                                                    


class ClaudeBlogGenerator:                                                                                                 
    def __init__(self):                                                                                                    
        self.client = Anthropic(api_key=os.getenv('CLAUDE_API_KEY'))                                                       
                                                                                                                            
    def generate(self, content: List[Dict]) -> str:                                                                        
        """Generate blog content using Claude."""                                                                          
        try:                                                                                                               
            # Prepare the content for the prompt                                                                           
            combined_content = self._prepare_content(content)                                                              
                                                                                                                            
            # Generate blog using Claude                                                                                   
            response = self.client.messages.create(                                                                        
                model="claude-2",                                                                                          
                max_tokens=1000,                                                                                           
                messages=[{                                                                                                
                    "role": "user",                                                                                        
                    "content": f"Create a well-structured, engaging blog post from this content: {combined_content}\n\nInclude images with alt text accurately describing what the image is all about"       
                }]                                                                                                         
            )                                                                                                              
                                                                                                                            
            return response.content[0].text                                                                                
                                                                                                                            
        except Exception as e:                                                                                             
            raise Exception(f"Failed to generate blog with Claude: {str(e)}")                                              
                                                                                                                            
    def _prepare_content(self, content: List[Dict]) -> str:                                                                
        """Prepare content for the AI prompt."""                                                                           
        combined = ""                                                                                                      
        for item in content:                                                                                               
            combined += f"Title: {item.get('title', '')}\n"                                                                
            combined += f"Content: {item.get('text', '')}\n"                                                               
            if 'comments' in item:                                                                                         
                combined += f"Comments: {' '.join(item['comments'])}\n"                                                    
        return combined