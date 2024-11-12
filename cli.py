import click                                                                                                                                                                                                                              
from dotenv import load_dotenv
from trogon import tui
from scraper import WebScraper
from reddit_parser import RedditParser
from blog_generator import OpenAIBlogGenerator, ClaudeBlogGenerator
from image_processor import ImageProcessor


load_dotenv()

@tui()
@click.command()                                                                                                           
@click.option('--urls', '-u', multiple=True, help='List of website URLs to scrape')                                        
@click.option('--subreddits', '-s', multiple=True, help='List of subreddits or Reddit post URLs')                          
@click.option('--ai-model', '-m', type=click.Choice(['openai', 'claude']), default='openai', help='Choose AI model for blog generation')                                                                  
def create_blog(urls, subreddits, ai_model):                                                                               
    """Create a blog from website URLs and Reddit content."""                                                              

    # Initialize components                                                                                                
    web_scraper = WebScraper()                                                                                             
    reddit_parser = RedditParser()                                                                                         
    image_processor = ImageProcessor()                                                                                     

    content = []                                                                                                           

    # Process website URLs
    if urls:
        for url in urls:                                                                                                   
            try:                                                                                                           
                scraped_content = web_scraper.scrape(url)                                                                  
                content.append(scraped_content)                                                                            
            except Exception as e:                                                                                         
                click.echo(f"Error scraping {url}: {str(e)}")                                                              
                                                                                                                            
    # Process Reddit content                                                                                               
    if subreddits:                                                                                                         
        for subreddit in subreddits:                                                                                       
            try:                                                                                                           
                reddit_content = reddit_parser.parse(subreddit)                                                            
                content.append(reddit_content)                                                                             
            except Exception as e:                                                                                         
                click.echo(f"Error parsing Reddit content {subreddit}: {str(e)}")                                          
                                                                                                                            
    if not content:                                                                                                        
        click.echo("No content was successfully scraped or parsed.")                                                       
        return                                                                                                             

    # Process images and generate alt text                                                                                 
    processed_content = image_processor.process_images(content)                                                            

    # Generate blog using selected AI model                                                                                
    if ai_model == 'openai':                                                                                               
        generator = OpenAIBlogGenerator()                                                                                  
    else:                                                                                                                  
        generator = ClaudeBlogGenerator()                                                                                  

    try:                                                                                                                   
        blog_content = generator.generate(processed_content)                                                               
        click.echo("Blog generated successfully!")                                                                         
        click.echo("\nBlog Content:")
        click.echo(blog_content)
    except Exception as e:                                                                                                 
        click.echo(f"Error generating blog: {str(e)}")                                                                     
                                                                                                                            
if __name__ == '__main__':                                                                                                 
    create_blog()
