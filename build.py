#!/usr/bin/env python3
import os
import markdown
import frontmatter
from datetime import datetime, date
import re
import datetime as dt

# Define a string for the header/nav section that will be used across all pages
HEADER_CSS = '''
header {
  max-width: 1100px;
  margin: 0 auto 2rem auto;
  padding: 2rem 0 0 0;
  background: none;
  box-shadow: none;
}
header h1 {
  margin: 0 0 0.5em 0;
  font-size: 2.5rem;
  color: #fff;
  letter-spacing: 2px;
  font-weight: 700;
  text-align: center;
}
.main-nav {
  display: flex;
  gap: 1.5rem;
  background: #fff;
  padding: 1rem 2rem;
  font-size: 1.1rem;
  margin-bottom: 2rem;
  justify-content: center;
  border-radius: 6px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
  width: 100%;
  box-sizing: border-box;
}
.main-nav a {
  color: #666666;
  text-decoration: none;
  padding: 0.3em 0.7em;
  border-radius: 3px;
  transition: background 0.15s;
}
.main-nav a:hover, .main-nav a.active {
  background: #f0f0f0;
}
'''

# Footer HTML and year
current_year = dt.datetime.now().year
FOOTER_HTML = '<footer class="site-footer">© jackchartres.xyz {year}</footer>'

# NAV setup with direct HTML (no wrapper)
NAV_HTML = '''<nav class="main-nav">
  <a href="/" hx-get="/" hx-swap="innerHTML" hx-target="#content">Home</a>
  <a href="/contact.html" hx-get="/contact.html" hx-swap="innerHTML" hx-target="#content">Contact</a>
</nav>'''

# Directories and paths
POSTS_DIR = "blog"
BLOG_DIR = "docs"  # Physical path for file generation (root of docs directory)
ASSETS_DIR = "docs/assets/images"
ASSETS_DIR_URL = "/assets/images"
TEMPLATES_DIR = "templates"

# Ensure output directories exist
os.makedirs(ASSETS_DIR, exist_ok=True)
os.makedirs("docs/vendor", exist_ok=True)

# Load posts
posts = []
for fname in os.listdir(POSTS_DIR):
    if not fname.endswith(".md"): continue
    path = os.path.join(POSTS_DIR, fname)
    fm = frontmatter.load(path)
    # Parse date from front matter: handle string, datetime, or date
    raw_date = fm['date']
    if isinstance(raw_date, str):
        date_obj = datetime.strptime(raw_date, "%Y-%m-%d").date()
    elif isinstance(raw_date, datetime):
        date_obj = raw_date.date()
    else:
        # assume PyYAML parsed into date object
        date_obj = raw_date
    # Derive slug from filename (strip date prefix)
    slug = fname[11:-3]
    # Convert markdown content to HTML
    content_html = markdown.markdown(fm.content, extensions=['fenced_code'])
    
    # Clean up WordPress-style image captions
    caption_pattern = r'\[caption.*?width="(\d+)".*?\](.*?)\[/caption\]'
    def caption_replace(match):
        width = match.group(1)
        content = match.group(2)
        # Remove any trailing "Rendering..." or similar text after the image
        content = re.sub(r'\s*Rendering[^<]*$', '', content)
        # Extract the image URL to add specific sizing
        img_match = re.search(r'<img.*?src="([^"]+)"', content)
        if img_match:
            img_url = img_match.group(1)
            # Extract only the image tag from content
            img_tag = re.search(r'(<img[^>]*>)', content)
            if img_tag:
                img_only = img_tag.group(1)
            else:
                img_only = content
            # Create figure with caption
            img_caption = re.sub(r'.*<img.*?/>\s*(.*)', r'\1', content).strip()
            return f'''<figure class="image-container" style="max-width: {width}px; margin: 0 auto;">
{img_only}
<figcaption>{img_caption}</figcaption>
</figure>'''
        else:
            return f'<div class="image-container" style="max-width: {width}px; margin: 0 auto;">{content}</div>'
    
    content_html = re.sub(caption_pattern, caption_replace, content_html)
    
    # Fix image paths for static assets
    content_html = content_html.replace('src="images/', f'src="{ASSETS_DIR_URL}/')
    posts.append({
        'title': fm['title'],
        'date': date_obj,
        'slug': slug,
        'coverImage': fm.get('coverImage', None),
        'content': content_html
    })

