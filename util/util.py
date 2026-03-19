from pygments.styles import get_style_by_name

def hex_to_rgb(color):
    # Remove whitespace, and the # of the value
    color = (color or "").lstrip("#")

    if len(color) == 3:
        color = "".join(ch * 2 for ch in color)

    if len(color) != 6:
        return 39, 40, 34  # monokai-like fallback
    # Convert a hex color string (e.g., "#ff8800" or "#f80") into an (R, G, B) tuple of integers.
    return tuple(int(color[i:i + 2], 16) for i in (0, 2, 4)) 

def line_number_colors(style_name):
    """Use same background as the code area and a high-contrast number color."""
    try:
        theme_style = get_style_by_name(style_name)
        bg = theme_style.background_color or "#272822"
    except Exception:
        bg = "#272822"

    r, g, b = hex_to_rgb(bg)
    luminance = (0.299 * r + 0.587 * g + 0.114 * b) / 255
    fg = "#111111" if luminance > 0.6 else "#f5f5f5"
    return bg, fg

def parse_line_range(line_selection, total_lines):
    """Parse 'start-end' or single 'line' input."""
    line_selection = line_selection.strip()
    if "-" in line_selection:
        start_line, end_line = line_selection.split("-", 1)
        start, end = int(start_line), int(end_line)
    else:
        start = int(line_selection)
        end = int(total_lines)

    if start > end or end > total_lines:
        raise ValueError("Start line must be less than or equal to end line.")

    return start, end
