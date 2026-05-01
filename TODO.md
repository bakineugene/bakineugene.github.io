# TODO: Blog System Improvements

## Priority Items

### 1. Avoid Duplicating Images
**Issue**: Currently images are copied to both `src/blog/.../images/` and `docs/blog/.../images/`. This creates duplication and wastes space.

**Solution**: 
- Modify build process to copy images from `src/` to `docs/` during build
- Keep only source images in `src/`
- Update Makefile to handle image copying

### 2. Images with Preview
**Issue**: Blog posts show full-size images directly without thumbnail/preview functionality.

**Solution**:
- Add thumbnail generation for images
- Implement lightbox or modal preview for larger images
- Consider using `<figure>` with `<figcaption>` for better semantics

### 3. Add Links Back to Blog Root
**Issue**: Blog posts lack navigation to return to main blog index or homepage.

**Solution**:
- Add consistent navigation header/footer to blog posts
- Include "Back to Blog" or "Home" links
- Ensure navigation is present in all generated HTML

### 4. Fix `make` - Currently It Does Not Work
**Issue**: The `make` command may have issues with dependencies or missing files.

**Solution**:
- Test current `make` command to identify specific failures
- Fix any dependency issues in Makefile
- Ensure all required tools (pandoc, python3) are available
- Add proper error handling and logging

### 5. Add Telegram Blog Link
**Issue**: No Telegram link for blog/channel in site navigation.

**Solution**:
- Add Telegram icon/link in site footer or navigation
- Consider adding to social media links section
- Update template to include Telegram reference

## Implementation Notes

### Image Duplication Fix
The current structure has images in both source and output directories. The build process should:
1. Copy images from `src/blog/*/images/` to `docs/blog/*/images/`
2. Only copy when images are newer than destination
3. Clean up old images in `docs/` during `make clean`

### Make Command Issues
Potential issues to investigate:
- Missing `src/index.md` generation
- Python script dependencies
- Pandoc installation and Lua filter
- Directory creation permissions

### Image Preview Implementation
Options:
1. Client-side JavaScript lightbox
2. Server-side thumbnail generation during build
3. CSS-only zoom on hover

Given static site nature, option 2 (build-time thumbnails) is preferred but requires additional dependencies (ImageMagick, etc.). Option 1 (client-side) is simpler to implement.

### Navigation Links
Add to blog post template:
- Breadcrumb navigation: Home → Blog → Post Title
- Previous/Next post navigation
- Back to blog index link

### Telegram Integration
Add to existing navigation/footer:
- Icon: Telegram logo (SVG or Font Awesome)
- Link: `https://t.me/username` or channel link
- Label: "Telegram Blog" or similar

## Dependencies Checklist
- [ ] Python 3 for blog index generation
- [ ] Pandoc for Markdown to HTML conversion
- [ ] Make for build automation
- [ ] (Optional) ImageMagick for thumbnail generation

## Testing Checklist
- [ ] `make` runs without errors
- [ ] Images are copied correctly (no duplication)
- [ ] Blog posts have navigation links
- [ ] Telegram link appears in site
- [ ] Image preview functionality works
- [ ] All existing functionality preserved

## Files to Modify
1. `Makefile` - Add image copying rules, fix dependencies
2. `src/index.template.md` - Add navigation/Telegram link
3. Blog post template (if exists) or CSS/HTML generation
4. `style.css` - Add styles for navigation and image previews
5. Python scripts - Update if needed for navigation generation

## Timeline
1. Fix `make` command (highest priority)
2. Implement image duplication fix
3. Add navigation links
4. Add Telegram link
5. Implement image preview (if time permits)

---
*Last Updated: 2026-04-13*
*Status: In Progress*