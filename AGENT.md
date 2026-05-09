# AGENT.md - Project Guide for Future Agents

## Project Overview

This is a personal homepage/weblog project for `bakineugene.github.io`. It's a static site generator that converts Markdown files to HTML using Pandoc, with a separate resume submodule.

## Project Structure

```
bakineugene.github.io/
├── AGENT.md                    # This file - guide for agents
├── README.md                   # Project README
├── Makefile                    # Build automation
├── style.css                   # Main stylesheet
├── md-to-html-links.lua        # Pandoc Lua filter for link conversion
├── add-navigation.lua          # Pandoc Lua filter for blog post navigation
├── docs/                       # Generated HTML output
│   ├── index.html
│   ├── style.css
│   ├── attiny13a/              # Technical articles
│   └── blog/                   # Generated blog posts
├── scripts/                    # Build automation scripts
│   ├── generate-blog-index.py  # Blog post listing generator
│   ├── insert_blog_listing.py  # Template insertion script
│   └── copy_telegram_media.py  # Media file copier for blog posts
├── src/                        # Source Markdown files
│   ├── index.md                # Generated index (from template)
│   ├── index.template.md       # Index template with blog markers
│   ├── attiny13a/              # ATtiny13A microcontroller articles
│   └── blog/                   # Blog post directories
│       ├── YYYY-MM-DD-Post_Title/
│       │   └── index.md        # Blog post with frontmatter
│       └── ...                 # More blog posts
└── resume/                     # Resume submodule (git submodule)
    ├── generator.js            # Resume HTML generator
    ├── index.markup            # Resume template
    ├── data.json               # Resume data
    ├── css/main.css            # Resume styles
    └── package.json            # Node.js dependencies
```

## Key Technologies

- **Static Site Generator**: Pandoc with custom Lua filters
- **Build System**: GNU Make
- **Styling**: Custom CSS with CSS variables
- **Blog System**: Python scripts with YAML frontmatter and automatic navigation
- **Resume Generator**: Node.js with markup-js templating
- **Version Control**: Git with submodules

## Blog System

The blog system extends the static site generator with automated blog post management, listing generation, template-based index creation, and automatic navigation.

### Blog Post Structure
- **Directory Naming**: `YYYY-MM-DD-Post_Title` (e.g., `2026-04-13-Welcome_To_My_Blog`)
- **Content File**: Each directory contains an `index.md` file
- **Frontmatter**: YAML frontmatter at the top of each post for metadata:
  ```yaml
  ---
  title: "Post Title"
  date: YYYY-MM-DD
  author: Author Name
  tags: [tag1, tag2]
  summary: "Brief description"
  ---
  ```

### Blog Index Generation
The system automatically generates a blog listing on the homepage:

1. **Scripts**:
   - `scripts/generate-blog-index.py`: Scans `src/blog/` directories and creates a markdown list
   - `scripts/insert_blog_listing.py`: Inserts the generated list into the index template

2. **Template System**:
   - `src/index.template.md`: Contains markers `<!-- BLOG_POSTS_START -->` and `<!-- BLOG_POSTS_END -->`
   - Generated content is inserted between these markers
   - Output is saved as `src/index.md`

3. **Build Integration**:
   - The Makefile automatically runs the blog index generation before building HTML
   - Blog posts are converted to HTML alongside other markdown files

### Blog Post Navigation
The system automatically adds "На главную" (To main page) navigation links to all blog posts:

- **Automatic Detection**: Blog posts are detected by YAML frontmatter (title, date, tags, or summary)
- **Navigation Placement**: Links appear at both the beginning and end of each blog post
- **Styling**: Navigation links use the `.nav-home` CSS class with distinctive styling
- **Absolute URLs**: Links use absolute paths configurable via `SITE_ROOT_URL` environment variable

### Creating New Blog Posts
1. Create a new directory in `src/blog/` with the naming convention
2. Add an `index.md` file with YAML frontmatter and content
3. Run `make` to generate the updated index and HTML files
4. The new post will appear on the homepage blog listing with automatic navigation

## Navigation Configuration

The blog post navigation system is configurable for different deployment environments:

### Configuration Sources
The navigation system uses the following priority for determining the root URL:
1. **Pandoc Variable**: `--variable site-root-url=URL` passed to Pandoc
2. **Environment Variable**: `SITE_ROOT_URL` environment variable
3. **Default**: `https://bakineugene.github.io/`

### Usage Examples

**Production Deployment (Default):**
```bash
make
# Uses default root URL: https://bakineugene.github.io/
```

**Local Development:**
```bash
SITE_ROOT_URL=http://localhost:8000 make
# Generates links pointing to local development server
```

**Custom Domain:**
```bash
SITE_ROOT_URL=https://example.com make
# Generates links pointing to custom domain
```

**Direct Pandoc Variable:**
```bash
pandoc input.md -o output.html --lua-filter=add-navigation.lua --variable site-root-url=http://example.com
```

### CSS Styling
Navigation links are styled via the `.nav-home` class in `style.css`:
- Distinctive bordered boxes with centered alignment
- Hover effects with color inversion
- Consistent spacing (2rem margins)
- Responsive design that works on all screen sizes

