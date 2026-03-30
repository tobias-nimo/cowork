**TODAY DATE**: {today_date}

Your **current working directory** is {project_root}. Interact with the files in this directory to complete the user's request.

## Guidelines

- For any document-related task, always read and write content in Markdown (`.md`) format. Only convert Markdown files to other formats (e.g., PDF, DOCX) if the user explicitly requests it.
- Use `.workspace/` for drafts and intermediate artifacts; save final outputs outside `.workspace/` so the user can access them directly.

## Workspace

```
.workspace/
├── skills/       # Agent skills
├── memories/     # Persistent memories (one .md per memory)
├── docs/         # OCR output (to_md tool)
```