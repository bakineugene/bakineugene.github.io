# bakineugene.github.io

Personal homepage and weblog for Eugene Bakin.

## Overview

This is a static site generated from Markdown using Pandoc, with a custom blog system and resume submodule.

## Features

- **Static Site Generation**: Convert Markdown to HTML using Pandoc with custom Lua filters
- **Blog System**: Automated blog post management with YAML frontmatter and automatic index generation
- **Responsive Design**: Custom CSS with CSS variables for theming
- **Resume**: Separate resume submodule with JSON-based data and templating
- **GitHub Pages**: Deployed automatically from the `docs/` directory

## Project Structure

```
bakineugene.github.io/
├── AGENT.md                    # Guide for agents (comprehensive documentation)
├── README.md                   # This file
├── Makefile                    # Build automation
├── style.css                   # Main stylesheet
├── md-to-html-links.lua        # Pandoc Lua filter for link conversion
├── docs/                       # Generated HTML output (GitHub Pages root)
├── scripts/                    # Build automation scripts
├── src/                        # Source Markdown files
└── resume/                     # Resume submodule
```

## Quick Start

### Building the Site

```bash
# Install dependencies (Ubuntu/Debian)
sudo apt-get install pandoc make

# Clone repository with submodules
git clone --recursive https://github.com/bakineugene/bakineugene.github.io
cd bakineugene.github.io

# Build the site
make

# The generated site will be in docs/
```

### Adding Content

#### Regular Articles
Create Markdown files in `src/` directory. Use relative `.md` links – they will be automatically converted to `.html` links.

#### Blog Posts
1. Create a directory in `src/blog/` with naming convention `DD-MM-YYYY-Post_Title`
2. Add an `index.md` file with YAML frontmatter:
   ```yaml
   ---
   title: "Post Title"
   date: YYYY-MM-DD
   author: Your Name
   tags: [tag1, tag2]
   summary: "Brief description"
   ---
   ```
3. Run `make` to generate the updated index and HTML files

### Updating Resume
```bash
cd resume
npm install
node generator.js
```

## Blog System

The blog system automatically:
- Scans `src/blog/` directories for posts
- Generates a listing with metadata (title, date, author, tags, summary)
- Inserts the listing into the main index page between `<!-- BLOG_POSTS_START -->` and `<!-- BLOG_POSTS_END -->` markers
- Sorts posts in reverse chronological order (newest first)

## Deployment

The site is deployed via GitHub Pages from the `docs/` directory. After building with `make`, commit and push changes to deploy.

## Documentation

For detailed documentation, see [AGENT.md](AGENT.md) which includes:
- Complete project structure
- Build system details
- Blog system implementation
- Common tasks for agents
- File descriptions
- Environment setup

## License

Personal project – not licensed for redistribution.
