# Find all markdown files under src/
SRC_MD := $(shell find src -type f -name "*.md")

# Map src/foo.md -> weblog/foo.html
OUT_HTML := $(patsubst src/%.md,weblog/%.html,$(SRC_MD))

CSS := style.css

# Default target
all: $(OUT_HTML)

# Rule to convert markdown to html
weblog/%.html: src/%.md
	@mkdir -p $(dir $@)
	pandoc $< -o $@ -s --css=$(CSS)

# Clean output
clean:
	rm -rf weblog/*.html weblog/*/

.PHONY: all clean
