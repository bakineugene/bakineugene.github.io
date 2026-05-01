#!/usr/bin/env python3
"""
Copy media files from Telegram archive to blog post directories.

This script reads the output from parse_telegram_archive.py and copies
referenced media files to the appropriate blog post directories, organizing
them into subdirectories (images/, videos/, files/).

Usage:
    python3 copy_telegram_media.py [--input parsed_posts.json] [--dry-run] [--verbose]
"""

import json
import os
import shutil
import argparse
import sys
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
import re


def load_parsed_posts(input_file: str) -> List[Dict[str, Any]]:
    """
    Load parsed blog posts from JSON file.
    
    Args:
        input_file: Path to JSON file containing parsed blog posts
        
    Returns:
        List of blog post dictionaries
    """
    print(f"Loading parsed posts from: {input_file}")
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        if isinstance(data, list):
            return data
        elif isinstance(data, dict) and 'blog_posts' in data:
            return data['blog_posts']
        else:
            print(f"Warning: Unexpected data format in {input_file}")
            return []
    except FileNotFoundError:
        print(f"Error: Input file not found: {input_file}")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in {input_file}: {e}")
        sys.exit(1)


def get_media_type_directory(media_type: str) -> str:
    """
    Determine the target subdirectory for a media type.
    
    Args:
        media_type: 'photo', 'video', 'file', 'audio'
        
    Returns:
        Subdirectory name (images/, videos/, files/, audio/)
    """
    if media_type == 'photo':
        return 'images'
    elif media_type == 'video':
        return 'videos'
    elif media_type == 'audio':
        return 'audio'
    else:  # 'file' or any other type
        return 'files'


def sanitize_filename(filename: str) -> str:
    """
    Sanitize filename to be safe for filesystem.
    
    Args:
        filename: Original filename
        
    Returns:
        Sanitized filename
    """
    # Replace problematic characters
    filename = re.sub(r'[<>:"|?*]', '_', filename)
    # Remove leading/trailing spaces and dots
    filename = filename.strip('. ')
    # Ensure filename is not empty
    if not filename:
        filename = 'file'
    return filename


def generate_unique_filename(target_dir: Path, filename: str) -> str:
    """
    Generate a unique filename in the target directory.
    
    Args:
        target_dir: Target directory Path object
        filename: Desired filename
        
    Returns:
        Unique filename (may have numeric suffix if file exists)
    """
    if not target_dir.exists():
        return filename
    
    stem = Path(filename).stem
    suffix = Path(filename).suffix
    
    # Check if file already exists
    if not (target_dir / filename).exists():
        return filename
    
    # Try with numeric suffix
    counter = 1
    while True:
        new_filename = f"{stem}_{counter}{suffix}"
        if not (target_dir / new_filename).exists():
            return new_filename
        counter += 1


def copy_media_file(
    source_path: str,
    target_dir: Path,
    media_type: str,
    dry_run: bool = False,
    verbose: bool = False
) -> Tuple[bool, str]:
    """
    Copy a single media file from source to target directory.
    
    Args:
        source_path: Relative path to media file in telegram_archive/
        target_dir: Target directory Path object
        media_type: Type of media ('photo', 'video', 'file', 'audio')
        dry_run: If True, only simulate the copy operation
        verbose: If True, print detailed information
        
    Returns:
        Tuple of (success, new_filename)
    """
    # Check for placeholder paths (from Telegram export when files were too large)
    if source_path.startswith('(') and source_path.endswith(')'):
        if verbose:
            print(f"  Skipping placeholder file: {source_path}")
        return False, ""
    
    # Construct full source path
    telegram_archive_dir = Path("telegram_archive")
    source_file = telegram_archive_dir / source_path
    
    if not source_file.exists():
        print(f"  Warning: Source file not found: {source_file}")
        return False, ""
    
    # Get filename from path
    filename = Path(source_path).name
    filename = sanitize_filename(filename)
    
    # Generate unique filename
    unique_filename = generate_unique_filename(target_dir, filename)
    
    # Create target directory if it doesn't exist
    if not dry_run:
        target_dir.mkdir(parents=True, exist_ok=True)
    
    target_file = target_dir / unique_filename
    
    if verbose:
        print(f"  Copying: {source_path}")
        print(f"    From: {source_file}")
        print(f"    To: {target_file}")
    
    if dry_run:
        print(f"  [DRY RUN] Would copy: {source_path} -> {target_file}")
        return True, unique_filename
    
    try:
        shutil.copy2(source_file, target_file)
        if verbose:
            print(f"    Successfully copied ({source_file.stat().st_size} bytes)")
        return True, unique_filename
    except Exception as e:
        print(f"  Error copying {source_path}: {e}")
        return False, ""


def update_markdown_content(
    content: str,
    media_updates: List[Tuple[str, str, str]]
) -> str:
    """
    Update Markdown content with new media file paths.
    
    Args:
        content: Original Markdown content
        media_updates: List of (old_path, new_path, media_type) tuples
        
    Returns:
        Updated Markdown content
    """
    updated_content = content
    
    for old_path, new_path, media_type in media_updates:
        # Handle different media reference patterns
        patterns = [
            # ![Alt text](old_path)
            (rf'!\[([^\]]*)\]\({re.escape(old_path)}\)', f'![\\1]({new_path})'),
            # [Link text](old_path)
            (rf'\[([^\]]*)\]\({re.escape(old_path)}\)', f'[\\1]({new_path})'),
            # Direct reference in text (less common)
            (rf'(?<!")(?<!\]\(){re.escape(old_path)}(?!\))', new_path)
        ]
        
        for pattern, replacement in patterns:
            updated_content = re.sub(pattern, replacement, updated_content)
    
    return updated_content


