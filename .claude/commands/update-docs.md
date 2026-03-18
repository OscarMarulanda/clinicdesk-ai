# Update Documentation

After completing any implementation work, review and update the project documentation to reflect what was built.

## Checklist

1. **`docs/CHECKLIST.md`** — Mark completed tasks, add any new tasks discovered during implementation
2. **`docs/PROGRESS.md`** — Add an entry for what was just completed, note any deviations from the original plan and why
3. **`docs/ARCHITECTURE.md`** — Update if any architectural changes were made (new components, changed data flow, added/removed services)
4. **`docs/ADR/`** — Create a new ADR if a significant technical decision was made during this work
5. **`docs/DATABASE.md`** — Update if schema changed (new tables, columns, indexes, migrations)
6. **`docs/API_SPEC.md`** — Update if endpoints were added, changed, or removed
7. **`docs/AGENT_DESIGN.md`** — Update if system prompt, tools, or escalation logic changed
8. **`docs/SETUP.md`** — Update if new dependencies, env vars, or setup steps were added

## How to update

- Read each doc that might be affected
- Make precise, minimal updates — don't rewrite sections that haven't changed
- In PROGRESS.md, include: date, what was done, what changed from plan (if anything), what's next
- In CHECKLIST.md, use `[x]` for completed items and add new items under appropriate sections if scope expanded

## Version checks

Before updating docs, also verify:
- Are we using the latest stable versions of all dependencies?
- If a dependency was added or upgraded, note the version in SETUP.md
- Check for any deprecation warnings encountered during implementation
