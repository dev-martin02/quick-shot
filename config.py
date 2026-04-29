# File Handler for Screenshot Content
import os
from util.util import line_number_colors
import io
from PIL import Image
from pygments import highlight
from pygments.lexers import guess_lexer_for_filename
from pygments.formatters import ImageFormatter
from rich.console import Console
import json
# Image Configurations 
class Image_Config:
    def __init__(self, config_path="config.json"):
        if config_path and os.path.exists(config_path):
            self.load_from_file(config_path)
        else:
            self.font_name = "DejaVu Sans Mono"
            self.font_size = 16
            self.image_pad = 10
            self.line_pad = 4
            self.style = 'monakai'
            self.line_numbers = False
            self.line_number_bg = None
            self.line_number_fg = None
        
    def update_line_number_colors(self, bg, fg):
        if self.line_numbers is True:
            bg, fg = line_number_colors(self.style)
            self.line_number_bg = bg
            self.line_number_fg = fg

    def load_from_file(self, config_path):
        with open(config_path, 'r') as f:
            config = json.load(f)['image_config']
            for key, value in config.items():
                setattr(self, key, value)
    
    def save_to_file(self, config_path):
        config = {
            'image_config': self.__dict__
        }
        with open(config_path, 'w') as f:
            json.dump(config, f, indent=2)
console = Console()

class ScreenshotFileHandler:
    def __init__(self, file_path, config_path="config.json"):
        self.file_path = file_path
        self.content = self.get_file_content()
        self.lines = len(self.content)
        self.img_config = Image_Config(config_path)

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
        img_config = self.img_config.__dict__
        formatter = ImageFormatter(**img_config) # We used ** to unpack the content

        image_bytes = highlight(code_text, lexer, formatter)
        return Image.open(io.BytesIO(image_bytes))