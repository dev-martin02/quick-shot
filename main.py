import random
import io
from PIL import Image
from pygments import highlight
from pygments.lexers import guess_lexer_for_filename, TextLexer
from pygments.formatters import ImageFormatter
from pygments.styles import get_all_styles, get_style_by_name

styles = list(get_all_styles())
font_style = list()

def _hex_to_rgb(color):
    color = (color or "").strip().lstrip("#")
    if len(color) == 3:
        color = "".join(ch * 2 for ch in color)
    if len(color) != 6:
        return 39, 40, 34  # monokai-like fallback
    return tuple(int(color[i:i + 2], 16) for i in (0, 2, 4))


def _line_number_colors(style_name):
    """Use same background as the code area and a high-contrast number color."""
    try:
        style_cls = get_style_by_name(style_name)
        bg = style_cls.background_color or "#272822"
    except Exception:
        bg = "#272822"

    r, g, b = _hex_to_rgb(bg)
    luminance = (0.299 * r + 0.587 * g + 0.114 * b) / 255
    fg = "#111111" if luminance > 0.6 else "#f5f5f5"
    return bg, fg

def create_highlighted_image(code_text, file_name, style):
    """Create a syntax-highlighted image from code text."""
    try:
        lexer = guess_lexer_for_filename(file_name, code_text)
    except Exception:
        lexer = TextLexer()

    line_number_bg, line_number_fg = _line_number_colors(style)

    formatter = ImageFormatter(
        style=style,
        font_name="DejaVu Sans Mono",
        font_size=16,
        line_numbers=True,
        image_pad=10,
        line_number_separator=False,
        line_pad=4,
        line_number_bg=line_number_bg,
        line_number_fg=line_number_fg

    )

    image_bytes = highlight(code_text, lexer, formatter)
    return Image.open(io.BytesIO(image_bytes))


def parse_line_range(raw_range, total_lines):
    """Parse 'start-end' or single 'line' input."""
    raw_range = raw_range.strip()
    if "-" in raw_range:
        start_s, end_s = raw_range.split("-", 1)
        start, end = int(start_s), int(end_s)
    else:
        start = end = int(raw_range)

    start = max(1, start)
    end = min(total_lines, end)

    if start > end:
        raise ValueError("Start line must be <= end line.")
    return start, end


def main():
    file_name = input("Enter the name of the file to be screenshot: ").strip()
    code_lines = input("Enter line range (e.g. 5-12 or 8): ").strip()
    style = input(f"Enter the style to use (by default we us monokai, or say random to choose a random style): ").strip() or "monokai"
    if(style == "random"):
        style = random.choice(styles)
    with open(file_name, "r", encoding="utf-8") as f:
        all_lines = f.readlines()

    start, end = parse_line_range(code_lines, len(all_lines))
    selected_code = "".join(all_lines[start - 1:end])

    print(f"Capturing lines {start}-{end} from {file_name}")

    img = create_highlighted_image(selected_code, file_name, style)
    img.show()
    img.save("code_snippet.png")
    print("Saved to code_snippet.png")


if __name__ == "__main__":
    main()