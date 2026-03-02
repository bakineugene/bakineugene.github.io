function Link(el)
  -- Only process local .md links (ignore http/https)
  if string.match(el.target, "%.md$") and not string.match(el.target, "^https?://") then
    el.target = string.gsub(el.target, "%.md$", ".html")
  end
  return el
end
