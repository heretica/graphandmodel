#!/usr/bin/env python3
"""
Persist discovered facts back to the Obsidian vault.
"""

import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.obsidian_reasoner import ObsidianFactExtractor, GraphReasoner, DiscoveryPersister


def main():
    vault_path = Path("graph")

    print("=" * 80)
    print("PERSISTING DISCOVERED FACTS TO OBSIDIAN GRAPH")
    print("=" * 80)

    # Extract facts and infer new ones
    print(f"\n[1/3] Extracting facts and running reasoner...")
    extractor = ObsidianFactExtractor(vault_path)
    facts = extractor.extract_facts()

    reasoner = GraphReasoner()
    inferred = reasoner.infer(facts)
    print(f"     Discovered {len(inferred)} new facts")

    # Persist discoveries
    print(f"\n[2/3] Adding discoveries to markdown files...")
    persister = DiscoveryPersister(vault_path)
    stats = persister.persist(inferred)

    print(f"\n[3/3] Summary")
    print(f"     Updated {stats['updated_files']} files")
    print(f"     Skipped {stats['skipped_entities']} entities (file not found)")
    print(f"     Total facts persisted: {stats['total_facts']}")

    print("\n" + "=" * 80)
    print("DISCOVERY INTEGRATION COMPLETE")
    print("=" * 80)
    print("\nDiscovered relationships are now part of the knowledge graph!")
    print("Run analyze.py again to see the enriched graph.\n")


if __name__ == "__main__":
    main()
