#!/usr/bin/env python3
"""
Complete Demo: Obsidian Graph Reasoner

This script demonstrates the complete workflow:
1. Extract facts from Obsidian markdown files
2. Define reasoning rules
3. Infer new knowledge
4. Display results
"""

import sys
from pathlib import Path

# Add current directory to path
sys.path.insert(0, str(Path(__file__).parent))

try:
    from obsidian_graph_reasoner import ObsidianGraphReasoner
    REASONER_AVAILABLE = True
except ImportError as e:
    print(f"Warning: Could not import ObsidianGraphReasoner: {e}")
    print("Make sure semantica is installed: pip install semantica")
    REASONER_AVAILABLE = False


def main():
    """Run the complete demo."""

    if not REASONER_AVAILABLE:
        print("\n" + "=" * 80)
        print("DEMO MODE - Showing expected output structure")
        print("=" * 80)
        print("\nTo run the full reasoner, install dependencies:")
        print("  pip install -r requirements.txt")
        print("\nExpected workflow:")
        print("  1. Scan Obsidian vault for .md files")
        print("  2. Extract YAML frontmatter relationships")
        print("  3. Convert to logical facts (subject RELATION object)")
        print("  4. Apply reasoning rules")
        print("  5. Infer new knowledge")
        print("\nExample reasoning rules:")
        print("  • Ancestor Rule: A→B, B→C ⟹ A is ancestor of C")
        print("  • Type Inheritance: A is-a B, C parent-of B ⟹ A belongs-to C")
        print("  • Usage Inheritance: A is-a B, B used-for C ⟹ A can-be-used-for C")
        print("=" * 80)
        return

    print("=" * 80)
    print("OBSIDIAN GRAPH REASONER - FULL DEMO")
    print("=" * 80)

    # Step 1: Initialize reasoner
    print("\n[1/5] Initializing reasoner...")
    vault_path = Path(__file__).parent / 'graph'

    if not vault_path.exists():
        print(f"Error: Vault path not found: {vault_path}")
        print("Please ensure the 'graph/' directory exists with Obsidian markdown files.")
        return

    reasoner = ObsidianGraphReasoner(str(vault_path))

    # Step 2: Scan vault
    print(f"[2/5] Scanning Obsidian vault: {vault_path}")
    facts = reasoner.scan_vault()
    print(f"     Extracted {len(facts)} facts from markdown files")

    if not facts:
        print("     Warning: No facts extracted. Check your markdown files have YAML frontmatter.")
        print("     Example frontmatter:")
        print("     ---")
        print("     parent: \"[[ParentConcept]]\"")
        print("     type_model: \"[[SomeType]]\"")
        print("     ---")
        return

    # Step 3: Add reasoning rules
    print("[3/5] Adding reasoning rules...")
    reasoner.add_reasoning_rules()
    print("     ✓ Ancestor rule")
    print("     ✓ Type inheritance rule")
    print("     ✓ Usage inheritance rule")
    print("     ✓ Shared type rule")
    print("     ✓ Algorithm applicability rule")

    # Step 4: Infer new knowledge
    print("[4/5] Inferring new knowledge...")
    inferred_facts = reasoner.infer_new_knowledge()
    print(f"     Generated {len(inferred_facts)} new inferred facts")

    # Step 5: Display results
    print("[5/5] Displaying results...\n")
    reasoner.print_summary(inferred_facts)

    # Additional analysis
    if inferred_facts:
        print("\n" + "=" * 80)
        print("KNOWLEDGE EXPANSION ANALYSIS")
        print("=" * 80)

        expansion_rate = (len(inferred_facts) / len(facts)) * 100 if facts else 0
        print(f"\nKnowledge expansion: {expansion_rate:.1f}%")
        print(f"  • Original facts: {len(facts)}")
        print(f"  • Inferred facts: {len(inferred_facts)}")
        print(f"  • Total knowledge: {len(facts) + len(inferred_facts)}")

        # Categorize inferred facts
        relation_types = {}
        for fact in inferred_facts:
            parts = fact.split()
            if len(parts) >= 3:
                relation = parts[1]
                relation_types[relation] = relation_types.get(relation, 0) + 1

        if relation_types:
            print("\nInferred relationships by type:")
            for relation, count in sorted(relation_types.items(), key=lambda x: x[1], reverse=True):
                print(f"  • {relation}: {count}")

        print("=" * 80)

    print("\n✅ Demo completed successfully!")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nDemo interrupted by user.")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error during demo: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
