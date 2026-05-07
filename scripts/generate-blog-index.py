#!/usr/bin/env python3
"""
Generate blog post listing for index.md
Scans src/blog/ for directories matching YYYY-MM-DD-* pattern
Generates markdown list in reverse chronological order
"""

import os
import re
import sys
import locale
from datetime import datetime

def extract_date_title(dirname):
    """Extract date and title from directory name"""
    locale.setlocale(locale.LC_TIME, 'ru_RU.UTF-8')
    pattern = r'^(\d{4})-(\d{2})-(\d{2})-(.+)$'
    match = re.match(pattern, dirname)
    if match:
        year, month, day, title = match.groups()
        # Convert to readable date
        try:
            date_obj = datetime(int(year), int(month), int(day))
            readable_date = date_obj.strftime('%d %B %Y')
        except ValueError:
            # Fallback if date is invalid
            readable_date = f"{day}-{month}-{year}"
        # Convert underscores to spaces in title
        readable_title = title.replace('_', ' ')
        return {
            'dirname': dirname,
            'date': readable_date,
            'title': readable_title,
            'raw_date': f'{year}{month}{day}',  # For sorting (YYYYMMDD)
            'year': year,
            'month': month,
            'day': day
        }
    return None

def extract_frontmatter_simple(filepath):
    """
    Extract YAML frontmatter from markdown file using simple parsing.
    Returns dict with frontmatter values.
    """
    frontmatter = {}
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except (IOError, UnicodeDecodeError):
        return frontmatter
    
    if not lines or not lines[0].startswith('---'):
        return frontmatter
    
    # Collect lines between --- delimiters
    fm_lines = []
    in_frontmatter = False
    for line in lines[1:]:  # Skip first ---
        if line.startswith('---'):
            break
        fm_lines.append(line)
    
    # Simple key: value parsing
    for line in fm_lines:
        line = line.strip()
        if ':' in line:
            key, value = line.split(':', 1)
            key = key.strip()
            value = value.strip()
            # Remove quotes
            if value.startswith('"') and value.endswith('"'):
                value = value[1:-1]
            elif value.startswith("'") and value.endswith("'"):
                value = value[1:-1]
            # Handle list values
            if value.startswith('[') and value.endswith(']'):
                # Simple list parsing
                items = value[1:-1].split(',')
                value = [item.strip().strip('"\'') for item in items]
            frontmatter[key] = value
    
    return frontmatter

def generate_blog_listing(blog_dir='src/blog'):
    """Generate markdown list of blog posts"""
    if not os.path.exists(blog_dir):
        return "# Blog\n\nNo blog posts yet.\n"
    
    posts = []
    for item in os.listdir(blog_dir):
        item_path = os.path.join(blog_dir, item)
        if os.path.isdir(item_path):
            post_info = extract_date_title(item)
            if post_info:
                # Check for index.md and extract frontmatter
                index_md = os.path.join(item_path, 'index.md')
                if os.path.exists(index_md):
                    frontmatter = extract_frontmatter_simple(index_md)
                    if frontmatter and 'title' in frontmatter:
                        # Override title from frontmatter if available
                        post_info['title'] = frontmatter['title']
                    if frontmatter and 'tags' in frontmatter:
                        post_info['tags'] = frontmatter['tags']
                    if frontmatter and 'author' in frontmatter:
                        post_info['author'] = frontmatter['author']
                    if frontmatter and 'summary' in frontmatter:
                        post_info['summary'] = frontmatter['summary']
                
                posts.append(post_info)
    
    if not posts:
        return "# Blog\n\nNo blog posts yet.\n"
    
    # Sort in reverse chronological order (newest first)
    posts.sort(key=lambda x: x['raw_date'], reverse=True)
    
    # Generate markdown
    lines = ["# Blog Posts\n"]
    for post in posts:
        link = f"blog/{post['dirname']}/index.html"
        lines.append(f"- **{post['date']}**: [{post['title']}]({link})")
        # Optional: Add author/tags if available
        if 'tags' in post and post['tags']:
            if isinstance(post['tags'], list):
                tags_str = ', '.join(post['tags'])
            else:
                tags_str = str(post['tags'])
            if (len(tags_str) > 0):
                lines[-1] += f" *(tags: {tags_str})*"
        if 'summary' in post:
            lines[-1] += f" — {post['summary']}"
    
    return '\n'.join(lines)

if __name__ == '__main__':
    listing = generate_blog_listing()
    print(listing)