# Sort posts by date descending
posts.sort(key=lambda x: x['date'], reverse=True)

# Generate per-post HTML pages
for p in posts:
    # Create directory structure for new URL format: YYYY/MM/DD/slug/
    year = p['date'].strftime('%Y')
    month = p['date'].strftime('%m')
    day = p['date'].strftime('%d')
    post_dir = os.path.join(BLOG_DIR, year, month, day, p['slug'])
    
    # Ensure the directory exists
    os.makedirs(post_dir, exist_ok=True)
    
    # Define the URL path for this post (for navigation)
    post_url = f"/{year}/{month}/{day}/{p['slug']}/"
    
    cover_html = ''
    if p['coverImage']:
        cover_html = f'<div class="cover-image"><img src="{ASSETS_DIR_URL}/{p["coverImage"]}" alt="Cover image"/></div>'
    
    # Calculate relative path to root for CSS and scripts
    relative_path_to_root = "../../../../"
    
    page_html = f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8"/>
  <title>{p['title']} - Project Space</title>
  <link rel="stylesheet" href="{relative_path_to_root}styles.css"/>
  <script src="https://unpkg.com/htmx.org@1.10.2"></script>
  <style>
    body {{
      background-color: #23272f;
      margin: 0;
      padding: 0;
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
      line-height: 1.6;
    }}
    {HEADER_CSS}
    #post-content {{
      background-color: white;
      max-width: 1100px;
      margin: 0 auto 2rem;
      padding: 2rem;
      box-shadow: 0 2px 8px rgba(0,0,0,0.1);
      border-radius: 6px;
      box-sizing: border-box;
    }}
    .image-container {{
      text-align: center;
      margin: 2em auto;
    }}
    .image-container img {{
      max-width: 100%;
      height: auto;
      display: block;
      margin: 0 auto;
    }}
    .cover-image {{
      max-width: 100%;
      margin: 1.5em auto 2.5em;
      text-align: center;
    }}
    .cover-image img {{
      max-width: 100%;
      height: auto;
      border-radius: 4px;
      box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }}
    figure.image-container {{
      display: block;
      margin: 2em auto;
    }}
    figcaption {{
      font-size: 0.9em;
      color: #666;
      margin-top: 0.5em;
      text-align: center;
      font-style: italic;
    }}
    h2, h3, h4 {{
      color: #23272f;
      font-weight: 700;
      letter-spacing: 0.5px;
      margin-top: 2rem;
      margin-bottom: 1rem;
    }}
    h2 {{
      font-size: 2rem;
      border-bottom: 2px solid #bbb;
      display: inline-block;
      padding-bottom: 0.2em;
    }}
    h3 {{
      font-size: 1.3rem;
    }}
    h4 {{
      font-size: 1.1rem;
    }}
    time {{
      display: block;
      color: #666;
      margin-bottom: 1rem;
    }}
    p {{
      margin-bottom: 1.2rem;
    }}
    .site-footer {{
      text-align: center;
      color: #888;
      font-size: 1em;
      padding: 2em 0 1em 0;
      background: none;
    }}
    .contact-section {{
      margin-top: 4rem;
      padding-top: 2rem;
      border-top: 1px solid #ddd;
    }}
    .email-form {{
      display: flex;
      flex-direction: column;
      gap: 1.2rem;
      margin-top: 1rem;
    }}
    .email-form label {{
      font-weight: 500;
    }}
    .email-form input[type="text"], 
    .email-form input[type="email"], 
    .email-form textarea {{
      padding: 0.7em;
      border: 1px solid #ccc;
      border-radius: 4px;
      font-size: 1em;
    }}
    .email-form textarea {{
      min-height: 120px;
      resize: vertical;
    }}
    .email-form button {{
      background: #666666;
      color: #fff;
      border: none;
      border-radius: 4px;
      padding: 0.8em 1.5em;
      font-size: 1em;
      cursor: pointer;
      align-self: flex-start;
      transition: background 0.15s;
    }}
    .email-form button:hover {{
      background: #555555;
    }}
    .subscribe-section {{
      margin-top: 3rem;
      padding-top: 2rem;
      border-top: 1px solid #ddd;
    }}
    .subscribe-section p {{
      margin-bottom: 1rem;
      font-size: 0.95em;
      color: #555;
    }}
    .subscribe-input-group {{
      display: flex;
      gap: 0.5rem;
      max-width: 500px;
    }}
    .subscribe-form input[type="email"] {{
      flex: 1;
      padding: 0.7em;
      border: 1px solid #ccc;
      border-radius: 4px;
      font-size: 1em;
    }}
    .subscribe-form button {{
      background: #666666;
      color: #fff;
      border: none;
      border-radius: 4px;
      padding: 0.7em 1.2em;
      font-size: 1em;
      cursor: pointer;
      white-space: nowrap;
      transition: background 0.15s;
    }}
    .subscribe-form button:hover {{
      background: #555555;
    }}
  </style>
