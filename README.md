![AI Blog Cli](https://res.cloudinary.com/djaqusrpx/image/upload/v1731410602/Screenshot_from_2024-11-12_12-14-41_h5mzuc.png)

# AI Blog Writer

A powerful command-line tool that creates AI-generated blog posts from various sources including websites and Reddit content. The tool scrapes content, processes images with AI-generated alt text, and uses either OpenAI or Claude to generate well-structured blog posts.

## Features

- Scrape content from multiple websites
- Parse Reddit posts and subreddits
- Generate AI-powered alt text for images
- Choose between OpenAI or Claude for blog generation
- Command-line interface with Click
- Support for multiple URLs and subreddits in a single command

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd ai-blog-generator
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables in `.env`:
```
OPENAI_API_KEY=your_openai_api_key_here
CLAUDE_API_KEY=your_claude_api_key_here
```

4. Configure Reddit API credentials in `reddit_parser.py`

## Usage

### Command Line Interface (CLI)

Basic usage with website URLs:
```bash
python cli.py -u https://example.com -u https://example2.com -m openai
```

Using Reddit content:
```bash
python cli.py -s programming -s "https://reddit.com/r/programming/comments/example"
```

Combining both sources with Claude AI:
```bash
python cli.py -u https://example.com -s programming -m claude
```

### Text User Interface (TUI)

Launch the interactive TUI:
```bash
python tui.py
```

Or use Trogon to automatically generate a TUI from the CLI:
```bash
python cli.py --tui
```

The TUI provides an interactive interface where you can:
- Enter a blog title
- Add multiple URLs and subreddits
- Select the AI model
- Generate the blog with a single click

### CLI Options

- `-u, --urls`: Website URLs to scrape (can be used multiple times)
- `-s, --subreddits`: Subreddit names or post URLs (can be used multiple times)
- `-m, --ai-model`: Choose AI model ('openai' or 'claude', default: 'openai')

## Requirements

- Python 3.7+
- Beautiful Soup 4
- Click
- PRAW (Python Reddit API Wrapper)
- OpenAI API key
- Claude API key
- Reddit API credentials

## Project Structure

- `cli.py`: Main CLI interface
- `scraper.py`: Website content scraper
- `reddit_parser.py`: Reddit content parser
- `blog_generator.py`: AI blog generation logic
- `image_processor.py`: Image processing and alt text generation

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Author

Victor Evogor
- Twitter: [@victorevogor](https://x.com/victorevogor)
