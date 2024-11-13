from pydantic import BaseModel
from typing import List

class BlogRequest(BaseModel):
    urls: List[str] = []
    subreddits: List[str] = []
    ai_model: str = "openai"
    title: str

class BlogResponse(BaseModel):
    content: str
    filename: str