</head>
<body>
  <header>
    <h1>Project Space</h1>
    {NAV_HTML}
  </header>
  <article id="post-content">
    <h2>{p['title']}</h2>
    <time datetime="{p['date'].isoformat()}">{p['date'].strftime('%B %d, %Y')}</time>
    {cover_html}
    {p['content']}
    
    <div class="contact-section">
      <h3>Contact Me About This Post</h3>
      <form class="email-form" action="mailto:your-email@example.com" method="post" enctype="text/plain">
        <label for="name">Name</label>
        <input type="text" id="name" name="name" required />
        <label for="email">Your Email</label>
        <input type="email" id="email" name="email" required />
        <label for="subject">Subject</label>
        <input type="text" id="subject" name="subject" value="Re: {p['title']}" required />
        <label for="message">Message</label>
        <textarea id="message" name="message" required></textarea>
        <button type="submit">Send Email</button>
      </form>
    </div>
    
    <div class="subscribe-section">
      <h3>Subscribe to Blog Updates</h3>
      <p>Enter your email to receive notifications when new posts are published.</p>
      <form class="subscribe-form" action="mailto:your-email@example.com?subject=Blog Subscription" method="post" enctype="text/plain">
        <div class="subscribe-input-group">
          <input type="email" id="subscribe-email" name="subscribe-email" placeholder="Your email address" required />
          <button type="submit">Subscribe</button>
        </div>
      </form>
    </div>
  </article>
  {FOOTER_HTML.format(year=current_year)}
