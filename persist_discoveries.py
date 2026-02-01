#!/usr/bin/env python3
"""
Persist Discovered Facts into Obsidian Graph

Takes inferred facts from the reasoner and adds them back to the
markdown files as YAML frontmatter properties.
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


def find_markdown_file(vault_path: Path, entity_name: str):
    """Find the markdown file for a given entity."""
    for md_file in vault_path.rglob('*.md'):
        if '.obsidian' in md_file.parts:
            continue
        if md_file.stem == entity_name:
            return md_file
    return None


def add_discovery_to_file(file_path: Path, relation: str, targets: list):
    """Add discovered relationships to a markdown file's frontmatter."""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    yaml_match = re.match(r'^---\s*\n(.*?)\n---\s*\n(.*)$', content, re.DOTALL)
    if not yaml_match:
        print(f"  ⚠️  No frontmatter found in {file_path.name}")
        return False

    yaml_content = yaml_match.group(1)
    body = yaml_match.group(2)
    frontmatter = yaml.safe_load(yaml_content) or {}

    # Map relation types to YAML keys
    key_map = {
        'ANCESTOR_OF': 'ancestor_of',
        'THEORY_APPLIED_BY': 'theory_applied_by',
        'DOMAIN_ENCOMPASSES': 'domain_encompasses',
        'CONTRIBUTED_TO': 'contributed_to',
        'INDIRECTLY_USES': 'indirectly_uses',
        'TRANSITIVELY_PART_OF': 'transitively_part_of'
    }

    key = key_map.get(relation)
    if not key:
        return False

    # Format targets as wikilinks
    formatted_targets = [f"[[{t}]]" for t in targets]

    # Add or update the key
    if key in frontmatter:
        existing = frontmatter[key]
        if isinstance(existing, str):
            existing = [existing]
        # Merge and deduplicate
        all_targets = set(existing + formatted_targets)
        frontmatter[key] = sorted(list(all_targets))
    else:
        frontmatter[key] = formatted_targets if len(formatted_targets) > 1 else formatted_targets[0]

    # Add discovery metadata
    if 'inferred_by' not in frontmatter:
        frontmatter['inferred_by'] = 'reasoner'

    # Write back
    new_yaml = yaml.dump(frontmatter, default_flow_style=False, allow_unicode=True, sort_keys=False)
    new_content = f"---\n{new_yaml}---\n{body}"

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(new_content)

    return True


def main():
    vault_path = Path("graph")

    print("=" * 80)
    print("PERSISTING DISCOVERED FACTS TO OBSIDIAN GRAPH")
    print("=" * 80)

    print(f"\n[1/3] Extracting facts and running reasoner...")
    facts = extract_facts_from_vault(vault_path)
    inferred = infer_facts(facts)
    print(f"     Discovered {len(inferred)} new facts")

    # Organize discoveries by source entity
    discoveries_by_source = defaultdict(lambda: defaultdict(list))
    for relation, source, target in inferred:
        discoveries_by_source[source][relation].append(target)

    print(f"\n[2/3] Adding discoveries to markdown files...")

    updated_files = []
    for entity, relations in sorted(discoveries_by_source.items()):
        file_path = find_markdown_file(vault_path, entity)
        if not file_path:
            print(f"  ⚠️  File not found for: {entity}")
            continue

        print(f"\n  📝 {entity}")
        for relation, targets in relations.items():
            if add_discovery_to_file(file_path, relation, targets):
                print(f"     + {relation}: {len(targets)} discoveries")
                updated_files.append(file_path)

    print(f"\n[3/3] Summary")
    print(f"     Updated {len(set(updated_files))} files with discovered knowledge")

    print("\n" + "=" * 80)
    print("DISCOVERY INTEGRATION COMPLETE")
    print("=" * 80)
    print("\nDiscovered relationships are now part of the knowledge graph!")
    print("Run analyze_scm_reasoning.py again to see the enriched graph.\n")


if __name__ == "__main__":
    main()
