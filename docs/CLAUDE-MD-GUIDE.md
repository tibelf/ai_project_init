# How to Write a Good CLAUDE.md

## Principles

### Progressive Disclosure
Put the most important information first. Structure from essential to detailed:
1. One-sentence project description
2. Key commands (build, test, dev)
3. Architecture overview
4. Directory structure
5. Key files and their purposes
6. Development patterns and conventions

### Only Include What Claude Doesn't Already Know
- **DO**: Project-specific conventions, non-standard commands, architectural decisions
- **DON'T**: Generic advice like "write clean code" or "handle errors properly"

### Be Specific, Not Vague
- **DO**: `npm run dev` starts the dev server on port 3000
- **DON'T**: "Use the standard development workflow"

### Keep It Concise
- Aim for < 200 lines for simple projects
- Use tables for structured information (key files, CLI args)
- Link to separate docs for detailed topics (`.claude/docs/`)

## Template Structure

```markdown
# CLAUDE.md

## Project Overview
One sentence about what this project does.

## Key Commands
\`\`\`bash
npm run dev      # Start development server
npm run build    # Production build
npm test         # Run tests
\`\`\`

## Architecture
- **Framework**: Next.js 14 with App Router
- **Database**: PostgreSQL via Prisma
- **Auth**: NextAuth.js

## Key Files
| File | Purpose |
|------|---------|
| `src/app/layout.tsx` | Root layout with providers |
| `src/lib/db.ts` | Database client singleton |

## Development Patterns
- Server Components by default, Client Components only when needed
- API routes in `src/app/api/`
```

## Multi-layer Architecture

Claude Code reads CLAUDE.md files at multiple levels:

1. `~/.claude/CLAUDE.md` — Global rules (all projects)
2. `./CLAUDE.md` — Project-specific rules
3. `./.claude/CLAUDE.md` — Additional project rules

The global CLAUDE.md should contain universal coding standards.
Project CLAUDE.md should contain project-specific information only.

## Refactoring Existing CLAUDE.md

Use the `/refactor-CLAUDE` command to:
1. Find contradictions
2. Extract essentials for root CLAUDE.md
3. Group remaining instructions into categories
4. Create modular file structure under `.claude/docs/`
5. Flag redundant or obvious instructions for removal
