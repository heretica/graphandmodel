#!/usr/bin/env python3
"""
Analyze and display inferred facts from the Obsidian knowledge graph.
"""

import sys
from pathlib import Path
from collections import defaultdict

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.obsidian_reasoner import ObsidianFactExtractor, GraphReasoner


def main():
    vault_path = Path("graph")

    print("=" * 80)
    print("ENHANCED SCM REASONING ANALYSIS")
    print("=" * 80)

    # Extract facts
    print(f"\n[1/4] Extracting facts from {vault_path}...")
    extractor = ObsidianFactExtractor(vault_path)
    facts = extractor.extract_facts()
    print(f"     Extracted {len(facts)} facts")

    # Organize by relation type
    by_relation = defaultdict(list)
    for fact in facts:
        by_relation[fact.relation].append((fact.subject, fact.object))

    print(f"\n[2/4] Fact types:")
    for relation, pairs in sorted(by_relation.items()):
        print(f"     {relation}: {len(pairs)} facts")

    # Apply reasoning
    print(f"\n[3/4] Applying reasoning rules...")
    reasoner = GraphReasoner()
    inferred = reasoner.infer(facts)
    print(f"     Generated {len(inferred)} new inferred facts")

    # Organize inferred facts
    inferred_by_relation = defaultdict(list)
    for fact in inferred:
        inferred_by_relation[fact.relation].append((fact.subject, fact.object))

    print(f"\n[4/4] Displaying results...")

    # Display original facts
    print("\n" + "=" * 80)
    print("ORIGINAL FACTS BY CATEGORY")
    print("=" * 80)

    for relation in ['PARENT_OF', 'PART_OF', 'CREATED', 'USES']:
        if relation in by_relation:
            print(f"\n{relation} ({len(by_relation[relation])} facts):")
            for subj, obj in sorted(by_relation[relation])[:10]:
                print(f"  • {subj} → {obj}")
            if len(by_relation[relation]) > 10:
                print(f"  ... and {len(by_relation[relation]) - 10} more")

    # Display inferred facts
    print("\n" + "=" * 80)
    print("INFERRED FACTS BY REASONING RULES")
    print("=" * 80)

    for relation, pairs in sorted(inferred_by_relation.items()):
        print(f"\n{relation} ({len(pairs)} inferred):")
        for subj, obj in sorted(pairs)[:10]:
            print(f"  ✓ {subj} → {obj}")
        if len(pairs) > 10:
            print(f"  ... and {len(pairs) - 10} more")

    # Display insights
    print("\n" + "=" * 80)
    print("KNOWLEDGE GRAPH INSIGHTS")
    print("=" * 80)

    all_entities = set()
    for fact in facts + inferred:
        all_entities.add(fact.subject)
        all_entities.add(fact.object)

    print(f"\nTotal unique entities: {len(all_entities)}")
    print(f"Total relationships: {len(facts)} (original) + {len(inferred)} (inferred) = {len(facts) + len(inferred)}")

    # Most connected entities
    connections = defaultdict(int)
    for fact in facts + inferred:
        connections[fact.subject] += 1
        connections[fact.object] += 1

    print(f"\nMost connected entities:")
    for entity, count in sorted(connections.items(), key=lambda x: x[1], reverse=True)[:10]:
        print(f"  • {entity}: {count} connections")

    print("\n" + "=" * 80)


if __name__ == "__main__":
    main()
