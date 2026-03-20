---
name: memory
description: Use this skill to persist and recall information across conversations using the .workspace/memories/ directory
---

# Memory Skill

This skill provides a file-based memory system for persisting important information across conversations. Memories are stored as individual markdown files in `.workspace/memories/`.

## When to Use This Skill

- The user explicitly asks you to **remember** something
- The user asks you to **recall** or **check** something from a previous conversation
- You learn important context that would be valuable in future conversations (user preferences, project decisions, key contacts, recurring workflows)

## Memory Format

Each memory is a standalone markdown file in `.workspace/memories/` with YAML frontmatter:

```markdown
---
name: short-descriptive-name
type: user | project | reference | feedback
---

Content of the memory.
```

### Memory Types

| Type | What to store | Example |
|------|--------------|---------|
| `user` | User role, preferences, expertise, working style | "User is a backend engineer, prefers concise responses" |
| `project` | Ongoing work, decisions, deadlines, goals | "Auth migration blocked until Q2 security review completes" |
| `reference` | Pointers to external resources and their purpose | "Design specs are in the shared Drive folder 'Project X Specs'" |
| `feedback` | Corrections or confirmations about how to approach work | "User wants draft emails in bullet-point format, not prose" |

## How to Save a Memory

1. Check if a related memory already exists by listing files in `.workspace/memories/`
2. If updating, edit the existing file. If new, create a file named `<type>_<topic>.md`
3. Keep memories **concise and actionable** — one idea per file

**Example:**

```markdown
---
name: user-communication-style
type: feedback
---

User prefers short, direct emails. No greetings or sign-offs unless the recipient is external.
```

## How to Recall Memories

When a task might benefit from prior context:

1. List files in `.workspace/memories/` to see what's available
2. Read relevant memory files based on their names
3. Apply the context to your current task

## What NOT to Save

- Information that can be derived from files in the current project
- Temporary or in-progress task details (use a todo list instead)
- Verbatim copies of documents or code
- Sensitive credentials or API keys

## Guidelines

- **One memory per file** — easier to find, update, and delete
- **Use clear file names** — `feedback_email_style.md` not `mem_001.md`
- **Keep memories current** — update or delete memories that are no longer accurate
- **Ask before saving** if you're unsure whether something is worth remembering
- **Convert relative dates** to absolute dates when saving (e.g. "next Monday" → "2026-03-23")
