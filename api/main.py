from fastapi import FastAPI, HTTPException
from .models import BlogRequest, BlogResponse
from datetime import datetime
from pathlib import Path
import sys
import os

# Add parent directory to path to import blog generation modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scraper import WebScraper
from reddit_parser import RedditParser
from blog_generator import OpenAIBlogGenerator, ClaudeBlogGenerator
from image_processor import ImageProcessor

app = FastAPI(
    title="AI Blog Writer API",
    description="API for generating AI-powered blog posts from web content and Reddit discussions",
    version="1.0.0"
)

@app.post("/generate", response_model=BlogResponse)
async def generate_blog(request: BlogRequest):
    """Generate a blog post from provided URLs and Reddit content."""
    
    # Initialize components
    web_scraper = WebScraper()
    reddit_parser = RedditParser()
    image_processor = ImageProcessor()

    content = []

    # Process website URLs
    if request.urls:
        for url in request.urls:
            try:
                scraped_content = web_scraper.scrape(url)
                content.append(scraped_content)
            except Exception as e:
                raise HTTPException(status_code=400, detail=f"Error scraping {url}: {str(e)}")

    # Process Reddit content
    if request.subreddits:
        for subreddit in request.subreddits:
            try:
                reddit_content = reddit_parser.parse(subreddit)
                content.append(reddit_content)
            except Exception as e:
                raise HTTPException(status_code=400, detail=f"Error parsing Reddit content {subreddit}: {str(e)}")

    if not content:
        raise HTTPException(status_code=400, detail="No content was successfully scraped or parsed")

    # Process images and generate alt text
    processed_content = image_processor.process_images(content)

    # Generate blog using selected AI model
    try:
        generator = OpenAIBlogGenerator() if request.ai_model == 'openai' else ClaudeBlogGenerator()
        blog_content = generator.generate(processed_content)
        
        # Create blogs directory if it doesn't exist
        blogs_dir = Path("blogs")
        blogs_dir.mkdir(exist_ok=True)
        
        # Generate filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"blog_{timestamp}.md"
        filepath = blogs_dir / filename
        
        # Save blog content to file
        with open(filepath, "w") as f:
            f.write(blog_content)
            
        return BlogResponse(
            content=blog_content,
            filename=str(filepath)
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating blog: {str(e)}")

@app.get("/")
async def root():
    """Root endpoint returning API information."""
    return {
        "name": "AI Blog Writer API",
        "version": "1.0.0",
        "description": "Generate AI-powered blog posts from web content and Reddit discussions"
    }