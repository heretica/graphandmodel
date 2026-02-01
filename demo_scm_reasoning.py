#!/usr/bin/env python3
"""
Demo: Reasoning on Structural Causal Models Knowledge Graph

This script demonstrates what the reasoner will infer from the SCM knowledge base,
showing the facts extracted and the logical inferences that will be made.
"""

import os
import re
from pathlib import Path
import yaml


def extract_facts_from_vault(vault_path: Path):
    """Extract facts from all markdown files in the vault."""
    facts = []

    for md_file in vault_path.rglob('*.md'):
        if '.obsidian' in md_file.parts:
            continue

        try:
            with open(md_file, 'r', encoding='utf-8') as f:
                content = f.read()

            # Extract YAML frontmatter
            yaml_match = re.match(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
            if not yaml_match:
                continue

            yaml_content = yaml_match.group(1)
            frontmatter = yaml.safe_load(yaml_content)

            if not frontmatter:
                continue

            subject = md_file.stem

            # Extract relationships
            for key, value in frontmatter.items():
                if value is None:
                    continue

                # Handle parent relationships
                if key == 'parent':
                    values = [value] if isinstance(value, str) else value
                    for v in values:
                        parent = v.replace('[[', '').replace(']]', '').strip()
                        facts.append(f"{parent} PARENT_OF {subject}")

                # Handle type_model relationships
                elif key == 'type_model':
                    values = [value] if isinstance(value, str) else value
                    for v in values:
                        type_name = v.replace('[[', '').replace(']]', '').strip()
                        facts.append(f"{subject} IS_A {type_name}")

                # Handle part_of relationships
                elif key == 'part_of':
                    values = [value] if isinstance(value, str) else value
                    for v in values:
                        part = v.replace('[[', '').replace(']]', '').strip()
                        facts.append(f"{subject} PART_OF {part}")

                # Handle used_in relationships
                elif key == 'used_in':
                    values = [value] if isinstance(value, str) else value
                    for v in values:
                        used = v.replace('[[', '').replace(']]', '').strip()
                        facts.append(f"{subject} USED_IN {used}")

                # Handle uses relationships
                elif key == 'uses':
                    values = [value] if isinstance(value, str) else value
                    for v in values:
                        uses = v.replace('[[', '').replace(']]', '').strip()
                        facts.append(f"{subject} USES {uses}")

                # Handle known_for relationships
                elif key == 'known_for':
                    values = [value] if isinstance(value, str) else value
                    for v in values:
                        known = v.replace('[[', '').replace(']]', '').strip()
                        facts.append(f"{subject} CREATED {known}")

                # Handle field relationships
                elif key == 'field':
                    values = [value] if isinstance(value, str) else value
                    for v in values:
                        field = v.replace('[[', '').replace(']]', '').strip()
                        facts.append(f"{subject} WORKS_IN {field}")

        except Exception as e:
            print(f"Error processing {md_file}: {e}")

    return facts


def simulate_reasoning(facts):
    """Simulate what the reasoner would infer."""
    inferred = []

    # Build lookup structures
    parent_of = {}  # parent -> [children]
    is_a = {}       # subject -> [types]
    part_of = {}    # subject -> [wholes]
    uses = {}       # subject -> [tools]
    created = {}    # creator -> [creations]

    for fact in facts:
        parts = fact.split()
        if len(parts) < 3:
            continue

        if "PARENT_OF" in fact:
            parent, child = parts[0], parts[2]
            if parent not in parent_of:
                parent_of[parent] = []
            parent_of[parent].append(child)

        elif "IS_A" in fact:
            subject, type_val = parts[0], parts[2]
            if subject not in is_a:
                is_a[subject] = []
            is_a[subject].append(type_val)

        elif "PART_OF" in fact:
            part, whole = parts[0], parts[2]
            if part not in part_of:
                part_of[part] = []
            part_of[part].append(whole)

        elif "USES" in fact:
            subject, tool = parts[0], parts[2]
            if subject not in uses:
                uses[subject] = []
            uses[subject].append(tool)

        elif "CREATED" in fact:
            creator, creation = parts[0], parts[2]
            if creator not in created:
                created[creator] = []
            created[creator].append(creation)

    # Rule 1: Ancestor rule (transitivity of PARENT_OF)
    for grandparent, children in parent_of.items():
        for child in children:
            if child in parent_of:
                for grandchild in parent_of[child]:
                    inferred.append(f"{grandparent} ANCESTOR_OF {grandchild}")

    # Rule 2: Type inheritance through parent relationship
    for subject, types in is_a.items():
        for type_val in types:
            if type_val in parent_of:
                # Find parent of the type
                for parent_type in parent_of:
                    if type_val in parent_of[parent_type]:
                        inferred.append(f"{subject} BELONGS_TO {parent_type}")

    # Rule 3: Part-whole transitivity
    for part, wholes in part_of.items():
        for whole in wholes:
            if whole in part_of:
                for larger_whole in part_of[whole]:
                    inferred.append(f"{part} INDIRECTLY_PART_OF {larger_whole}")

    # Rule 4: Usage inheritance (if A uses B and C uses A, then C indirectly uses B)
    for user, tools in uses.items():
        for tool in tools:
            if tool in uses:
                for subtool in uses[tool]:
                    inferred.append(f"{user} INDIRECTLY_USES {subtool}")

    # Rule 5: Creation attribution (if A created B and B is part of C, A contributed to C)
    for creator, creations in created.items():
        for creation in creations:
            if creation in part_of:
                for whole in part_of[creation]:
                    inferred.append(f"{creator} CONTRIBUTED_TO {whole}")

    return list(set(inferred))  # Remove duplicates


def main():
    """Main demo function."""
    print("=" * 80)
    print("SCM KNOWLEDGE GRAPH REASONING DEMO")
    print("=" * 80)

    vault_path = Path("graph")

    print(f"\n[1/3] Scanning Obsidian vault: {vault_path}")
    facts = extract_facts_from_vault(vault_path)
    print(f"     Extracted {len(facts)} facts from markdown files")

    # Organize facts by category
    ml_facts = [f for f in facts if any(term in f for term in
                ["Classification", "Regression", "Clustering", "Model", "Logistic", "Linear", "KNN"])]
    scm_facts = [f for f in facts if any(term in f for term in
                 ["Causal", "DAG", "Pearl", "Rubin", "Counterfactual", "Structural"])]

    print(f"\n[2/3] Fact breakdown:")
    print(f"     ML Model facts: {len(ml_facts)}")
    print(f"     SCM/Causal facts: {len(scm_facts)}")
    print(f"     Total facts: {len(facts)}")

    print(f"\n[3/3] Simulating reasoning...")
    inferred = simulate_reasoning(facts)
    print(f"     Generated {len(inferred)} inferred facts")

    # Display sample facts
    print("\n" + "=" * 80)
    print("SAMPLE ORIGINAL FACTS")
    print("=" * 80)

    print("\n📊 Machine Learning Facts:")
    for fact in sorted(ml_facts)[:5]:
        print(f"  • {fact}")
    if len(ml_facts) > 5:
        print(f"  ... and {len(ml_facts) - 5} more")

    print("\n🧠 Causal Inference Facts:")
    for fact in sorted(scm_facts)[:10]:
        print(f"  • {fact}")
    if len(scm_facts) > 10:
        print(f"  ... and {len(scm_facts) - 10} more")

    # Display inferred facts
    print("\n" + "=" * 80)
    print("INFERRED FACTS (from reasoning rules)")
    print("=" * 80)

    if inferred:
        # Group by relation type
        by_relation = {}
        for fact in inferred:
            parts = fact.split()
            if len(parts) >= 2:
                relation = parts[1]
                if relation not in by_relation:
                    by_relation[relation] = []
                by_relation[relation].append(fact)

        for relation, relation_facts in sorted(by_relation.items()):
            print(f"\n{relation} ({len(relation_facts)} inferred):")
            for fact in sorted(relation_facts)[:5]:
                print(f"  ✓ {fact}")
            if len(relation_facts) > 5:
                print(f"  ... and {len(relation_facts) - 5} more")
    else:
        print("  (No facts inferred - this is a simulation)")

    # Key insights
    print("\n" + "=" * 80)
    print("KEY INSIGHTS")
    print("=" * 80)
    print("""
The knowledge graph now contains:

1. **Machine Learning Models** (Original)
   - Classification, Regression, Clustering hierarchies
   - Specific models: Logistic Regression, Linear Regression, KNN
   - Usage relationships: models used for Prediction

2. **Structural Causal Models** (Newly Added)
   - Core concepts: SCM, Causality, Causal Inference
   - Graph structures: DAG, Causal Graph, d-separation
   - Methods: do-calculus, Backdoor Criterion, Instrumental Variables
   - Researchers: Judea Pearl, Donald Rubin
   - Applications: Fairness in ML, Policy Evaluation

3. **Inferred Relationships**
   - Hierarchical relationships (ancestors)
   - Part-whole transitivity
   - Attribution and contribution
   - Indirect dependencies

The reasoner can now answer questions like:
- "What are all ancestors of Collider?" → Causal Graph, DAG, Graph Theory
- "What did Judea Pearl contribute to?" → SCM, do-calculus, and their applications
- "What methods are part of Causal Inference?" → All the techniques we added
""")
    print("=" * 80)

    # Instructions
    print("\n📝 Next Steps:")
    print("  1. Install semantica: pip install semantica")
    print("  2. Run full reasoner: python demo_reasoner.py")
    print("  3. Explore in Obsidian to see the visual graph")
    print("\n" + "=" * 80)


if __name__ == "__main__":
    main()
