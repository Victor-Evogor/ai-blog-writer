from textual.app import App, ComposeResult
from textual.containers import Container
from textual.widgets import Header, Footer, Input, Button, Select
from textual.binding import Binding
from typing import List
import click
from trogon import tui
from cli import create_blog

class BlogGeneratorTUI(App):
    """A Textual app to generate AI blogs."""
    
    CSS = """
    Screen {
        align: center middle;
    }

    #main-container {
        width: 80%;
        height: auto;
        border: solid green;
        padding: 2;
    }

    Input {
        margin: 1;
    }

    Button {
        margin: 1;
    }

    Select {
        margin: 1;
    }
    """

    BINDINGS = [
        Binding("q", "quit", "Quit", show=True),
        Binding("g", "generate", "Generate Blog", show=True),
    ]

    def __init__(self):
        super().__init__()
        self.urls: List[str] = []
        self.subreddits: List[str] = []

    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        yield Header()
        with Container(id="main-container"):
            yield Input(placeholder="Enter blog title...", id="title-input")
            yield Input(placeholder="Enter URL (press Enter to add)...", id="url-input")
            yield Input(placeholder="Enter subreddit (press Enter to add)...", id="subreddit-input")
            yield Select(
                [(label, value) for label, value in [("OpenAI", "openai"), ("Claude", "claude")]],
                prompt="Select AI Model",
                id="model-select"
            )
            yield Button("Generate Blog", variant="primary", id="generate-btn")
        yield Footer()

    def on_input_submitted(self, event: Input.Submitted) -> None:
        """Handle input submission."""
        if event.input.id == "url-input" and event.value:
            self.urls.append(event.value)
            event.input.value = ""
            self.notify(f"Added URL: {event.value}")
        elif event.input.id == "subreddit-input" and event.value:
            self.subreddits.append(event.value)
            event.input.value = ""
            self.notify(f"Added subreddit: {event.value}")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button presses."""
        if event.button.id == "generate-btn":
            self.action_generate()

    def action_generate(self) -> None:
        """Generate the blog post."""
        title = self.query_one("#title-input").value
        model = self.query_one("#model-select").value
        
        if not title:
            self.notify("Please enter a title", severity="error")
            return
        
        if not self.urls and not self.subreddits:
            self.notify("Please add at least one URL or subreddit", severity="error")
            return
            
        try:
            # Convert the parameters and call the CLI function
            urls_tuple = tuple(self.urls)
            subreddits_tuple = tuple(self.subreddits)
            
            # Call the CLI function
            create_blog.callback(
                urls=urls_tuple,
                subreddits=subreddits_tuple,
                title=title,
                ai_model=model
            )
            
            self.notify("Blog generated successfully!", severity="success")
        except Exception as e:
            self.notify(f"Error generating blog: {str(e)}", severity="error")

def run_tui():
    """Run the TUI application."""
    app = BlogGeneratorTUI()
    app.run()

if __name__ == "__main__":
    run_tui()
