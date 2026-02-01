# Troubleshooting Guide

This document tracks problems encountered and their solutions for future reference.

---

## GitHub Actions: Git Rebase Conflict Error

**Date:** 2026-02-02

### Problem

The `reasoning-workflow.yml` GitHub Action was failing with:
```
error: cannot pull with rebase: You have unstaged changes.
error: Please commit or stash them.
Rebase failed, attempting merge strategy
fatal: no rebase in progress
Error: Process completed with exit code 128.
```

### Root Cause

The `.obsidian/` directory (containing Obsidian editor settings) was being tracked by Git even though it was listed in `.gitignore`. This happened because:

1. The files were added to Git before being added to `.gitignore` (`.gitignore` only affects untracked files)
2. When the workflow ran, it only staged graph markdown files: `git add graph/**/*.md`
3. Obsidian settings files (`.obsidian/workspace.json`, etc.) were modified locally but not staged
4. The unstaged changes blocked `git pull --rebase`, causing the workflow to fail

### Solution

**Two-part fix:**

1. **Removed `.obsidian/` from Git tracking:**
   ```bash
   git rm -r --cached .obsidian/
   ```
   This removes the files from Git tracking while keeping them on disk.

2. **Updated workflow to handle unstaged changes:**
   ```yaml
   # Stash any remaining unstaged changes before pulling
   git stash --include-untracked --keep-index || echo "Nothing to stash"

   # Pull with rebase
   git pull --rebase origin main || {
     echo "Rebase failed, attempting merge strategy"
     git rebase --abort
     git pull --no-rebase origin main
   }

   git push

   # Pop stashed changes back (they remain local)
   git stash pop || echo "No stash to pop"
   ```

### Key Insights

- **`.gitignore` doesn't affect tracked files:** Once files are in Git history, adding them to `.gitignore` won't remove them from tracking. Use `git rm --cached` to untrack.
- **Workflow robustness:** Use `git stash` to temporarily store unstaged changes before pulling, preventing rebase conflicts from blocking automated workflows.
- **Concurrent modifications:** When workflows and local editors (like Obsidian) modify files simultaneously, use selective staging (`git add specific/paths`) and stash management to handle conflicts gracefully.

### References

- Commit: `0d01d23` - Fix GitHub Actions workflow git conflict error
- File: `.github/workflows/reasoning-workflow.yml`
- Related: CLAUDE.md "GitHub Actions Workflow Robustness" section

---
