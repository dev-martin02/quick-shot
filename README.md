# Quick Shot

A simple command-line tool that converts code snippets into beautifully syntax-highlighted images.

## Description

Quick Shot captures specific lines of code from any file and generates a professional-looking image with syntax highlighting. Perfect for sharing code in presentations, documentation, or social media. The tool supports multiple syntax highlighting styles and automatically detects the programming language.

## Features

- 📸 Convert code snippets to images with syntax highlighting
- 🎨 Multiple color schemes (or choose a random style)
- 📝 Select specific line ranges from your files
- 🔤 Automatic language detection based on file extension
- 📊 Line numbers included in the generated image

## Installation

1. Clone or download this repository
2. Navigate to the project directory
3. Create a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```
4. Install the package:
   ```bash
   pip install -e .
   ```

## Usage

Run the main script:
```bash
python main.py
```

You'll be prompted to provide:
1. **File name**: Path to the file containing the code
2. **Line range**: Which lines to capture (e.g., `5-12` or just `8` for a single line)
3. **Style**: Syntax highlighting theme (default: `monokai`, or type `random` for a random style)

The tool will generate `code_snippet.png` in your working directory.

### Example

```
Enter the name of the file to be screenshot: main.py
Enter line range (e.g. 5-12 or 8): 10-25
Enter the style to use (by default we us monokai, or say random to choose a random style): monokai

Capturing lines 10-25 from main.py
Saved to code_snippet.png
```

## License

MIT License
