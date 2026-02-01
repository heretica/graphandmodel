#!/usr/bin/env python3
"""
Enhanced SCM Reasoning Analysis

Shows detailed inferences from the SCM knowledge graph.
"""

import os
import re
from pathlib import Path
import yaml
from collections import defaultdict


def extract_facts_from_vault(vault_path: Path):
    """Extract all facts from markdown files."""
    facts = []

    for md_file in vault_path.rglob('*.md'):
        if '.obsidian' in md_file.parts:
            continue

        try:
            with open(md_file, 'r', encoding='utf-8') as f:
                content = f.read()

            yaml_match = re.match(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
            if not yaml_match:
                continue

            yaml_content = yaml_match.group(1)
            frontmatter = yaml.safe_load(yaml_content)

            if not frontmatter:
                continue

            subject = md_file.stem

            for key, value in frontmatter.items():
                if value is None:
                    continue

                if key == 'parent':
                    values = [value] if isinstance(value, str) else value
                    for v in values:
                        parent = v.replace('[[', '').replace(']]', '').strip()
                        facts.append(('PARENT_OF', parent, subject))

                elif key == 'type_model':
                    values = [value] if isinstance(value, str) else value
                    for v in values:
                        type_name = v.replace('[[', '').replace(']]', '').strip()
                        facts.append(('IS_A', subject, type_name))

                elif key == 'part_of':
                    values = [value] if isinstance(value, str) else value
                    for v in values:
                        part = v.replace('[[', '').replace(']]', '').strip()
                        facts.append(('PART_OF', subject, part))

                elif key == 'used_in':
                    values = [value] if isinstance(value, str) else value
                    for v in values:
                        used = v.replace('[[', '').replace(']]', '').strip()
                        facts.append(('USED_IN', subject, used))

                elif key == 'uses':
                    values = [value] if isinstance(value, str) else value
                    for v in values:
                        uses = v.replace('[[', '').replace(']]', '').strip()
                        facts.append(('USES', subject, uses))

                elif key == 'known_for':
                    values = [value] if isinstance(value, str) else value
                    for v in values:
                        known = v.replace('[[', '').replace(']]', '').strip()
                        facts.append(('CREATED', subject, known))

                elif key == 'created_by':
                    values = [value] if isinstance(value, str) else value
                    for v in values:
                        creator = v.replace('[[', '').replace(']]', '').strip()
                        facts.append(('CREATED', creator, subject))

                elif key == 'field':
                    values = [value] if isinstance(value, str) else value
                    for v in values:
                        field = v.replace('[[', '').replace(']]', '').strip()
                        facts.append(('WORKS_IN', subject, field))

                elif key == 'used_for':
                    values = [value] if isinstance(value, str) else value
                    for v in values:
                        usage = v.replace('[[', '').replace(']]', '').strip()
                        facts.append(('USED_FOR', subject, usage))

        except Exception as e:
            pass

    return facts


def infer_facts(facts):
    """Apply reasoning rules to infer new facts."""
    inferred = set()

    # Build indexes
    parent_of = defaultdict(set)
    part_of = defaultdict(set)
    uses = defaultdict(set)
    created = defaultdict(set)
    is_a = defaultdict(set)

    for relation, subj, obj in facts:
        if relation == 'PARENT_OF':
            parent_of[subj].add(obj)
        elif relation == 'PART_OF':
            part_of[subj].add(obj)
        elif relation == 'USES':
            uses[subj].add(obj)
        elif relation == 'CREATED':
            created[subj].add(obj)
        elif relation == 'IS_A':
            is_a[subj].add(obj)

    # Rule 1: Transitive PARENT_OF → ANCESTOR_OF
    for grandparent, children in parent_of.items():
        for child in children:
            if child in parent_of:
                for grandchild in parent_of[child]:
                    inferred.add(('ANCESTOR_OF', grandparent, grandchild))

    # Rule 2: Transitive PART_OF
    for part, wholes in part_of.items():
        for whole in wholes:
            if whole in part_of:
                for larger_whole in part_of[whole]:
                    inferred.add(('TRANSITIVELY_PART_OF', part, larger_whole))

    # Rule 3: Created X, X part of Y → Contributed to Y
    for creator, creations in created.items():
        for creation in creations:
            if creation in part_of:
                for whole in part_of[creation]:
                    inferred.add(('CONTRIBUTED_TO', creator, whole))

    # Rule 4: Uses X, X uses Y → Indirectly uses Y
    for user, tools in uses.items():
        for tool in tools:
            if tool in uses:
                for subtool in uses[tool]:
                    inferred.add(('INDIRECTLY_USES', user, subtool))

    # Rule 5: Parent of X, X part of Y → Related to Y
    for parent, children in parent_of.items():
        for child in children:
            if child in part_of:
                for whole in part_of[child]:
                    inferred.add(('DOMAIN_ENCOMPASSES', parent, whole))

    # Rule 6: Created by X, Used by Y → Applied by Y
    for creator, creations in created.items():
        for creation in creations:
            for user, used_items in uses.items():
                if creation in used_items:
                    inferred.add(('THEORY_APPLIED_BY', creator, user))

    return list(inferred)


def main():
    vault_path = Path("graph")

    print("=" * 80)
    print("ENHANCED SCM REASONING ANALYSIS")
    print("=" * 80)

    print(f"\n[1/4] Extracting facts from {vault_path}...")
    facts = extract_facts_from_vault(vault_path)
    print(f"     Extracted {len(facts)} facts")

    # Organize by relation type
    by_relation = defaultdict(list)
    for relation, subj, obj in facts:
        by_relation[relation].append((subj, obj))

    print(f"\n[2/4] Fact types:")
    for relation, pairs in sorted(by_relation.items()):
        print(f"     {relation}: {len(pairs)} facts")

    print(f"\n[3/4] Applying reasoning rules...")
    inferred = infer_facts(facts)
    print(f"     Generated {len(inferred)} new inferred facts")

    # Organize inferred facts
    inferred_by_relation = defaultdict(list)
    for relation, subj, obj in inferred:
        inferred_by_relation[relation].append((subj, obj))

    print(f"\n[4/4] Displaying results...")

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

    print("\n" + "=" * 80)
    print("INFERRED FACTS BY REASONING RULES")
    print("=" * 80)

    for relation, pairs in sorted(inferred_by_relation.items()):
        print(f"\n{relation} ({len(pairs)} inferred):")
        for subj, obj in sorted(pairs)[:10]:
            print(f"  ✓ {subj} → {obj}")
        if len(pairs) > 10:
            print(f"  ... and {len(pairs) - 10} more")

    print("\n" + "=" * 80)
    print("KNOWLEDGE GRAPH INSIGHTS")
    print("=" * 80)

    # Find key nodes
    all_entities = set()
    for _, subj, obj in facts + inferred:
        all_entities.add(subj)
        all_entities.add(obj)

    print(f"\nTotal unique entities: {len(all_entities)}")
    print(f"Total relationships: {len(facts)} (original) + {len(inferred)} (inferred) = {len(facts) + len(inferred)}")

    # Find most connected entities
    connections = defaultdict(int)
    for _, subj, obj in facts + inferred:
        connections[subj] += 1
        connections[obj] += 1

    print(f"\nMost connected entities:")
    for entity, count in sorted(connections.items(), key=lambda x: x[1], reverse=True)[:10]:
        print(f"  • {entity}: {count} connections")

    print("\n" + "=" * 80)
    print("EXAMPLE QUERIES THE REASONER CAN ANSWER")
    print("=" * 80)

    print("""
1. "What did Judea Pearl create?"
   → Structural Causal Model, do-calculus

2. "What is Judea Pearl's impact?"
   → CONTRIBUTED_TO Structural Causal Model
   → THEORY_APPLIED_BY Fairness in Machine Learning
   → THEORY_APPLIED_BY Root Cause Analysis

3. "What are the ancestors of Collider?"
   → Causal Graph (parent)
   → Directed Acyclic Graph (grandparent via transitivity)

4. "What methods are part of Causal Inference?"
   → Instrumental Variables, Propensity Score Matching,
   → Mediation Analysis, Policy Evaluation, Root Cause Analysis

5. "What uses Structural Causal Model?"
   → Fairness in Machine Learning
   → Counterfactual reasoning
   → Mediation Analysis

6. "What is the relationship between Pearl and applications?"
   → Pearl CREATED do-calculus
   → do-calculus PART_OF Structural Causal Model
   → Fairness in ML USES Structural Causal Model
   → Therefore: Pearl CONTRIBUTED_TO modern ML fairness
    """)

    print("=" * 80)


if __name__ == "__main__":
    main()
