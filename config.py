# File Handler for Screenshot Content
from util.util import line_number_colors
import io
from PIL import Image
from pygments import highlight
from pygments.lexers import guess_lexer_for_filename
from pygments.formatters import ImageFormatter
from rich.console import Console

# Image Configurations 
class Image_Config:
    def __init__(self, style="dracula", line_numbers=True):
        self.font_name = "DejaVu Sans Mono"
        self.font_size = 16
        self.image_pad = 10
        self.line_pad = 4
        self.style = style
        self.line_numbers = line_numbers
        self.line_number_bg = None
        self.line_number_fg = None
        
    def update_line_number_colors(self, bg, fg):
        if self.line_numbers is True:
            bg, fg = line_number_colors(self.style)
            self.line_number_bg = bg
            self.line_number_fg = fg

console = Console()

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
        
    def return_content_lines(self, start, end):
        code_text = "".join(self.content[start - 1:end])
        try:
            lexer = guess_lexer_for_filename(self.file_path, code_text)
        except Exception as e:
            console.print(f"[red]Error retrieving lines:[/red] {e}")
            return ""
        img_config = Image_Config(style="default").__dict__
        formatter = ImageFormatter(**img_config) # We used ** to unpack the content

        image_bytes = highlight(code_text, lexer, formatter)
        return Image.open(io.BytesIO(image_bytes))