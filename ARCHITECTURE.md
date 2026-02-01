# Architecture Documentation

## System Overview

The Obsidian Graph Reasoner is a knowledge graph reasoning system that automatically extracts facts from Obsidian markdown files, applies logical inference rules, and persists discoveries back to the vault.

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                     GitHub Actions Workflow                     │
│                  (Automated CI/CD Orchestration)                │
└────────────────────────────┬────────────────────────────────────┘
                             │ triggers on: push *.md
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Obsidian Graph Reasoner                      │
│                                                                 │
│  ┌──────────────────┐    ┌──────────────────┐    ┌──────────┐ │
│  │ ObsidianFact     │───▶│  GraphReasoner   │───▶│Discovery │ │
│  │ Extractor        │    │   (6 rules)      │    │Persister │ │
│  └──────────────────┘    └──────────────────┘    └──────────┘ │
│         │                         │                      │     │
│         │ extracts                │ infers               │     │
│         ▼                         ▼                      ▼     │
│    ┌─────────┐              ┌─────────┐           ┌─────────┐ │
│    │  Facts  │─────────────▶│ Facts   │──────────▶│ Updated │ │
│    │ (List)  │   input      │(+inferred)│ output  │  Vault  │ │
│    └─────────┘              └─────────┘           └─────────┘ │
└─────────────────────────────────────────────────────────────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │ Obsidian Vault  │
                    │   (graph/*.md)  │
                    │  YAML frontmatter│
                    └─────────────────┘
```

## Component Hierarchy

```
src/
├── obsidian_reasoner/              Core reasoning library
│   ├── models.py                   Data structures
│   │   └── Fact(relation, subject, object)
│   ├── extractor.py                Fact extraction
│   │   └── ObsidianFactExtractor
│   │       ├── extract_facts() → List[Fact]
│   │       └── find_markdown_file(entity) → Path
│   ├── reasoner.py                 Inference engine
│   │   └── GraphReasoner
│   │       ├── infer(facts) → List[Fact]
│   │       └── _rule_* (6 inference rules)
│   └── persister.py                Discovery persistence
│       └── DiscoveryPersister
│           └── persist(facts) → Stats
│
├── cli/                            Command-line interface
│   ├── analyze.py                  Analysis CLI
│   └── persist.py                  Persistence CLI
│
└── importers/                      External data importers
    └── wikidata.py                 Wikidata SPARQL importer
```

## Data Flow

### 1. Extraction Phase

```
Obsidian Vault (*.md files)
        │
        │ YAML frontmatter parsing
        ▼
ObsidianFactExtractor
        │
        │ Maps keys to relations:
        │   parent → PARENT_OF
        │   uses → USES
        │   created_by → CREATED
        │   ...
        ▼
List[Fact(relation, subject, object)]
```

### 2. Reasoning Phase

```
List[Fact] (extracted)
        │
        ▼
GraphReasoner.infer()
        │
        ├──▶ Rule 1: Transitive PARENT_OF → ANCESTOR_OF
        ├──▶ Rule 2: Transitive PART_OF
        ├──▶ Rule 3: CREATED + PART_OF → CONTRIBUTED_TO
        ├──▶ Rule 4: USES + USES → INDIRECTLY_USES
        ├──▶ Rule 5: PARENT_OF + PART_OF → DOMAIN_ENCOMPASSES
        └──▶ Rule 6: CREATED + USES → THEORY_APPLIED_BY
        │
        ▼
List[Fact] (inferred)
```

### 3. Persistence Phase

```
List[Fact] (inferred)
        │
        ▼
DiscoveryPersister.persist()
        │
        │ Organizes by source entity
        │ Finds corresponding .md files
        │ Maps relation types to YAML keys
        │ Adds inferred_by: reasoner
        ▼
Updated Obsidian Vault
```

## Inference Rules

### Rule 1: Transitive Parent (ANCESTOR_OF)
```
A PARENT_OF B
B PARENT_OF C
─────────────────
A ANCESTOR_OF C
```

### Rule 2: Transitive Part-Of
```
A PART_OF B
B PART_OF C
─────────────────────────
A TRANSITIVELY_PART_OF C
```

### Rule 3: Contribution Tracking
```
Creator CREATED X
X PART_OF Y
──────────────────────
Creator CONTRIBUTED_TO Y
```

### Rule 4: Indirect Usage
```
A USES X
X USES Y
─────────────────────
A INDIRECTLY_USES Y
```

### Rule 5: Domain Encompassing
```
Parent PARENT_OF Child
Child PART_OF Whole
────────────────────────
Parent DOMAIN_ENCOMPASSES Whole
```

### Rule 6: Theory Application
```
Creator CREATED Theory
User USES Theory
──────────────────────────
Creator THEORY_APPLIED_BY User
```

## Relationship Mapping

### Input (YAML frontmatter → Relations)

| YAML Key       | Relation Type | Direction |
|----------------|---------------|-----------|
| `parent`       | PARENT_OF     | Inverted  |
| `type_model`   | IS_A          | Forward   |
| `part_of`      | PART_OF       | Forward   |
| `uses`         | USES          | Forward   |
| `created_by`   | CREATED       | Inverted  |
| `field`        | WORKS_IN      | Forward   |
| `used_for`     | USED_FOR      | Forward   |

### Output (Relations → YAML frontmatter)

| Inferred Relation         | YAML Key                 |
|---------------------------|--------------------------|
| ANCESTOR_OF               | `ancestor_of`            |
| TRANSITIVELY_PART_OF      | `transitively_part_of`   |
| CONTRIBUTED_TO            | `contributed_to`         |
| INDIRECTLY_USES           | `indirectly_uses`        |
| DOMAIN_ENCOMPASSES        | `domain_encompasses`     |
| THEORY_APPLIED_BY         | `theory_applied_by`      |

## GitHub Actions Workflow

```
Event: push (*.md files in graph/)
        │
        ▼
1. Checkout repository
        │
        ▼
2. Set up Python 3.10
        │
        ▼
3. Install dependencies
        │
        ▼
4. Run src/cli/analyze.py
        │
        ▼
5. Run src/cli/persist.py
        │
        ▼
6. Check for changes
        │
        ├── No changes → End
        │
        └── Has changes
                │
                ▼
        7. Commit and push
                │
                ▼
        Updated repository
```

## Computational Ontology

The system architecture is formalized in a Grafo computational ontology:

**Document:** `graphandmodel_computational_ontology`
**IRI:** `http://www.graphandmodel.io/ontology`
**Prefix:** `gm`

### Ontology Graph

```
ObsidianVault
     ▲         ▲
     │         │
     │extracts │persists_to
     │from     │
     │         │
ObsidianFactExtractor ──produces──▶ Fact ◀──infers_from── GraphReasoner
                                     ▲                           ▲
                                     │                           │
                                     │                     orchestrates
                                     │                           │
                              DiscoveryPersister ◀────orchestrates────┘
                                                        │
                                                        │
                                                GitHubActionsWorkflow
```

### Constitutional Principles

1. ✅ **No orphan nodes**: All entities participate in relationships
2. ✅ **Attributed relationships**: All relationships have descriptions
3. ✅ **Entity properties**: All entities have descriptions and IRIs

## Scalability Considerations

### Current Design
- **Files**: Processes all `.md` files in vault
- **Facts**: Holds all facts in memory
- **Inference**: Builds indexes for O(n²) worst case

### Optimization Strategies (Future)

1. **Incremental Processing**
   - Only process changed files
   - Cache previous inference results
   - Detect which rules need re-execution

2. **Parallel Processing**
   - Extract facts from files in parallel
   - Apply independent rules concurrently
   - Batch persistence operations

3. **Graph Database Backend**
   - Store facts in Neo4j or similar
   - Use Cypher for inference queries
   - Support larger knowledge bases

## Extension Points

### Adding New Inference Rules

1. Create method in `GraphReasoner`:
```python
def _rule_my_rule(self, indexes: Dict) -> Set[tuple]:
    inferred = set()
    # Your logic
    return inferred
```

2. Register in `__init__`:
```python
self.rules.append(self._rule_my_rule)
```

### Adding New Relation Types

1. Update `extractor.py`:
```python
RELATION_MAPPINGS = {
    'my_key': ('MY_RELATION', False),
}
```

2. Update `persister.py`:
```python
RELATION_TO_KEY = {
    'MY_RELATION': 'my_key',
}
```

### Custom Importers

Create new importer in `src/importers/`:
```python
class CustomImporter:
    def import_data(self):
        # Fetch from API
        # Create markdown files
        pass
```

## Security Considerations

### YAML Parsing
- Uses `yaml.safe_load()` to prevent code injection
- Only parses frontmatter (not arbitrary YAML files)

### Git Operations
- Workflow uses `GITHUB_TOKEN` for authentication
- Limited to repository write permissions
- Commits are attributed properly

### File System
- Only writes to `graph/` directory
- Validates file paths before writing
- No arbitrary file execution

## Performance Metrics

### Typical Knowledge Base (50 entities, 100 facts)
- **Extraction**: ~0.1 seconds
- **Reasoning**: ~0.05 seconds
- **Persistence**: ~0.2 seconds
- **Total**: ~0.35 seconds

### Large Knowledge Base (500 entities, 1000 facts)
- **Extraction**: ~1 second
- **Reasoning**: ~2 seconds
- **Persistence**: ~3 seconds
- **Total**: ~6 seconds

## Error Handling

### Graceful Degradation
- Skips files with parsing errors
- Continues if some facts fail to persist
- Reports statistics at end

### Logging Strategy (Future)
- Structured logging with levels
- Separate logs for extraction/reasoning/persistence
- Debug mode for troubleshooting

## Testing Strategy (Future)

### Unit Tests
- Test each module independently
- Mock file system operations
- Verify inference rules

### Integration Tests
- Test full extraction → reasoning → persistence flow
- Use test fixtures with known results

### End-to-End Tests
- Create temporary vault
- Run full workflow
- Verify expected discoveries

## Dependencies

### Core
- `pyyaml>=5.4.0` - YAML parsing

### Optional
- `SPARQLWrapper>=1.8.5` - Wikidata importer
- `requests>=2.25.0` - HTTP requests

### Development
- `pytest` - Testing (future)
- `black` - Code formatting (future)
- `mypy` - Type checking (future)

## References

- [Obsidian Documentation](https://help.obsidian.md/)
- [YAML Specification](https://yaml.org/spec/)
- [GitHub Actions](https://docs.github.com/en/actions)
- [Grafo Platform](https://gra.fo/)
