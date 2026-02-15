# Find markdown files
SRC_MD := $(shell find src -type f -name "*.md")

# Map to docs
OUT_HTML := $(patsubst src/%.md,docs/%.html,$(SRC_MD))

CSS_SRC := style.css
CSS_DST := docs/style.css

CSS := /style.css

# Default target
all: $(CSS_DST) $(OUT_HTML)

# Copy CSS once
$(CSS_DST): $(CSS_SRC)
	@mkdir -p docs
	cp $(CSS_SRC) $(CSS_DST)

# Convert markdown to HTML
docs/%.html: src/%.md | $(CSS_DST)
	@mkdir -p $(dir $@)
	pandoc $< -o $@ -s --css=$(CSS)

# Clean
clean:
	rm -rf docs

.PHONY: all clean