def process_blog_post(
    post: Dict[str, Any],
    blog_base_dir: Path,
    dry_run: bool = False,
    verbose: bool = False
) -> Dict[str, Any]:
    """
    Process a single blog post: copy media files and update content.
    
    Args:
        post: Blog post dictionary
        blog_base_dir: Base directory for blog posts (src/blog/)
        dry_run: If True, only simulate operations
        verbose: If True, print detailed information
        
    Returns:
        Updated blog post dictionary
    """
    post_id = post.get('id', 0)
    title = post.get('title', 'Untitled')
    directory_name = post.get('directory_name', f"post_{post_id}")
    
    print(f"\nProcessing post {post_id}: {title}")
    print(f"  Directory: {directory_name}")
    
    # Create blog post directory path
    post_dir = blog_base_dir / directory_name
    
    # Get media files from post
    media_files = post.get('media_files', [])
    if not media_files:
        print("  No media files to process")
        return post
    
    print(f"  Found {len(media_files)} media file(s)")
    
    # Track media updates for content replacement
    media_updates = []
    
    # Process each media file
    for i, media in enumerate(media_files):
        media_type = media.get('type', 'file')
        source_path = media.get('path', '')
        
        if not source_path:
            print(f"  Warning: Media file {i+1} has no path")
            continue
        
        # Determine target subdirectory
        subdir_name = get_media_type_directory(media_type)
        target_dir = post_dir / subdir_name
        
        # Copy the file
        success, new_filename = copy_media_file(
            source_path, target_dir, media_type, dry_run, verbose
        )
        
        if success and new_filename:
            # Construct new relative path for Markdown
            new_relative_path = f"{subdir_name}/{new_filename}"
            media_updates.append((source_path, new_relative_path, media_type))
            
            # Also handle thumbnail if present
            thumbnail_path = media.get('thumbnail')
            if thumbnail_path and Path(thumbnail_path).exists():
                # Copy thumbnail to same directory
                thumb_success, thumb_new_filename = copy_media_file(
                    thumbnail_path, target_dir, 'photo', dry_run, verbose
                )
                if thumb_success and thumb_new_filename:
                    new_thumb_path = f"{subdir_name}/{thumb_new_filename}"
                    media_updates.append((thumbnail_path, new_thumb_path, 'photo'))
    
    # Update Markdown content if we have media updates
    if media_updates and 'content' in post:
        old_content = post['content']
        new_content = update_markdown_content(old_content, media_updates)
        
        if new_content != old_content:
            post['content'] = new_content
            print(f"  Updated Markdown content with {len(media_updates)} path replacements")
            
            # Save updated content to file if post directory exists
            if not dry_run and post_dir.exists():
                markdown_file = post_dir / "index.md"
                try:
                    # Read existing frontmatter if present
                    if markdown_file.exists():
                        with open(markdown_file, 'r', encoding='utf-8') as f:
                            existing_content = f.read()
                        
                        # Check for YAML frontmatter
                        if existing_content.startswith('---'):
                            # Extract frontmatter
                            parts = existing_content.split('---', 2)
                            if len(parts) >= 3:
                                frontmatter = parts[1]
                                # Replace content after frontmatter
                                updated_file_content = f"---{frontmatter}---\n\n{new_content}"
                            else:
                                updated_file_content = new_content
                        else:
                            updated_file_content = new_content
                    else:
                        updated_file_content = new_content
                    
                    # Write updated content
                    with open(markdown_file, 'w', encoding='utf-8') as f:
                        f.write(updated_file_content)
                    print(f"  Saved updated content to {markdown_file}")
                except Exception as e:
                    print(f"  Error saving updated content: {e}")
    
    return post


def main():
    """Main entry point for the script."""
    parser = argparse.ArgumentParser(
        description='Copy media files from Telegram archive to blog post directories.'
    )
    parser.add_argument(
        '--input',
        default='parsed_telegram_posts.json',
        help='Input JSON file with parsed blog posts (default: parsed_telegram_posts.json)'
    )
    parser.add_argument(
        '--output',
        help='Output JSON file with updated posts (optional)'
    )
    parser.add_argument(
        '--blog-dir',
        default='src/blog',
        help='Base directory for blog posts (default: src/blog)'
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Simulate operations without copying files'
    )
    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Print detailed information about each operation'
    )
    parser.add_argument(
        '--skip-existing',
        action='store_true',
        help='Skip copying if target file already exists'
    )
    
    args = parser.parse_args()
    
    # Load parsed posts
    posts = load_parsed_posts(args.input)
    
    if not posts:
        print("No blog posts found to process.")
        return
    
    print(f"Loaded {len(posts)} blog post(s)")
    
    # Create blog base directory
    blog_base_dir = Path(args.blog_dir)
    if not blog_base_dir.exists() and not args.dry_run:
        print(f"Creating blog directory: {blog_base_dir}")
        blog_base_dir.mkdir(parents=True, exist_ok=True)
    
    # Process each blog post
    updated_posts = []
    for post in posts:
        updated_post = process_blog_post(
            post, blog_base_dir, args.dry_run, args.verbose
        )
        updated_posts.append(updated_post)
    
    # Save updated posts to output file if specified
    if args.output:
        try:
            with open(args.output, 'w', encoding='utf-8') as f:
                json.dump(updated_posts, f, indent=2, ensure_ascii=False)
            print(f"\nSaved updated posts to: {args.output}")
        except Exception as e:
            print(f"Error saving output file: {e}")
    
    # Print summary
    print("\n=== PROCESSING SUMMARY ===")
    print(f"Total posts processed: {len(updated_posts)}")
    if args.dry_run:
        print("Mode: DRY RUN (no files were actually copied)")
    else:
        print("Mode: LIVE (files were copied)")


if __name__ == '__main__':
    main()