</body>
</html>'''  
    # Write the index.html file in the post directory
    with open(os.path.join(post_dir, "index.html"), 'w', encoding='utf-8') as f:
        f.write(page_html)

# Generate grid of cards for index
card_items = ''
for p in posts:
    date_str = p['date'].strftime('%B %d, %Y')
    # Create the post URL in the new format
    year = p['date'].strftime('%Y')
    month = p['date'].strftime('%m')
    day = p['date'].strftime('%d')
    post_url = f"/{year}/{month}/{day}/{p['slug']}/"
    
    cover_html = ''
    if p['coverImage']:
        cover_html = f'<div class="card-image"><img src="{ASSETS_DIR_URL}/{p["coverImage"]}" alt="{p["title"]} cover"/></div>'
    card_items += f'''
      <div class="post-card">
        <a hx-get="{post_url} #post-content" hx-swap="innerHTML" hx-target="#content" href="{post_url}">
          {cover_html}
          <div class="card-content">
            <h2>{p['title']}</h2>
            <time datetime="{p['date'].isoformat()}">{date_str}</time>
          </div>
        </a>
      </div>
    '''
index_html = f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8"/>
  <title>Project Space</title>
  <link rel="stylesheet" href="styles.css"/>
  <script src="https://unpkg.com/htmx.org@1.10.2"></script>
  <style>
    body {{
      background-color: #23272f;
      margin: 0;
      padding: 0;
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
      line-height: 1.6;
    }}
    {HEADER_CSS}
    #content {{
      background-color: white;
      max-width: 1100px;
      margin: 0 auto 2rem;
      padding: 2rem;
      box-shadow: 0 2px 8px rgba(0,0,0,0.1);
      border-radius: 6px;
      box-sizing: border-box;
    }}
    .post-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
      gap: 2rem;
      margin: 0;
      padding: 0;
    }}
    .post-card {{
      background: #fff;
      border-radius: 8px;
      box-shadow: 0 2px 8px rgba(0,0,0,0.08);
      overflow: hidden;
      transition: box-shadow 0.2s;
      display: flex;
      flex-direction: column;
      min-width: 0;
    }}
    .post-card:hover {{
      box-shadow: 0 4px 16px rgba(0,0,0,0.13);
    }}
    .post-card a {{
      color: inherit;
      text-decoration: none;
      display: flex;
      flex-direction: column;
      height: 100%;
    }}
    .card-image img {{
      width: 100%;
      height: 180px;
      object-fit: cover;
      display: block;
    }}
    .card-content {{
      padding: 1.2rem 1rem 1rem 1rem;
      flex: 1 1 auto;
      display: flex;
      flex-direction: column;
      justify-content: flex-end;
    }}
    .card-content h2 {{
      font-size: 1.2rem;
      margin: 0 0 0.5rem 0;
      font-weight: 600;
    }}
    .card-content time {{
      color: #888;
      font-size: 0.95em;
    }}
    .subscribe-section {{
      margin-top: 3rem;
      padding-top: 2rem;
      border-top: 1px solid #ddd;
    }}
    .subscribe-section h3 {{
      margin-bottom: 0.5rem;
    }}
    .subscribe-section p {{
      margin-bottom: 1rem;
      font-size: 0.95em;
      color: #555;
    }}
    .subscribe-input-group {{
      display: flex;
      gap: 0.5rem;
      max-width: 500px;
    }}
    .subscribe-form input[type="email"] {{
      flex: 1;
      padding: 0.7em;
      border: 1px solid #ccc;
      border-radius: 4px;
      font-size: 1em;
    }}
    .subscribe-form button {{
      background: #666666;
      color: #fff;
      border: none;
      border-radius: 4px;
      padding: 0.7em 1.2em;
      font-size: 1em;
      cursor: pointer;
      white-space: nowrap;
      transition: background 0.15s;
    }}
    .subscribe-form button:hover {{
      background: #555555;
    }}
    .site-footer {{
      text-align: center;
      color: #888;
      font-size: 1em;
      padding: 2em 0 1em 0;
      background: none;
    }}
  </style>
</head>
<body>
  <header>
    <h1>Project Space</h1>
    {NAV_HTML}
  </header>
  <div id="content">
    <div class="post-grid">
      {card_items}
    </div>
    
    <div class="subscribe-section">
      <h3>Subscribe to Blog Updates</h3>
      <p>Enter your email to receive notifications when new posts are published.</p>
      <form class="subscribe-form" action="mailto:your-email@example.com?subject=Blog Subscription" method="post" enctype="text/plain">
        <div class="subscribe-input-group">
          <input type="email" id="subscribe-email" name="subscribe-email" placeholder="Your email address" required />
          <button type="submit">Subscribe</button>
        </div>
      </form>
    </div>
  </div>
  {FOOTER_HTML.format(year=current_year)}
</body>
</html>'''
with open("docs/index.html", 'w', encoding='utf-8') as f:
    f.write(index_html)

