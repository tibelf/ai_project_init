# Skills Guide

## Bundled Skills (included in this repo)

| Skill | Description |
|-------|-------------|
| `vercel-react-best-practices` | 45+ React/Next.js performance optimization rules from Vercel Engineering |
| `web-design-guidelines` | UI code review against Web Interface Guidelines |
| `xiaohongshu-note-writer` | 小红书产品推荐笔记写作 |
| `commit-with-docs` | Commit with documentation updates |
| `add-api` | API route scaffolding with template assets |
| `generate-claude-md` | Intelligently generate CLAUDE.md for any project |

## External Skills (installed via `claude skill add`)

| Skill | Install Command | Description |
|-------|----------------|-------------|
| `agent-browser` | `claude skill add agent-browser` | Browser automation CLI for AI agents |
| `find-skills` | `claude skill add find-skills` | Discover and install agent skills |
| `kipper-frontend-design` | `claude skill add kipper-frontend-design` | Production-grade frontend UI design |
| `remotion-best-practices` | `claude skill add remotion-best-practices` | Remotion video creation in React |
| `seo-audit` | `claude skill add seo-audit` | SEO audit and diagnostics |
| `skill-creator` | `claude skill add skill-creator` | Guide for creating new skills |
| `composio` | `claude skill add composio` | Composio integration (Twitter API etc.) |
| `firecrawl` | `claude skill add firecrawl` | Firecrawl web scraping |

## Creating Your Own Skills

Each skill needs a `SKILL.md` file with frontmatter:

```markdown
---
name: my-skill
description: What this skill does
argument-hint: [optional-args]
---

# Skill Title

Instructions for Claude Code when this skill is invoked...
```

Place the skill directory in `skills/` and run `./manage.sh → Add` to register it.
