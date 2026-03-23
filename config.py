# File Handler for Screenshot Content
from util.util import line_number_colors


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
            error = f"[red]File not found:[/red] {self.file_path}"
            return error


# Image Configurations
class Image_Config:
    def __init__(self, style="monokai", line_numbers=True):
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