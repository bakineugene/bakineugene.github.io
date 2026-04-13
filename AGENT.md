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
├── docs/                       # Generated HTML output
│   ├── index.html
│   ├── style.css
│   ├── attiny13a/              # Technical articles
│   └── blog/                   # Generated blog posts
├── scripts/                    # Build automation scripts
│   ├── generate-blog-index.py  # Blog post listing generator
│   └── insert_blog_listing.py  # Template insertion script
├── src/                        # Source Markdown files
│   ├── index.md                # Generated index (from template)
│   ├── index.template.md       # Index template with blog markers
│   ├── attiny13a/              # ATtiny13A microcontroller articles
│   └── blog/                   # Blog post directories
│       ├── DD-MM-YYYY-Post_Title/
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

- **Static Site Generator**: Pandoc with custom Lua filter
- **Build System**: GNU Make
- **Styling**: Custom CSS with CSS variables
- **Blog System**: Python scripts with YAML frontmatter
- **Resume Generator**: Node.js with markup-js templating
- **Version Control**: Git with submodules

## Blog System

The blog system extends the static site generator with automated blog post management, listing generation, and template-based index creation.

### Blog Post Structure
- **Directory Naming**: `DD-MM-YYYY-Post_Title` (e.g., `13-04-2026-Welcome_To_My_Blog`)
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

### Creating New Blog Posts
1. Create a new directory in `src/blog/` with the naming convention
2. Add an `index.md` file with YAML frontmatter and content
3. Run `make` to generate the updated index and HTML files
4. The new post will appear on the homepage blog listing

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
4. Applies the Lua filter to convert `.md` links to `.html` links

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
mkdir -p src/blog/DD-MM-YYYY-Post_Title

# Create index.md with YAML frontmatter
vim src/blog/DD-MM-YYYY-Post_Title/index.md

# Add frontmatter and content
# Example frontmatter:
# ---
# title: "Post Title"
# date: YYYY-MM-DD
# author: Your Name
# tags: [tag1, tag2]
# summary: "Brief description"
# ---

# Build the site (automatically updates blog listing)
make

# Verify the output
open docs/blog/DD-MM-YYYY-Post_Title/index.html
```

### 3. Updating Styles
1. Edit `style.css`
2. Run `make` to copy to `docs/`
3. Test with existing pages

### 4. Modifying Resume
```bash
cd resume
# Edit data.json for content changes
# Edit index.markup for template changes
# Edit css/main.css for styling
node generator.js
```

### 5. Troubleshooting Build Issues
- Ensure `pandoc` is installed: `pandoc --version`
- Check Makefile syntax: `make -n` (dry run)
- Verify file permissions
- Check for missing dependencies in resume: `npm list`
- Ensure Python 3 is available for blog index generation

## Design Principles

1. **Simplicity**: Minimal dependencies, straightforward build process
2. **Portability**: Uses standard tools (Make, Pandoc)
3. **Separation of Concerns**: Content (Markdown), Style (CSS), Build (Make)
4. **Version Control**: All source files tracked, generated files in docs/

## File Descriptions

### `Makefile`
- Defines build targets and dependencies
- Uses pattern rules for Markdown → HTML conversion
- Handles CSS copying and directory creation

### `md-to-html-links.lua`
- Pandoc Lua filter
- Processes Link elements in AST
- Converts `.md` file extensions to `.html`

### `style.css`
- Modern CSS with CSS variables
- Responsive design
- Typography-focused styling
- Code block styling

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
```

## Contact & Resources

- Repository: https://github.com/bakineugene/bakineugene.github.io
- Live site: https://bakineugene.github.io
- Resume submodule: https://github.com/bakineugene/resume

---

*This document was generated for agent assistance. Update it when project structure or workflows change.*