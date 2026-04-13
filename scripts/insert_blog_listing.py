#!/usr/bin/env python3
"""
Insert blog listing into template file.
Usage: python3 insert_blog_listing.py <template> <listing> <output>
"""

import sys
import os

def insert_listing(template_path, listing_path, output_path):
    """Insert listing content between BLOG_POSTS_START and BLOG_POSTS_END markers"""
    with open(template_path, 'r', encoding='utf-8') as f:
        template = f.read()
    
    with open(listing_path, 'r', encoding='utf-8') as f:
        listing = f.read()
    
    start_marker = '<!-- BLOG_POSTS_START -->'
    end_marker = '<!-- BLOG_POSTS_END -->'
    
    # Find the region between markers
    start_pos = template.find(start_marker)
    end_pos = template.find(end_marker)
    
    if start_pos == -1 or end_pos == -1:
        print("Error: Markers not found in template", file=sys.stderr)
        sys.exit(1)
    
    # Include the end marker in the replacement
    end_pos += len(end_marker)
    
    # Build new content
    new_content = template[:start_pos] + start_marker + '\n' + listing + '\n' + end_marker + template[end_pos:]
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(new_content)

if __name__ == '__main__':
    if len(sys.argv) != 4:
        print("Usage: python3 insert_blog_listing.py <template> <listing> <output>", file=sys.stderr)
        sys.exit(1)
    
    template_file = sys.argv[1]
    listing_file = sys.argv[2]
    output_file = sys.argv[3]
    
    if not os.path.exists(template_file):
        # If template doesn't exist, just copy listing to output
        with open(listing_file, 'r', encoding='utf-8') as f:
            listing = f.read()
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(listing)
    else:
        insert_listing(template_file, listing_file, output_file)