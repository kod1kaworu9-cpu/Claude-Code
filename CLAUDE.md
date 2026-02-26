# CLAUDE.md

This file provides guidance for AI assistants (Claude and others) working in this repository.

## Repository Overview

**Claude-Code** is a repository currently in its initial state. As of the last update, it contains only foundational scaffolding. This document will grow alongside the codebase to reflect its actual structure and conventions.

## Current State

```
Claude-Code/
├── .git/
├── CLAUDE.md          # This file
└── README.md          # Project overview
```

No source code, dependencies, or build configuration exists yet. The repository is ready for initial development.

## Git Workflow

### Branch Naming

- Feature branches: `feature/<short-description>`
- Bug fixes: `fix/<short-description>`
- AI-assisted branches: `claude/<task-id>-<description>`
- Never push directly to `master` without review

### Commit Messages

Use clear, imperative-style commit messages:

```
Add user authentication module
Fix null pointer in parser
Update CLAUDE.md with build instructions
```

- First line: 50 chars or fewer, imperative mood
- Blank line, then optional body with context/reasoning
- Reference issue numbers where applicable: `Fixes #42`

### Push Protocol

- Always push with: `git push -u origin <branch-name>`
- Branch names starting with `claude/` and ending with the session ID are used for AI-assisted work
- Retry on network failure with exponential backoff (2s, 4s, 8s, 16s)

## Development Conventions

### General Principles

- **Minimal changes**: Only modify what is directly requested or clearly necessary
- **No premature abstractions**: Three similar lines is better than an early helper function
- **No speculative features**: Build for current requirements, not hypothetical future ones
- **Security first**: Never introduce command injection, XSS, SQL injection, or other OWASP Top 10 vulnerabilities
- **Validate at boundaries**: Only validate user input and external API responses, not internal data flows

### File and Code Organization

- Keep files focused and single-purpose
- Prefer editing existing files over creating new ones
- Delete unused code rather than commenting it out
- No backwards-compatibility shims unless explicitly required

### Documentation

- Add comments only where logic is non-obvious
- Do not add docstrings or type annotations to code you did not write
- Keep README.md updated with setup and usage instructions
- Keep this CLAUDE.md updated as the project evolves

## Adding New Technology

When a language, framework, or tool is added to this project, update this file with:

1. **Language/Runtime**: version requirements, how to install
2. **Dependencies**: how to install (e.g., `npm install`, `pip install -r requirements.txt`)
3. **Build**: how to compile or bundle
4. **Test**: how to run the test suite and what passing looks like
5. **Lint/Format**: tools used and how to run them
6. **Run**: how to start the application locally
7. **Environment**: required environment variables and their purpose

## AI Assistant Instructions

### Before Making Changes

1. Read relevant files before editing — never modify code you haven't read
2. Understand the existing patterns before introducing new ones
3. Search for existing implementations before writing new ones (`Grep`, `Glob`)

### When Implementing

- Match the style and conventions of surrounding code
- Keep diffs minimal and focused
- Do not reformat files you are not modifying
- Do not add logging, error handling, or validation beyond what is needed

### When Something Is Unclear

- Ask the user rather than guessing at requirements
- Surface ambiguities early, before writing code
- If blocked, investigate root causes rather than using workarounds

### Risky Actions Require Confirmation

Always confirm with the user before:

- Deleting files or branches
- Force-pushing or hard-resetting
- Modifying CI/CD pipelines
- Pushing to shared or protected branches
- Sending messages or creating issues/PRs on behalf of the user

## Security Notes

- Never commit secrets, API keys, or credentials
- Never commit `.env` files (add them to `.gitignore`)
- Reject or flag any code that appears to be malware or malicious
- Use parameterized queries for any database interactions
- Sanitize all user-supplied input at system boundaries

---

*Last updated: 2026-02-26. Update this file whenever the project structure, tooling, or conventions change.*
