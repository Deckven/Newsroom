---
name: obsidian
description: >
  Manage Obsidian vault — read, create, edit, and search notes; manage tags and frontmatter;
  work with wikilinks and backlinks; generate MOC (Map of Content).
  This skill should be used when the user wants to interact with their Obsidian vault directly:
  reading notes, creating or editing notes, searching by content/tags/folders,
  managing tags, finding backlinks, or building Maps of Content.
---

# Obsidian Vault Manager

Vault path: `C:/ObsidianDataStorage`

## Vault Conventions

- Notes are `.md` files with optional YAML frontmatter delimited by `---`
- Frontmatter fields: `title`, `tags`, `date`, `created`, `modified`, `aliases`, `status`, custom keys
- Tags appear in frontmatter (`tags: [a, b]`) or inline (`#tagname`)
- Wikilinks: `[[Note Name]]` or `[[Note Name|Display Text]]`
- Folder names may contain `!` prefix and parenthetical labels like `(1st SubL)`

## Operations

### 1. Read Notes

**By name or path:**
Use the Read tool with the full path: `C:/ObsidianDataStorage/<folder>/<note>.md`

**By folder:**
Use Glob to list notes in a folder:
- Pattern: `<folder>/**/*.md` for recursive, `<folder>/*.md` for flat
- Path: `C:/ObsidianDataStorage`

**Parse frontmatter:** Extract YAML between the first `---` pair. The body starts after the closing `---`.

### 2. Create Notes

Use the Write tool. Always include YAML frontmatter:

```markdown
---
title: Note Title
date: YYYY-MM-DD
tags: [tag1, tag2]
---

# Note Title

Content here.
```

**File naming:** Use descriptive kebab-case or space-separated names matching vault conventions. Place in the appropriate subfolder based on content domain.

### 3. Edit Notes

Use the Read tool first, then Edit tool for targeted changes. Preserve existing frontmatter fields unless explicitly asked to modify them. When editing frontmatter, maintain valid YAML syntax.

### 4. Search Notes

**By content:** Use Grep with path `C:/ObsidianDataStorage` to search note bodies.

**By filename:** Use Glob with path `C:/ObsidianDataStorage` and pattern `**/*<query>*.md`.

**By tags:** Use Grep to find notes containing a tag:
- Frontmatter tags: search for pattern `tags:.*\b<tagname>\b` or `- <tagname>`
- Inline tags: search for `#<tagname>`

**By frontmatter field:** Use Grep for `<field>: <value>` within the vault path.

### 5. Manage Tags

**Add a tag to a note:**
1. Read the note
2. If frontmatter has `tags:` as a list, append the new tag
3. If frontmatter has `tags:` as a string, convert to list and append
4. If no `tags:` field, add it to frontmatter
5. Use Edit to apply the change

**Remove a tag from a note:**
1. Read the note
2. Remove the tag from the `tags:` list/string in frontmatter
3. Optionally remove inline `#tagname` occurrences if requested
4. Use Edit to apply the change

**Bulk tag operations:**
1. Use Grep to find all notes with the target tag
2. Process each note individually using the add/remove logic above
3. Report the count of modified notes

### 6. Wikilinks and Backlinks

**Find outgoing links from a note:**
Read the note and extract all `[[...]]` patterns.

**Find backlinks to a note:**
Use Grep to search the entire vault for `[[Note Name]]` or `[[Note Name|`. The search pattern: `\[\[<Note Name>(\||\]\])`.

**Resolve broken links:**
1. Extract all wikilinks from a note (or set of notes via Grep)
2. For each link target, use Glob to check if `**/<target>.md` exists
3. Report links that have no matching file

### 7. Map of Content (MOC)

Generate a MOC note that aggregates wikilinks to related notes.

**By folder:**
1. Use Glob to list all `.md` files in the target folder
2. For each file, extract the title (frontmatter `title` or first `# H1` or filename stem)
3. Write a MOC note with wikilinks grouped logically

**By tag:**
1. Use Grep to find all notes with the target tag
2. Extract titles and build wikilinks
3. Write the MOC note

**MOC format:**
```markdown
---
title: "MOC: <Topic>"
date: <today>
tags: [MOC]
---

# <Topic> — Map of Content

## Notes

- [[Note One]] — brief description if available
- [[Note Two]]
- [[Note Three]]
```

## Response Guidelines

- When listing notes, show filename, title (from frontmatter or H1), and tags
- When showing note content, include frontmatter summary (tags, date) before the body
- For search results, show matched line with surrounding context
- For bulk operations, confirm the scope before executing and report results
- Preserve vault structure — do not reorganize folders unless explicitly asked
- Use forward slashes in paths for consistency
