# Troubleshooting Guide

This document contains solutions to common problems encountered during development and usage.

## Code Reorganization (February 2026)

### Problem: Duplicate code across analyze_scm_reasoning.py and persist_discoveries.py

**Issue:** The `extract_facts_from_vault()` and `infer_facts()` functions were duplicated in both files, making maintenance difficult.

**Solution:**
1. Created modular architecture with separate concerns:
   - `src/obsidian_reasoner/extractor.py` - Fact extraction
   - `src/obsidian_reasoner/reasoner.py` - Inference engine
   - `src/obsidian_reasoner/persister.py` - Discovery persistence
   - `src/obsidian_reasoner/models.py` - Data models

2. Refactored old scripts to use new modules in `src/cli/`

**Files changed:**
- Created: `src/obsidian_reasoner/` package
- Created: `src/cli/analyze.py`, `src/cli/persist.py`
- Deprecated: `analyze_scm_reasoning.py`, `persist_discoveries.py`

---

### Problem: obsidian_graph_reasoner.py imports non-existent 'semantica' library

**Issue:** The old reasoner implementation depended on a `semantica` library that doesn't exist or isn't available.

**Solution:**
1. Removed dependency on `semantica`
2. Implemented custom reasoning engine in `src/obsidian_reasoner/reasoner.py`
3. Reasoning rules are now self-contained with no external dependencies

**Files changed:**
- Removed: `semantica` from `requirements.txt`
- Created: `src/obsidian_reasoner/reasoner.py` with 6 built-in inference rules
- Deprecated: `obsidian_graph_reasoner.py`

---

## GitHub Actions

### Problem: Workflow not triggering on new markdown files

**Symptoms:** Adding new `.md` files to the `graph/` directory doesn't trigger the workflow.

**Possible causes:**
1. Workflow file not committed to repository
2. Changes pushed to wrong branch
3. Incorrect path pattern in workflow

**Solution:**
```bash
# 1. Ensure workflow is committed
git add .github/workflows/reasoning-workflow.yml
git commit -m "Add reasoning workflow"
git push

# 2. Check you're on the main branch
git branch --show-current

# 3. Verify path pattern matches your structure
# Edit .github/workflows/reasoning-workflow.yml if needed:
on:
  push:
    paths:
      - 'graph/**/*.md'  # Adjust if your vault is elsewhere
```

---

### Problem: GitHub Actions fails with "Permission denied"

**Symptoms:** Workflow runs but fails when trying to commit changes back.

**Solution:**
1. Ensure `GITHUB_TOKEN` has write permissions
2. In your repository settings:
   - Go to Settings → Actions → General
   - Under "Workflow permissions", select "Read and write permissions"
   - Save

---

## Python Package Issues

### Problem: ModuleNotFoundError when importing obsidian_reasoner

**Symptoms:**
```python
from src.obsidian_reasoner import ObsidianFactExtractor
ModuleNotFoundError: No module named 'src'
```

**Solution:**

**Option 1:** Install the package in development mode:
```bash
pip install -e .
```

**Option 2:** Add the project root to your Python path:
```python
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.obsidian_reasoner import ObsidianFactExtractor
```

**Option 3:** Run scripts from the project root:
```bash
# From project root directory
python src/cli/analyze.py
```

---

### Problem: YAML parsing errors

**Symptoms:**
```
yaml.scanner.ScannerError: mapping values are not allowed here
```

**Solution:**
1. Check your markdown frontmatter format:
```yaml
---
parent: [[Entity Name]]
type_model: [[Type]]
---
```

2. Ensure no tabs in YAML (use spaces only)
3. Validate YAML syntax: https://www.yamllint.com/

---

## Reasoning Engine

### Problem: No facts extracted from vault

**Symptoms:** `Extracted 0 facts` when running analyzer.

**Possible causes:**
1. Vault path is incorrect
2. No YAML frontmatter in markdown files
3. Frontmatter keys don't match expected format

**Solution:**
```bash
# 1. Check vault path
ls -la graph/  # Should show your markdown files

# 2. Verify frontmatter format
head -20 graph/CausalInference/some-file.md

# 3. Ensure frontmatter uses recognized keys:
# parent, type_model, part_of, uses, created_by, field, used_for
```

---

### Problem: Inferred facts not appearing in files

**Symptoms:** `persist.py` runs successfully but no changes in markdown files.

**Possible causes:**
1. No new facts to infer
2. Target entities don't have corresponding files
3. Files lack proper YAML frontmatter

**Solution:**
```bash
# 1. Run analyzer to see what was inferred
python src/cli/analyze.py

# 2. Check that entity names match filenames
# If reasoner infers "Judea Pearl CONTRIBUTED_TO Causality",
# there must be files: "Judea Pearl.md" and "Causality.md"

# 3. Ensure files have YAML frontmatter (even if empty)
# Add to top of file:
---
---
```

---

## Development

### Problem: Changes to reasoning rules not reflected

**Symptoms:** Modified `reasoner.py` but behavior hasn't changed.

**Solution:**
1. If package is installed, reinstall:
```bash
pip install -e . --force-reinstall --no-deps
```

2. Or run scripts directly without installing:
```bash
python src/cli/analyze.py
```

3. Check you're editing the right file:
```bash
# Should be in src/obsidian_reasoner/reasoner.py
# NOT the old analyze_scm_reasoning.py
```

---

### Problem: Git conflicts when workflow commits

**Symptoms:** Merge conflicts in markdown files after workflow runs.

**Solution:**
1. Pull before adding new files:
```bash
git pull origin main
# Add your new markdown files
git add graph/
git commit -m "Add new notes"
git push
```

2. If conflicts occur, resolve manually:
```bash
git pull
# Fix conflicts in affected files
git add .
git commit -m "Resolve conflicts"
git push
```

---

## Best Practices to Avoid Issues

1. **Always run from project root:** `python src/cli/analyze.py`
2. **Keep entity names consistent:** Filename must match entity name in relationships
3. **Use proper YAML frontmatter:** Start files with `---` delimiter
4. **Pull before push:** Avoid conflicts with automated commits
5. **Test locally first:** Run `analyze.py` before `persist.py`

---

## Still Having Issues?

1. Check the [README.md](README.md) for usage instructions
2. Review the [MIGRATION.md](MIGRATION.md) if upgrading from old structure
3. Consult the [REASONER_README.md](REASONER_README.md) for technical details
4. Open an issue on GitHub with:
   - Error message
   - Steps to reproduce
   - Output of `python --version` and `pip list`
