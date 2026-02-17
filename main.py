import subprocess
from PIL import Image, ImageDraw, ImageFont


def create_screenshot_image(lines, background_color=(40, 44, 52), text_color=(171, 178, 191)):
    """Create a styled code snippet image."""
    
    # Font settings
    font_size = 16
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf", font_size)
    except OSError:
        font = ImageFont.load_default()
    
    # Layout settings
    padding = 40
    line_height = font_size + 8
    
    # Calculate image dimensions based on content
    max_line_length = max(len(line) for line in lines) if lines else 20
    char_width = font_size * 0.6  # Approximate width per character
    
    width = int(max_line_length * char_width) + (padding * 2)
    height = len(lines) * line_height + (padding * 2)
    
    # Create image
    img = Image.new('RGB', (width, height), color=background_color)
    draw = ImageDraw.Draw(img)
    
    # Draw each line of code
    for i, line in enumerate(lines):
        y = padding + (i * line_height)
        draw.text((padding, y), line.rstrip(), fill=text_color, font=font)
    
    return img

def main():
    file_name = input("Enter the name of the file to be screenshot: ")
    code_lines = input("Enter the code lines to be screenshot: ")

    terminal_output = subprocess.run(["cat", file_name], capture_output=True, text=True)    

    # the end of a sentence would have \n, by spliting by it you are getting the entire sentence or line
    if "-" in code_lines:
        start = int(code_lines.split("-")[0])
        end = int(code_lines.split("-")[1])

    # Build list of lines with line numbers
    lines = []
    for i, words in enumerate(terminal_output.stdout.splitlines()):
        if i + 1 >= start and i + 1 <= end:
            lines.append(f"{i+1}  {words}")

    img = create_screenshot_image(lines)
    img.show()
    img.save("code_snippet.png")
    print("Saved to code_snippet.png")
if __name__ == "__main__":
    main()