## Build System

### Main Site Build
The project uses a Makefile to automate the build process:

```bash
# Build the entire site (default)
make

# Clean generated files
make clean
```

**Build Process:**
1. Copies `style.css` to `docs/style.css`
2. Finds all `.md` files in `src/` directory
3. Converts each `.md` file to `.html` in `docs/` using Pandoc
4. Applies two Lua filters:
   - `md-to-html-links.lua`: Converts `.md` links to `.html` links
   - `add-navigation.lua`: Adds "На главную" navigation to blog posts
5. Copies media files (images, videos, audio) preserving directory structure

**Dependencies:**
- `pandoc` - Markdown to HTML conversion
- `make` - Build automation

### Resume Build
The resume is a separate submodule with its own build process:

```bash
cd resume
npm install          # Install dependencies
node generator.js    # Generate index.html from data.json
```

**Resume Dependencies:**
- `fs-extra` - File system utilities
- `markup-js` - Templating engine

## Development Workflow

### Adding New Content
1. Create a new Markdown file in `src/` directory (e.g., `src/new-article.md`)
2. Add links in appropriate index files (`.md` links will be converted to `.html`)
3. Run `make` to generate HTML
4. Commit changes and push to GitHub

### Styling
- Main styles are in `style.css`
- Uses CSS custom properties (variables) for theming
- Responsive design with max-width constraints
- Code blocks have syntax highlighting support
- Navigation links use `.nav-home` class with distinctive styling

### Link Handling
The Lua filter (`md-to-html-links.lua`) automatically converts:
- Local `.md` links → `.html` links
- Preserves external links (http/https)
- Example: `[Link](article.md)` becomes `[Link](article.html)`

## Git Submodules

The `resume/` directory is a git submodule:
- Original repository: `git@github.com:bakineugene/resume.git`
- To update: `git submodule update --remote`
- To clone with submodules: `git clone --recursive`

## Deployment

This is a GitHub Pages site:
- The `docs/` directory is the web root
- GitHub Pages serves from `docs/` branch or directory
- After building with `make`, commit and push to deploy

**Important**: For local testing, use `SITE_ROOT_URL=http://localhost:8000 make` to ensure navigation links work correctly with your local development server.

## Common Tasks for Agents

### 1. Adding a New Article (Non-Blog)
```bash
# Create new markdown file
vim src/new-topic/index.md

# Add content with proper frontmatter (optional)
# Use relative links to other .md files

# Build the site
make

# Verify the output
open docs/new-topic/index.html
```

### 2. Adding a New Blog Post
```bash
# Create blog post directory with naming convention
mkdir -p src/blog/YYYY-MM-DD-Post_Title

# Create index.md with YAML frontmatter
vim src/blog/YYYY-MM-DD-Post_Title/index.md

# Add frontmatter and content
# Example frontmatter:
# ---
# title: "Post Title"
# date: YYYY-MM-DD
# author: Your Name
# tags: [tag1, tag2]
# summary: "Brief description"
# ---

# Build the site (automatically updates blog listing and adds navigation)
make

# Verify the output (check for navigation links)
open docs/blog/YYYY-MM-DD-Post_Title/index.html
```

### 3. Testing Navigation with Local Development Server
```bash
# Start a local HTTP server in the docs directory
cd docs && python3 -m http.server 8000

# In another terminal, rebuild with local root URL
SITE_ROOT_URL=http://localhost:8000 make

# Refresh browser to see navigation links pointing to local server
```

### 4. Handling Media Files for Blog Posts
The `scripts/copy_telegram_media.py` script provides media file management capabilities for blog posts. It can copy media files from external sources into blog post directories and update Markdown content accordingly.

#### Media File Organization
- **Photos**: Copied to `blog_post/images/`
- **Videos**: Copied to `blog_post/videos/`
- **Documents/PDFs**: Copied to `blog_post/files/`
- **Audio files**: Copied to `blog_post/audio/`

#### Using the Media Copy Script
```bash
# Basic usage with a JSON file containing media references
python3 scripts/copy_telegram_media.py --input media_references.json

# Dry-run mode to see what would be copied
python3 scripts/copy_telegram_media.py --input media_references.json --dry-run

# With verbose output
python3 scripts/copy_telegram_media.py --input media_references.json --verbose

# Process only specific blog posts
python3 scripts/copy_telegram_media.py --input media_references.json --blog-dir src/blog
```

#### Script Features
- **Automatic directory creation**: Creates `images/`, `videos/`, `files/`, `audio/` subdirectories as needed
- **Path updating**: Updates Markdown content to reference new file locations
- **Duplicate handling**: Adds numeric suffixes to avoid filename conflicts
- **Error handling**: Skips missing files and placeholder paths
- **Dry-run mode**: Preview operations without copying files
- **Progress reporting**: Shows processing status for each blog post

#### Integration with Blog System
The script works with the existing blog system structure:
- Blog posts are in `src/blog/YYYY-MM-DD-Post_Title/` directories
- Each post has an `index.md` file with YAML frontmatter
- Media references in Markdown are updated automatically
- The script preserves existing frontmatter when updating content

