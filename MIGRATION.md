# Migration Guide

This document explains the reorganization of the codebase and how to migrate from the old structure to the new one.

## What Changed?

### Old Structure
```
.
├── analyze_scm_reasoning.py        # Monolithic script
├── persist_discoveries.py          # Duplicate code
├── obsidian_graph_reasoner.py      # Broken (semantica dependency)
└── wikidata_scm_importer.py        # Importer at root
```

### New Structure
```
.
├── src/
│   ├── obsidian_reasoner/          # Core library
│   │   ├── extractor.py
│   │   ├── reasoner.py
│   │   ├── persister.py
│   │   └── models.py
│   ├── cli/                        # CLI commands
│   │   ├── analyze.py
│   │   └── persist.py
│   └── importers/                  # Importers
│       └── wikidata.py
├── .github/workflows/              # CI/CD
│   └── reasoning-workflow.yml
└── setup.py                        # Package config
```

## Key Improvements

### 1. **Code Deduplication**
- `extract_facts_from_vault()` and `infer_facts()` were duplicated across files
- Now centralized in `extractor.py` and `reasoner.py`

### 2. **Modular Architecture**
- Separation of concerns: extraction, reasoning, persistence
- Each module has a single responsibility
- Easy to test and extend

### 3. **Removed Broken Dependencies**
- Removed dependency on `semantica` (non-existent library)
- `obsidian_graph_reasoner.py` was not functional

### 4. **Proper Python Package**
- Added `setup.py` for installable package
- Proper module structure with `__init__.py` files
- Entry points for CLI commands

### 5. **GitHub Actions Integration**
- Automated workflow on new file additions
- No manual script execution needed

## Migration Instructions

### If you were using the old scripts:

**Old way:**
```bash
python analyze_scm_reasoning.py
python persist_discoveries.py
```

**New way:**
```bash
python src/cli/analyze.py
python src/cli/persist.py
```

Or install the package and use entry points:
```bash
pip install -e .
obsidian-analyze
obsidian-persist
```

### If you were importing modules:

**Old imports (broken):**
```python
from obsidian_graph_reasoner import ObsidianGraphReasoner
```

**New imports:**
```python
from src.obsidian_reasoner import ObsidianFactExtractor, GraphReasoner, DiscoveryPersister
```

### If you had custom scripts:

Update your imports and use the new modular API:

```python
from pathlib import Path
from src.obsidian_reasoner import ObsidianFactExtractor, GraphReasoner, DiscoveryPersister

# Extract facts
vault_path = Path("graph")
extractor = ObsidianFactExtractor(vault_path)
facts = extractor.extract_facts()

# Run reasoning
reasoner = GraphReasoner()
inferred = reasoner.infer(facts)

# Persist discoveries
persister = DiscoveryPersister(vault_path)
stats = persister.persist(inferred)
```

## Backward Compatibility

The old scripts (`analyze_scm_reasoning.py`, `persist_discoveries.py`) have been kept temporarily but are now considered **deprecated**. They will be removed in a future version.

**Action Required:** Update your scripts and workflows to use the new structure.

## Troubleshooting

### Issue: Import errors

**Problem:**
```
ModuleNotFoundError: No module named 'semantica'
```

**Solution:** The old `obsidian_graph_reasoner.py` is deprecated. Use the new modules:
```python
from src.obsidian_reasoner import ObsidianFactExtractor, GraphReasoner
```

### Issue: Scripts not found

**Problem:**
```
python analyze_scm_reasoning.py
# Can't find file
```

**Solution:** Use the new CLI location:
```bash
python src/cli/analyze.py
```

### Issue: GitHub Actions not triggering

**Problem:** Workflow doesn't run when adding new markdown files.

**Solution:**
1. Ensure the workflow file is committed: `.github/workflows/reasoning-workflow.yml`
2. Check that changes are in the `graph/` directory
3. Push to the `main` branch

## Benefits of the New Structure

1. **Maintainable**: Clear separation of concerns
2. **Testable**: Each module can be tested independently
3. **Extensible**: Easy to add new inference rules or relation types
4. **Automated**: GitHub Actions handles everything
5. **Professional**: Follows Python packaging best practices

## Questions?

If you encounter any issues during migration, please:
1. Check the main [README.md](README.md)
2. Review the [REASONER_README.md](REASONER_README.md) for technical details
3. Open an issue on GitHub
