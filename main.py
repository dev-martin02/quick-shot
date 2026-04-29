import sys
import json
import os
from rich.console import Console

from config import Image_Config, ScreenshotFileHandler
from util.util import get_line_limits

console = Console()

def ensure_config_file(config_path="config.json"):
    """Create config file if it doesn't exist"""
    if not os.path.exists(config_path):
        default_config = Image_Config().save_to_file(config_path)
        console.print(f"[yellow]Config file not found. Creating default config at {config_path}[/yellow]")

def main():
    ensure_config_file()
    arguments = sys.argv[1:] 
    if not len(arguments):
        console.print("[red]Please provide a file path as the first argument.[/red]")
        sys.exit(1)

    file_path = arguments[0]
    file_info = ScreenshotFileHandler(file_path)
    lines = ""

    if len(file_info.content) == 0:
        console.print(f"[red]No content to process or file not found.[/red] {file_info.file_path}")
        sys.exit(1)

    elif(len(arguments) == 1):
        console.print(f"[green] No line range specified, capturing all lines! [/green]")
        lines = f"1-{file_info.lines}"

    elif len(arguments) > 2:
        console.print("[red]Too many arguments provided. Please follow the format: python main.py <file_path> 'start-end'[/red]")
        sys.exit(1)

    else: 
        lines = arguments[1]

    start, end = get_line_limits(lines, file_info.lines)

    content = file_info.return_content_lines(start, end)


    console.print(
        f"[cyan]Capturing lines {start}-{end} from {file_path}[/cyan]"
    )
    screenshot_file_name = "code_snippet.png"
    content.save(screenshot_file_name)
    console.print(f"[bold green]Saved:[/bold green] {screenshot_file_name}")

    content.show()


if __name__ == "__main__":
    main()
