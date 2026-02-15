# Find markdown files
SRC_MD := $(shell find src -type f -name "*.md")

# Map to weblog
OUT_HTML := $(patsubst src/%.md,weblog/%.html,$(SRC_MD))

CSS := /style.css

all: $(OUT_HTML)

weblog/%.html: src/%.md
	@mkdir -p $(dir $@)
	pandoc $< -o $@ -s --css=$(CSS)

clean:
	rm -rf weblog/*.html weblog/*/

.PHONY: all clean
