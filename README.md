# Obsidian Graph Reasoner

A reasoning engine for Obsidian knowledge graphs that automatically infers new relationships and enriches your knowledge base.

## 🏗️ Architecture

The system follows a clean, modular architecture:

```
src/
├── obsidian_reasoner/          # Core reasoning engine
│   ├── extractor.py            # Extract facts from Obsidian vault
│   ├── reasoner.py             # Apply inference rules
│   ├── persister.py            # Write discoveries back to vault
│   └── models.py               # Data models (Fact, etc.)
├── cli/                        # Command-line interface
│   ├── analyze.py              # Analyze and display inferences
│   └── persist.py              # Persist discoveries to vault
└── importers/                  # External data importers
    └── wikidata.py             # Import from Wikidata
```

## ✨ Features

- **Automatic Fact Extraction**: Parses YAML frontmatter from Obsidian markdown files
- **Logical Reasoning**: Applies 6 inference rules to discover new relationships:
  1. Transitive parent relationships (ANCESTOR_OF)
  2. Transitive part-of relationships
  3. Contribution tracking (created X → part of Y → contributed to Y)
  4. Indirect usage chains
  5. Domain encompassing
  6. Theory application tracking

- **Automated Discovery Persistence**: Writes inferred facts back to your Obsidian vault
- **CI/CD Integration**: GitHub Actions automatically runs reasoning when you add new notes

## 🚀 Quick Start

### Installation

```bash
# Install dependencies
pip install -r requirements.txt

# Install the package (optional)
pip install -e .
```

### Usage

#### Analyze your knowledge graph

```bash
python src/cli/analyze.py
```

This will:
1. Extract all facts from your Obsidian vault (`graph/` directory)
2. Apply reasoning rules to infer new relationships
3. Display statistics and insights about your knowledge graph

#### Persist discoveries back to your vault

```bash
python src/cli/persist.py
```

This will:
1. Run the reasoner
2. Write inferred facts back to your markdown files as YAML frontmatter
3. Add `inferred_by: reasoner` metadata to track automated discoveries

### Example

Given these facts in your Obsidian vault:

```yaml
---
parent: [[Causal Inference]]
---
# Propensity Score Matching
```

```yaml
---
created_by: [[Donald Rubin]]
---
# Propensity Score Matching
```

The reasoner will infer:
- `Donald Rubin CONTRIBUTED_TO Causal Inference`

## 🔄 Automated Workflow

The GitHub Actions workflow (`.github/workflows/reasoning-workflow.yml`) automatically:

1. **Triggers** when you push new `.md` files to the `graph/` directory
2. **Analyzes** your knowledge graph
3. **Persists** new discoveries
4. **Commits** the enriched files back to your repository

This means your Obsidian vault on GitHub stays synchronized with inferred knowledge!

## 📊 Supported Relationships

### Input Relations (from YAML frontmatter)

- `parent`: Creates PARENT_OF relationship
- `type_model`: Creates IS_A relationship
- `part_of`: Creates PART_OF relationship
- `uses`: Creates USES relationship
- `created_by`: Creates CREATED relationship
- `field`: Creates WORKS_IN relationship
- `used_for`: Creates USED_FOR relationship

### Inferred Relations

- `ANCESTOR_OF`: Transitive parent relationships
- `TRANSITIVELY_PART_OF`: Transitive part-of chains
- `CONTRIBUTED_TO`: Creator contributed to larger system
- `INDIRECTLY_USES`: Transitive usage chains
- `DOMAIN_ENCOMPASSES`: Domain coverage through hierarchy
- `THEORY_APPLIED_BY`: Theory application tracking

## 🧪 Testing

```bash
# Run the analyzer on the example knowledge base
python src/cli/analyze.py

# Test persistence (dry run recommended first)
python src/cli/persist.py
```

## 📁 Project Structure

```
.
├── .github/
│   └── workflows/
│       └── reasoning-workflow.yml    # GitHub Actions automation
├── src/
│   ├── obsidian_reasoner/            # Core modules
│   ├── cli/                          # CLI commands
│   └── importers/                    # Data importers
├── graph/                            # Your Obsidian vault
│   └── CausalInference/              # Example: Causal inference knowledge
├── requirements.txt                  # Python dependencies
├── setup.py                          # Package configuration
└── README.md                         # This file
```

## 🎯 Computational Ontology

This project follows a computational ontology design documented in Grafo:
- **Document**: `graphandmodel_computational_ontology`
- **IRI**: `http://www.graphandmodel.io/ontology`

Key architectural principles:
- No orphan entity nodes
- All relationships have attributes
- All entities have properties
- Modular separation: extraction → reasoning → persistence

## 🛠️ Development

### Adding New Inference Rules

Edit `src/obsidian_reasoner/reasoner.py` and add your rule method to the `GraphReasoner` class:

```python
def _rule_my_custom_rule(self, indexes: Dict) -> Set[tuple]:
    """Your custom reasoning rule."""
    inferred = set()
    # Your logic here
    return inferred
```

Then register it in `__init__`:

```python
self.rules = [
    # ... existing rules
    self._rule_my_custom_rule,
]
```

### Adding New Relationship Types

1. Update `RELATION_MAPPINGS` in `src/obsidian_reasoner/extractor.py`
2. Update `RELATION_TO_KEY` in `src/obsidian_reasoner/persister.py`

## 📝 License

MIT License - See LICENSE file for details

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 🔗 Related Projects

- [Obsidian](https://obsidian.md/) - The knowledge base application
- [Grafo](https://gra.fo/) - Computational ontology platform
