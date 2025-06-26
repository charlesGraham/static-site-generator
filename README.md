# Static Site Generator

This project is a Python-based static site generator (SSG). It converts Markdown content into static HTML pages using customizable templates and styles. The tool is designed for simplicity and flexibility, making it easy to build and deploy fast, secure, and maintainable static websites.

## Features

- Converts Markdown files to HTML
- Uses customizable HTML templates
- Supports static assets (CSS, images, etc.)
- Simple command-line interface
- Easily extensible for custom needs

## Project Structure

- `src/` — Source code for the generator
- `content/` — Markdown files to be converted
- `public/` — Output directory for generated HTML and static assets
- `static/` — Static files (CSS, images) to be copied to `public/`
- `template.html` — Main HTML template

## Usage

1. Place your Markdown files in the `content/` directory.
2. Run the generator:

   ```bash
   bash main.sh
   ```

   or

   ```bash
   python3 src/main.py
   ```

3. Find the generated site in the `public/` directory.

## Requirements

- Python 3.8+

## License

MIT License
