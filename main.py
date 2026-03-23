import random
import io
import sys
from PIL import Image
from pygments import highlight
from pygments.lexers import guess_lexer_for_filename, TextLexer
from pygments.formatters import ImageFormatter
from pygments.styles import get_all_styles
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.prompt import Prompt

from config import Image_Config
from util.util import get_line_limits

console = Console()
styles = list(get_all_styles())


def create_highlighted_image(code_text, file_name, style):
    """Create a syntax-highlighted image from code text."""
    try:
        lexer = guess_lexer_for_filename(file_name, code_text)
    except Exception:
        lexer = TextLexer()

    img_config = Image_Config(style=style, line_numbers=True).__dict__
    formatter = ImageFormatter(**img_config) # We used ** to unpack the content

    image_bytes = highlight(code_text, lexer, formatter)
    return Image.open(io.BytesIO(image_bytes))


def show_styles():
    """Display available styles."""
    table = Table(title="Available Pygments Styles")
    table.add_column("Style", style="cyan")

    for s in styles:
        table.add_row(s)

    console.print(table)


def main():
    console.print(Panel("Code Screenshot Generator", style="bold cyan"))
    
    file_name = Prompt.ask("File to screenshot")

    try:
        with open(file_name, "r", encoding="utf-8") as f:
            all_lines = f.readlines()
    except FileNotFoundError:
        console.print(f"[red]File not found:[/red] {file_name}")
        return

    console.print(f"[green]Loaded {len(all_lines)} lines[/green]")

    lines = Prompt.ask(
        "Line range",
        default="1"
    )

    style = Prompt.ask(
        "Style (monokai, random, or 'list')",
        default="monokai"
    )

    if style == "list":
        show_styles()
        style = Prompt.ask("Choose a style", default="monokai")

    if style == "random":
        style = random.choice(styles)
        console.print(f"[yellow]Random style selected:[/yellow] {style}")

    start, end = get_line_limits(lines, len(all_lines))
    selected_code = "".join(all_lines[start - 1:end])

    console.print(
        f"[cyan]Capturing lines {start}-{end} from {file_name}[/cyan]"
    )

    img = create_highlighted_image(selected_code, file_name, style)

    output = "code_snippet.png"
    img.save(output)

    console.print(f"[bold green]Saved:[/bold green] {output}")
    img.show()


class ScreenshotFileHandler:
    def __init__(self, file_path):
        self.file_path = file_path
        self.content = self.get_file_content()
        self.lines = len(self.content)

    def get_file_content(self):
        try:
            with open(self.file_path, "r", encoding="utf-8") as f:
                return f.readlines()
        except FileNotFoundError:
            console.print(f"[red]File not found:[/red] {self.file_path}")
            return []

if __name__ == "__main__":
    main()
    arguments = sys.argv[1:] 
    
    file_path = arguments[0]
    file_info = ScreenshotFileHandler(file_path)
    print(file_info.lines)
    lines = arguments[1:]
    print(file_path)
    print(lines)