### 5. Updating Styles
1. Edit `style.css`
2. Run `make` to copy to `docs/`
3. Test with existing pages (including navigation links)

### 6. Modifying Resume
```bash
cd resume
# Edit data.json for content changes
# Edit index.markup for template changes
# Edit css/main.css for styling
node generator.js
```

### 7. Troubleshooting Build Issues
- Ensure `pandoc` is installed: `pandoc --version`
- Check Makefile syntax: `make -n` (dry run)
- Verify file permissions
- Check for missing dependencies in resume: `npm list`
- Ensure Python 3 is available for blog index generation
- Verify navigation filter is working: Check generated HTML for "На главную" links

### 8. Testing Pandoc Filters

When developing or modifying Pandoc Lua filters, it's important to test them safely without causing the agent to hang. The following procedures ensure reliable testing:

#### Safe Testing Principles
- **Use simple test files**: Create temporary Markdown files with minimal content
- **Clean up after tests**: Always remove temporary files after verification
- **Avoid complex command chains**: Simple one-liners are less likely to hang
- **Use grep for verification**: Check for expected output patterns
- **Consider timeout mechanisms**: For automated testing, use `timeout` command if available

#### Example Safe Test Command
```bash
# Create a minimal test file
cat > test.md << 'EOF'
---
title: "Test"
date: 2026-01-01
---
Test content
EOF

# Run Pandoc with a timeout to prevent hanging
timeout 2s pandoc test.md -o test.html --lua-filter=add-navigation.lua

# Verify the navigation link was added
if grep -q 'На главную' test.html; then
    echo "✓ Filter added navigation successfully"
else
    echo "✗ Filter failed to add navigation"
fi

# Clean up
rm -f test.md test.html
```

This approach:
1. Uses a heredoc to create the test file (avoids echo issues)
2. Adds a 2-second timeout to prevent infinite hangs
3. Separates verification from execution for better error handling
4. Provides clear success/failure feedback

#### Testing Filter Modifications
When modifying filters like `add-navigation.lua`:
1. Create a test file that matches the filter's detection criteria (has title and date)
2. Run the filter in isolation to verify behavior
3. Check the generated HTML structure (e.g., navigation placement)
4. Compare with expected output using `diff` or pattern matching

#### Troubleshooting Hanging Commands
If a Pandoc command appears to hang:
- Check for infinite loops in Lua filters
- Ensure the filter terminates (returns a document)
- Use `timeout 5s pandoc ...` to limit execution time
- Test with smaller input files
- Verify Pandoc version compatibility
- Consider testing outside the agent environment (direct terminal)

## Design Principles

1. **Simplicity**: Minimal dependencies, straightforward build process
2. **Portability**: Uses standard tools (Make, Pandoc)
3. **Separation of Concerns**: Content (Markdown), Style (CSS), Build (Make)
4. **Version Control**: All source files tracked, generated files in docs/
5. **User Experience**: Automatic navigation for better blog post usability

## File Descriptions

### `Makefile`
- Defines build targets and dependencies
- Uses pattern rules for Markdown → HTML conversion
- Handles CSS copying and directory creation
- Supports configurable `SITE_ROOT_URL` for navigation links

### `md-to-html-links.lua`
- Pandoc Lua filter
- Processes Link elements in AST
- Converts `.md` file extensions to `.html`

### `add-navigation.lua`
- Pandoc Lua filter for blog post navigation
- Detects blog posts by YAML frontmatter metadata
- Adds "На главную" links at beginning and end of blog posts
- Configurable root URL via environment variable or Pandoc variable
- Uses absolute paths for reliable navigation across deployment environments

### `style.css`
- Modern CSS with CSS variables
- Responsive design
- Typography-focused styling
- Code block styling
- Navigation link styling (`.nav-home` class)

### `resume/generator.js`
- Node.js script
- Reads JSON data and markup template
- Generates static HTML resume
- Uses markup-js for templating

## Best Practices for Maintenance

1. **Keep dependencies minimal**: Only add tools when necessary
2. **Test builds**: Always run `make` after changes
3. **Use relative links**: For portability across environments
4. **Document changes**: Update this AGENT.md when modifying workflows
5. **Backup generated files**: `docs/` should be committed for deployment
6. **Test navigation**: Verify navigation links work correctly in both local and production environments

## Environment Setup

For new contributors/agents:

```bash
# 1. Install system dependencies
sudo apt-get install pandoc make  # Ubuntu/Debian
# or
brew install pandoc make         # macOS

# 2. Clone repository with submodules
git clone --recursive https://github.com/bakineugene/bakineugene.github.io

# 3. Build the site
cd bakineugene.github.io
make

# 4. Setup resume (optional)
cd resume
npm install
node generator.js

# 5. Test local development
SITE_ROOT_URL=http://localhost:8000 make
cd docs && python3 -m http.server 8000
```

## Contact & Resources

- Repository: https://github.com/bakineugene/bakineugene.github.io
- Live site: https://bakineugene.github.io
- Resume submodule: https://github.com/bakineugene/resume

---

*This document was generated for agent assistance. Update it when project structure or workflows change.*