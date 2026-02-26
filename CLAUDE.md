# CLAUDE.md

This file provides global guidance to Claude Code across all projects.

## Communication

- Respond in the same language as the user's message
- Be concise and direct
- Do not add unnecessary comments, docstrings, or type annotations to code you didn't change

## Code Quality

- Prefer editing existing files over creating new ones
- Keep solutions simple — avoid over-engineering
- Only make changes that are directly requested or clearly necessary
- Do not add features, refactor code, or make "improvements" beyond what was asked

## Git Workflow

- Create meaningful commit messages that explain "why" not "what"
- Never commit sensitive files (.env, credentials, API keys)
- Prefer creating new commits over amending existing ones
- Stage specific files rather than using `git add -A`

## Testing

- Run existing tests after making changes to verify nothing is broken
- Write tests when adding new functionality

## Architecture

- Follow existing patterns and conventions in the codebase
- Check for existing utilities before creating new ones
- Use the project's established naming conventions
