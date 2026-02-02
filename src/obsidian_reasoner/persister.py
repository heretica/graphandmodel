"""
Persist discovered facts back to Obsidian markdown files.
"""

import re
from pathlib import Path
from collections import defaultdict
from typing import List, Dict
import yaml

from .models import Fact


class DiscoveryPersister:
    """
    Writes inferred facts back to Obsidian vault as YAML frontmatter.
    """

    # Map relation types to YAML frontmatter keys
    RELATION_TO_KEY = {
        # Original domain-specific relations
        'ANCESTOR_OF': 'ancestor_of',
        'THEORY_APPLIED_BY': 'theory_applied_by',
        'DOMAIN_ENCOMPASSES': 'domain_encompasses',
        'CONTRIBUTED_TO': 'contributed_to',
        'INDIRECTLY_USES': 'indirectly_uses',
        'TRANSITIVELY_PART_OF': 'transitively_part_of',
        # New OWL-inspired relations
        'COAUTHOR_OF': 'coauthor_of',
        'COLLABORATES_WITH': 'collaborates_with',
        'CREATED_BY': 'created_by',
        'USED_BY': 'used_by',
        'HAS_PART': 'has_part',
        'INHERITS_METHODOLOGY_FROM': 'inherits_methodology_from',
        'CONTRIBUTED_TO_FIELD': 'contributed_to_field',
        'BRIDGES_DOMAIN': 'bridges_domain',
        'REQUIRES_UNDERSTANDING': 'requires_understanding',
    }

    def __init__(self, vault_path: Path):
        """
        Initialize the persister.

        Args:
            vault_path: Path to the Obsidian vault directory
        """
        self.vault_path = Path(vault_path)

    def persist(self, inferred_facts: List[Fact]) -> Dict[str, int]:
        """
        Persist inferred facts to markdown files.

        Args:
            inferred_facts: List of facts to persist

        Returns:
            Dictionary with statistics about the persistence operation
        """
        # Organize discoveries by source entity
        discoveries_by_source = self._organize_by_source(inferred_facts)

        updated_files = []
        skipped_entities = []

        # Update each file
        for entity, relations in sorted(discoveries_by_source.items()):
            file_path = self._find_markdown_file(entity)

            if not file_path:
                skipped_entities.append(entity)
                continue

            for relation, targets in relations.items():
                if self._add_to_file(file_path, relation, targets):
                    updated_files.append(file_path)

        return {
            'updated_files': len(set(updated_files)),
            'skipped_entities': len(skipped_entities),
            'total_facts': len(inferred_facts),
        }

    def _organize_by_source(self, facts: List[Fact]) -> Dict[str, Dict[str, List[str]]]:
        """
        Organize facts by source entity and relation type.

        Args:
            facts: List of facts to organize

        Returns:
            Nested dictionary: {entity: {relation: [targets]}}
        """
        organized = defaultdict(lambda: defaultdict(list))

        for fact in facts:
            organized[fact.subject][fact.relation].append(fact.object)

        return organized

    def _find_markdown_file(self, entity_name: str) -> Path:
        """
        Find the markdown file for a given entity.

        Args:
            entity_name: Name of the entity

        Returns:
            Path to the markdown file, or None if not found
        """
        for md_file in self.vault_path.rglob('*.md'):
            if '.obsidian' in md_file.parts:
                continue
            if md_file.stem == entity_name:
                return md_file
        return None

    def _add_to_file(self, file_path: Path, relation: str, targets: List[str]) -> bool:
        """
        Add discovered relationships to a markdown file's frontmatter.

        Args:
            file_path: Path to the markdown file
            relation: Relation type
            targets: List of target entities

        Returns:
            True if file was updated, False otherwise
        """
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Extract frontmatter
        yaml_match = re.match(r'^---\s*\n(.*?)\n---\s*\n(.*)$', content, re.DOTALL)
        if not yaml_match:
            return False

        yaml_content = yaml_match.group(1)
        body = yaml_match.group(2)
        frontmatter = yaml.safe_load(yaml_content) or {}

        # Map relation to YAML key
        key = self.RELATION_TO_KEY.get(relation)
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
