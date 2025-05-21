# JACK\_CHARTRES\_XYZ

A simple static site generated from Markdown, based on content exported from WordPress.

## Usage

1. **Install dependencies**

   ```bash
   python -m venv .venv
   pip install -r requirements.txt
   ```

2. **Generate the site**

   ```bash
   python build.py
   ```

3. **Preview locally**

   ```bash
   python -m http.server --directory docs
   ```

## Deployment

This site is published via GitHub Pages from the `docs/` folder on the `main` branch.

---

© 2025 Jack Chartres

