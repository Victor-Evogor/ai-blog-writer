from fastapi import FastAPI, HTTPException, status
from .models import BlogRequest, BlogResponse
from typing import List
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
    description="""
    AI Blog Writer API allows you to generate AI-powered blog posts by combining content from:
    * Web pages (via URL scraping)
    * Reddit discussions (via subreddit or post URLs)
    
    The API supports two AI models:
    * OpenAI GPT
    * Anthropic Claude
    
    Features:
    * Web content scraping
    * Reddit content parsing
    * Image processing with alt text generation
    * Markdown blog post generation
    * Automatic blog file saving
    """,
    version="1.0.0",
    contact={
        "name": "AI Blog Writer Team",
        "url": "https://github.com/yourusername/ai-blog-writer",
    },
    license_info={
        "name": "MIT License",
    }
)

@app.post(
    "/generate",
    response_model=BlogResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Generate a blog post",
    response_description="Generated blog post content and saved file location"
)
async def generate_blog(request: BlogRequest):
    """
    Generate an AI-written blog post by combining content from multiple sources.
    
    ## Request Body
    - **urls**: Optional list of web URLs to scrape for content
    - **subreddits**: Optional list of subreddit names or Reddit post URLs
    - **ai_model**: AI model to use ('openai' or 'claude')
    
    ## Returns
    - **content**: The generated blog post content in Markdown format
    - **filename**: Path to the saved blog post file
    
    ## Raises
    - **400**: If no content could be scraped/parsed or invalid URLs provided
    - **500**: If blog generation fails
    
    ## Example
    ```json
    {
        "urls": ["https://example.com/article"],
        "subreddits": ["technology"],
        "ai_model": "openai"
    }
    ```
    """
    
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

@app.get(
    "/",
    summary="API Information",
    response_description="Basic API details and version"
)
async def root():
    """
    Get basic information about the AI Blog Writer API.
    
    Returns basic metadata including:
    - API name
    - Current version
    - Brief description
    """
    return {
        "name": "AI Blog Writer API",
        "version": "1.0.0",
        "description": "Generate AI-powered blog posts from web content and Reddit discussions"
    }
