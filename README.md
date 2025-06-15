# MAV-LandingPage

This repository contains HTML landing pages and a Python script to generate an `index.html` listing all HTML files in the project. This is useful for hosting on GitHub Pages.

## Usage

1. **Generate the HTML index:**
   
   Run the following command in your project root:
   
   ```powershell
   python generate_index.py
   ```
   
   This will create an `index.html` file listing all HTML files in the repository.

2. **Host on GitHub Pages:**
   - Push your repository to GitHub.
   - In your repository settings, enable GitHub Pages and set the source to the root or `/docs` folder (wherever your HTML files are).
   - The generated `index.html` will serve as the landing page.

## Files
- `generate_index.py`: Python script to generate the HTML index.
- `index.html`: Generated file listing all HTML files.
- Other `.html` files: Your landing pages.

## Example
After running the script, your `index.html` will look like a modern, styled list of all HTML files in the project, each with a clickable link.

