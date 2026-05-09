-- Lua filter to add "На главную" navigation links to blog posts
-- Detects blog posts by checking for YAML frontmatter metadata (title, date, tags, summary)
-- Adds navigation divs at beginning and end of content
-- Uses absolute paths with configurable root URL via site-root-url variable or SITE_ROOT_URL env var

function Pandoc(doc)
  -- Check if this is a blog post by looking for typical blog post metadata
  -- Blog posts have YAML frontmatter with title, date, tags, and/or summary
  local has_title = doc.meta.title ~= nil
  local has_date = doc.meta.date ~= nil
  local has_tags = doc.meta.tags ~= nil
  local has_summary = doc.meta.summary ~= nil
  
  -- Consider it a blog post if it has at least title and date (common pattern)
  -- Or if it has title and tags/summary (some might not have date)
  local is_blog_post = (has_title and has_date) or (has_title and (has_tags or has_summary))
  
  if not is_blog_post then
    return doc
  end
  
  -- Determine the root URL for absolute links
  -- Priority: 1. Pandoc variable site-root-url, 2. Environment variable SITE_ROOT_URL, 3. Default
  local root_url = "https://bakineugene.github.io/"
  
  -- Check Pandoc metadata (passed via --variable site-root-url=...)
  if doc.meta["site-root-url"] then
    root_url = pandoc.utils.stringify(doc.meta["site-root-url"])
  else
    -- Fall back to environment variable
    local env_url = os.getenv("SITE_ROOT_URL")
    if env_url and env_url ~= "" then
      root_url = env_url
    end
  end
  
  -- Ensure root_url ends with a slash for proper URL concatenation
  if not root_url:match("/$") then
    root_url = root_url .. "/"
  end
  
  -- Create the navigation link with absolute URL
  local link = pandoc.Link("На главную", root_url)
  local para = pandoc.Para({link})
  local div = pandoc.Div({para})
  div.classes = {"nav-home"}
  
  -- Get document blocks
  local blocks = doc.blocks
  
  -- Create new blocks array with navigation at beginning and end
  local new_blocks = {}
  
  -- Insert navigation div at the beginning
  table.insert(new_blocks, div)
  
  -- Copy all existing blocks
  for i, block in ipairs(blocks) do
    table.insert(new_blocks, block)
  end
  
  -- Insert navigation div at the end
  table.insert(new_blocks, div)
  
  -- Return modified document
  doc.blocks = new_blocks
  return doc
end