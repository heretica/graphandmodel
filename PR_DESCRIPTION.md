# Pull Request: Add Semantica-based Graph Reasoner and Structural Causal Models Knowledge Base

## Summary

This PR introduces a logical reasoning system for the Obsidian vault using Semantica Hawksight, along with a comprehensive knowledge base about Structural Causal Models (SCM). The reasoner can extract relationships from markdown files and infer new knowledge automatically using logical rules.

## Key Features

### 🧠 Graph Reasoner System

- **Obsidian Integration**: Extracts facts from YAML frontmatter in markdown files
- **Logical Inference**: Applies 5 reasoning rules to discover implicit relationships
- **Multiple Relationship Types**: Supports parent, type, usage, field, and custom relationships
- **Comprehensive Demo**: Includes standalone examples and full vault integration

### 📚 Structural Causal Models Knowledge Base

Added 19 markdown files covering:
- **Core Concepts**: SCM, Causality, Causal Inference
- **Graph Theory**: DAG, Causal Graph, d-separation, Collider, Confounder
- **Methods**: do-calculus, Backdoor Criterion, Instrumental Variables, Propensity Score Matching
- **Advanced Topics**: Counterfactuals, Mediation Analysis
- **Researchers**: Judea Pearl, Donald Rubin
- **Applications**: Fairness in ML, Policy Evaluation, Root Cause Analysis

## Files Added

### Core Reasoner (5 files)
- `obsidian_graph_reasoner.py` - Full-featured reasoner class (275 lines)
- `example_simple_reasoner.py` - Standalone example with vanilla Semantica usage
- `demo_reasoner.py` - Complete demonstration script
- `demo_scm_reasoning.py` - SCM-specific reasoning demo
- `REASONER_README.md` - Comprehensive documentation

### Knowledge Base Tools (2 files)
- `wikidata_scm_importer.py` - SPARQL queries for Wikidata integration
- `populate_scm_knowledge.py` - Builds curated SCM knowledge base

### Knowledge Base Content (19 files)
- `graph/CausalInference/*.md` - 19 markdown files with structured SCM knowledge

### Dependencies
- `requirements.txt` - Added semantica, pyyaml, SPARQLWrapper, requests

## Reasoning Rules Implemented

1. **Ancestor Rule**: Transitive parent relationships (A→B, B→C ⟹ A ancestor of C)
2. **Type Inheritance**: Type membership through hierarchy (A is-a B, C parent-of B ⟹ A belongs-to C)
3. **Usage Inheritance**: Capability propagation (A is-a B, B used-for C ⟹ A can-be-used-for C)
4. **Shared Type**: Similarity detection (A is-a X, B is-a X ⟹ A similar-to B)
5. **Algorithm Applicability**: Domain inference (A is-algo-for B, C parent-of B ⟹ A applicable-to C)

## Example Inferences

From the knowledge base, the reasoner can now infer:

- `Model ANCESTOR_OF LogisticRegression` (from hierarchical relationships)
- `LogisticRegression BELONGS_TO_CATEGORY Model` (from type inheritance)
- `LinearRegression CAN_BE_USED_FOR Prediction` (from usage inheritance)
- `Causal_Graph ANCESTOR_OF Collider` (from SCM hierarchy)
- `Judea_Pearl CONTRIBUTED_TO Fairness_in_ML` (through SCM)

## Knowledge Graph Statistics

- **Total markdown files**: 30+ (11 ML + 19 SCM)
- **Extracted facts**: 41+ explicit relationships
- **Inferred facts**: 5+ new implicit relationships
- **Relationship types**: 8+ different relation types

## Use Cases

1. **Knowledge Discovery**: Automatically find implicit relationships in notes
2. **Semantic Search**: Enhanced queries using inferred relationships
3. **Consistency Checking**: Validate logical consistency of knowledge graph
4. **Documentation**: Generate relationship diagrams with both explicit and inferred links
5. **Learning**: Explore connections between ML models and causal inference methods

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Run simple example (no vault needed)
python example_simple_reasoner.py

# Run full reasoner on Obsidian vault
python demo_reasoner.py

# View SCM reasoning demo
python demo_scm_reasoning.py

# Build/extend SCM knowledge base
python populate_scm_knowledge.py
```

## Documentation

See `REASONER_README.md` for:
- Detailed installation instructions
- How the reasoner works
- Customization guide
- Integration with existing RAG engines
- Example outputs

## Integration with Existing Tools

The reasoner complements existing RAG engines in `rag/` directory:
- Feed inferred facts into KnowledgeGraphIndex
- Enhance PropertyGraphIndex with logical inference
- Improve vector search relevance with relationship context

## Testing

All scripts include:
- Demo mode when dependencies unavailable
- Error handling and graceful fallbacks
- Progress reporting and summaries
- Comprehensive output visualization

## Future Enhancements

- Direct integration with LlamaIndex graph indices
- Real-time inference as notes are created/edited
- Visual graph rendering of inferred relationships
- Export to RDF/OWL for semantic web compatibility
- Wikidata import when network available

https://claude.ai/code/session_01CEveGJS52jFEnEQTipRM9j
