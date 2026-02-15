# Find all markdown files under src/
SRC_MD := $(shell find src -type f -name "*.md")

# Convert src/foo.md -> weblog/foo.html
OUT_HTML := $(patsubst src/%.md,weblog/%.html,$(SRC_MD))

# Default target
all: $(OUT_HTML)

# Rule to convert
weblog/%.html: src/%.md
	@mkdir -p $(dir $@)
	pandoc $< -o $@

# Clean
clean:
	rm -rf weblog

.PHONY: all clean
