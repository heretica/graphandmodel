"""
Extract facts from Obsidian markdown files.
"""

import re
from pathlib import Path
from typing import List, Tuple
import yaml

from .models import Fact


class ObsidianFactExtractor:
    """Extracts relationship facts from Obsidian vault YAML frontmatter."""

    # Map YAML keys to relation types
    RELATION_MAPPINGS = {
        'parent': ('PARENT_OF', True),  # (relation_type, inverted)
        'type_model': ('IS_A', False),
        'part_of': ('PART_OF', False),
        'used_in': ('USED_IN', False),
        'uses': ('USES', False),
        'known_for': ('CREATED', False),
        'created_by': ('CREATED', True),
        'field': ('WORKS_IN', False),
        'used_for': ('USED_FOR', False),
    }

    def __init__(self, vault_path: Path):
        """
        Initialize the extractor.

        Args:
            vault_path: Path to the Obsidian vault directory
        """
        self.vault_path = Path(vault_path)

    def extract_facts(self) -> List[Fact]:
        """
        Extract all facts from the vault.

        Returns:
            List of Fact objects
        """
        facts = []

        for md_file in self.vault_path.rglob('*.md'):
            # Skip .obsidian directory
            if '.obsidian' in md_file.parts:
                continue

            try:
                file_facts = self._extract_from_file(md_file)
                facts.extend(file_facts)
            except Exception as e:
                # Silently skip files that can't be processed
                pass

        return facts

    def _extract_from_file(self, file_path: Path) -> List[Fact]:
        """
        Extract facts from a single markdown file.

        Args:
            file_path: Path to the markdown file

        Returns:
            List of facts extracted from the file
        """
        facts = []

        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Extract YAML frontmatter
        yaml_match = re.match(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
        if not yaml_match:
            return facts

        yaml_content = yaml_match.group(1)
        frontmatter = yaml.safe_load(yaml_content)

        if not frontmatter:
            return facts

        subject = file_path.stem

        # Process each frontmatter key
        for key, value in frontmatter.items():
            if value is None:
                continue

            if key not in self.RELATION_MAPPINGS:
                continue

            relation_type, inverted = self.RELATION_MAPPINGS[key]

            # Normalize to list
            values = [value] if isinstance(value, str) else value

            for v in values:
                # Clean wikilink format
                target = v.replace('[[', '').replace(']]', '').strip()

                # Create fact (swap subject/object if inverted)
                if inverted:
                    facts.append(Fact(relation_type, target, subject))
                else:
                    facts.append(Fact(relation_type, subject, target))

        return facts

    def find_markdown_file(self, entity_name: str) -> Path:
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
