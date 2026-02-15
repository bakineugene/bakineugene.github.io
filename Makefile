# Find markdown files
SRC_MD := $(shell find src -type f -name "*.md")

# Map to docs
OUT_HTML := $(patsubst src/%.md,docs/%.html,$(SRC_MD))

CSS := /style.css

all: $(OUT_HTML)

docs/%.html: src/%.md
	@mkdir -p $(dir $@)
	pandoc $< -o $@ -s --css=$(CSS)

clean:
	rm -rf docs

.PHONY: all clean