# Generate contact.html
contact_html = f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8"/>
  <title>Contact - Project Space</title>
  <link rel="stylesheet" href="styles.css"/>
  <script src="https://unpkg.com/htmx.org@1.10.2"></script>
  <style>
    body {{
      background-color: #23272f;
      margin: 0;
      padding: 0;
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
      line-height: 1.6;
    }}
    {HEADER_CSS}
    #content {{
      background-color: white;
      max-width: 500px;
      margin: 0 auto 2rem;
      padding: 2rem;
      box-shadow: 0 2px 8px rgba(0,0,0,0.1);
      border-radius: 4px;
      box-sizing: border-box;
    }}
    form {{
      display: flex;
      flex-direction: column;
      gap: 1.2rem;
    }}
    label {{
      font-weight: 500;
    }}
    input, textarea {{
      padding: 0.7em;
      border: 1px solid #ccc;
      border-radius: 4px;
      font-size: 1em;
    }}
    textarea {{
      min-height: 120px;
      resize: vertical;
    }}
    button {{
      background: #666666;
      color: #fff;
      border: none;
      border-radius: 4px;
      padding: 0.8em 1.5em;
      font-size: 1em;
      cursor: pointer;
      transition: background 0.15s;
    }}
    button:hover {{
      background: #555555;
    }}
    .subscribe-section {{
      margin-top: 3rem;
      padding-top: 2rem;
      border-top: 1px solid #ddd;
    }}
    .subscribe-section h3 {{
      margin-bottom: 0.5rem;
    }}
    .subscribe-section p {{
      margin-bottom: 1rem;
      font-size: 0.95em;
      color: #555;
    }}
    .subscribe-input-group {{
      display: flex;
      gap: 0.5rem;
      max-width: 500px;
    }}
    .subscribe-form input[type="email"] {{
      flex: 1;
      padding: 0.7em;
      border: 1px solid #ccc;
      border-radius: 4px;
      font-size: 1em;
    }}
    .subscribe-form button {{
      background: #666666;
      color: #fff;
      border: none;
      border-radius: 4px;
      padding: 0.7em 1.2em;
      font-size: 1em;
      cursor: pointer;
      white-space: nowrap;
      transition: background 0.15s;
    }}
    .subscribe-form button:hover {{
      background: #555555;
    }}
    .site-footer {{
      text-align: center;
      color: #888;
      font-size: 1em;
      padding: 2em 0 1em 0;
      background: none;
    }}
  </style>
</head>
<body>
  <header>
    <h1>Project Space</h1>
    {NAV_HTML}
  </header>
  <div id="content">
    <h2>Contact</h2>
    <form>
      <label for="name">Name</label>
      <input type="text" id="name" name="name" required />
      <label for="email">Email</label>
      <input type="email" id="email" name="email" required />
      <label for="message">Message</label>
      <textarea id="message" name="message" required></textarea>
      <button type="submit" disabled>Send (coming soon)</button>
    </form>
    
    <div class="subscribe-section">
      <h3>Subscribe to Blog Updates</h3>
      <p>Enter your email to receive notifications when new posts are published.</p>
      <form class="subscribe-form" action="mailto:your-email@example.com?subject=Blog Subscription" method="post" enctype="text/plain">
        <div class="subscribe-input-group">
          <input type="email" id="subscribe-email" name="subscribe-email" placeholder="Your email address" required />
          <button type="submit">Subscribe</button>
        </div>
      </form>
    </div>
  </div>
  {FOOTER_HTML.format(year=current_year)}
</body>
</html>'''
with open("docs/contact.html", 'w', encoding='utf-8') as f:
    f.write(contact_html) 