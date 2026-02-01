"""
Obsidian Graph Reasoner using Semantica Hawksight

This script demonstrates how to apply logical reasoning on top of an Obsidian vault
by extracting relationships from markdown files and inferring new knowledge.
"""

import os
import re
from pathlib import Path
from typing import List, Dict, Set
import yaml
from semantica.reasoning import Reasoner, Rule


class ObsidianGraphReasoner:
    """
    Reasoner that operates on an Obsidian vault by extracting relationships
    from YAML frontmatter and applying logical rules to infer new facts.
    """

    def __init__(self, vault_path: str):
        """
        Initialize the reasoner with the path to an Obsidian vault.

        Args:
            vault_path: Path to the Obsidian vault directory
        """
        self.vault_path = Path(vault_path)
        self.reasoner = Reasoner()
        self.facts = []

    def extract_entity_name(self, file_path: Path) -> str:
        """
        Extract entity name from file path (filename without extension).

        Args:
            file_path: Path to the markdown file

        Returns:
            Entity name
        """
        return file_path.stem

    def parse_wikilink(self, wikilink: str) -> str:
        """
        Parse Obsidian wikilink format [[Entity]] and extract entity name.

        Args:
            wikilink: String in format "[[Entity]]" or just "Entity"

        Returns:
            Clean entity name
        """
        if isinstance(wikilink, str):
            # Remove [[ and ]] if present
            return wikilink.replace('[[', '').replace(']]', '').strip()
        return str(wikilink)

    def extract_facts_from_file(self, file_path: Path) -> List[str]:
        """
        Extract facts from a single markdown file's YAML frontmatter.

        Args:
            file_path: Path to the markdown file

        Returns:
            List of facts in the format "subject RELATION object"
        """
        facts = []

        try:
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

            subject = self.extract_entity_name(file_path)

            # Extract different types of relationships
            for key, value in frontmatter.items():
                if value is None:
                    continue

                # Handle parent relationships
                if key == 'parent':
                    if isinstance(value, list):
                        for parent in value:
                            parent_name = self.parse_wikilink(parent)
                            facts.append(f"{parent_name} PARENT_OF {subject}")
                    else:
                        parent_name = self.parse_wikilink(value)
                        facts.append(f"{parent_name} PARENT_OF {subject}")

                # Handle type_model relationships
                elif key == 'type_model':
                    if isinstance(value, list):
                        for type_val in value:
                            type_name = self.parse_wikilink(type_val)
                            facts.append(f"{subject} IS_A {type_name}")
                    else:
                        type_name = self.parse_wikilink(value)
                        facts.append(f"{subject} IS_A {type_name}")

                # Handle type_algo relationships
                elif key == 'type_algo':
                    if isinstance(value, list):
                        for type_val in value:
                            type_name = self.parse_wikilink(type_val)
                            facts.append(f"{subject} IS_ALGORITHM_FOR {type_name}")
                    else:
                        type_name = self.parse_wikilink(value)
                        facts.append(f"{subject} IS_ALGORITHM_FOR {type_name}")

                # Handle usage relationships
                elif key == 'usage':
                    if isinstance(value, list):
                        for usage_val in value:
                            usage_name = self.parse_wikilink(usage_val)
                            facts.append(f"{subject} USED_FOR {usage_name}")
                    else:
                        usage_name = self.parse_wikilink(value)
                        facts.append(f"{subject} USED_FOR {usage_name}")

        except Exception as e:
            print(f"Error processing {file_path}: {e}")

        return facts

    def scan_vault(self) -> List[str]:
        """
        Scan the entire Obsidian vault and extract all facts.

        Returns:
            List of all facts extracted from the vault
        """
        all_facts = []

        # Find all markdown files
        for md_file in self.vault_path.rglob('*.md'):
            # Skip files in .obsidian directory
            if '.obsidian' in md_file.parts:
                continue

            file_facts = self.extract_facts_from_file(md_file)
            all_facts.extend(file_facts)

        self.facts = all_facts
        return all_facts

    def add_reasoning_rules(self):
        """
        Add logical reasoning rules to the reasoner.
        These rules define how to infer new knowledge from existing facts.
        """

        # Rule 1: Transitivity of parent relationships (grandparent rule)
        # If A is parent of B, and B is parent of C, then A is ancestor of C
        self.reasoner.add_rule(Rule(
            name="ancestor_rule",
            conditions=["?a PARENT_OF ?b", "?b PARENT_OF ?c"],
            conclusions=["?a ANCESTOR_OF ?c"]
        ))

        # Rule 2: Type inheritance through parent relationship
        # If A is a type B, and B is parent of C, then A is related to C
        self.reasoner.add_rule(Rule(
            name="type_inheritance",
            conditions=["?a IS_A ?b", "?c PARENT_OF ?b"],
            conclusions=["?a BELONGS_TO ?c"]
        ))

        # Rule 3: Usage inheritance
        # If A is type B, and B is used for C, then A can be used for C
        self.reasoner.add_rule(Rule(
            name="usage_inheritance",
            conditions=["?a IS_A ?b", "?b USED_FOR ?c"],
            conclusions=["?a CAN_BE_USED_FOR ?c"]
        ))

        # Rule 4: Shared type relationship
        # If A is type X and B is type X, then A and B are related
        self.reasoner.add_rule(Rule(
            name="shared_type",
            conditions=["?a IS_A ?x", "?b IS_A ?x"],
            conclusions=["?a SIMILAR_TO ?b"]
        ))

        # Rule 5: Algorithm applicability
        # If A is algorithm for B, and C is parent of B, then A is applicable to C domain
        self.reasoner.add_rule(Rule(
            name="algorithm_applicability",
            conditions=["?a IS_ALGORITHM_FOR ?b", "?c PARENT_OF ?b"],
            conclusions=["?a APPLICABLE_TO ?c"]
        ))

    def infer_new_knowledge(self) -> List[str]:
        """
        Apply reasoning rules to infer new facts from existing ones.

        Returns:
            List of newly inferred facts
        """
        if not self.facts:
            self.scan_vault()

        new_facts = self.reasoner.infer_facts(self.facts)
        return new_facts

    def get_all_facts(self) -> List[str]:
        """
        Get all facts (both original and inferred).

        Returns:
            Combined list of original and inferred facts
        """
        return self.facts

    def print_summary(self, inferred_facts: List[str]):
        """
        Print a summary of the reasoning results.

        Args:
            inferred_facts: List of inferred facts
        """
        print("=" * 80)
        print("OBSIDIAN GRAPH REASONER - SUMMARY")
        print("=" * 80)
        print(f"\nVault path: {self.vault_path}")
        print(f"Original facts extracted: {len(self.facts)}")
        print(f"New facts inferred: {len(inferred_facts)}")
        print("\n" + "=" * 80)
        print("ORIGINAL FACTS:")
        print("=" * 80)
        for fact in sorted(self.facts):
            print(f"  • {fact}")

        print("\n" + "=" * 80)
        print("INFERRED FACTS:")
        print("=" * 80)
        if inferred_facts:
            for fact in sorted(set(inferred_facts)):
                print(f"  ✓ {fact}")
        else:
            print("  (No new facts inferred)")
        print("=" * 80)

    def get_facts_by_relation(self, relation: str) -> List[str]:
        """
        Filter facts by a specific relation type.

        Args:
            relation: The relation to filter by (e.g., "PARENT_OF", "IS_A")

        Returns:
            List of facts containing that relation
        """
        return [fact for fact in self.facts if relation in fact]


def main():
    """
    Main function demonstrating the Obsidian Graph Reasoner.
    """
    # Initialize the reasoner with the Obsidian vault
    vault_path = os.path.join(os.path.dirname(__file__), 'graph')
    reasoner = ObsidianGraphReasoner(vault_path)

    print("Scanning Obsidian vault...")
    facts = reasoner.scan_vault()

    print(f"Extracted {len(facts)} facts from the vault.\n")

    # Add reasoning rules
    print("Adding reasoning rules...")
    reasoner.add_reasoning_rules()

    # Infer new knowledge
    print("Inferring new knowledge...\n")
    inferred_facts = reasoner.infer_new_knowledge()

    # Print summary
    reasoner.print_summary(inferred_facts)

    # Example queries
    print("\n" + "=" * 80)
    print("EXAMPLE QUERIES:")
    print("=" * 80)

    print("\n1. All parent relationships:")
    parent_facts = reasoner.get_facts_by_relation("PARENT_OF")
    for fact in sorted(parent_facts):
        print(f"   {fact}")

    print("\n2. All type relationships:")
    type_facts = reasoner.get_facts_by_relation("IS_A")
    for fact in sorted(type_facts):
        print(f"   {fact}")

    # Find inferred ancestor relationships
    ancestor_facts = [f for f in inferred_facts if "ANCESTOR_OF" in f]
    if ancestor_facts:
        print("\n3. Inferred ancestor relationships:")
        for fact in sorted(set(ancestor_facts)):
            print(f"   {fact}")


if __name__ == "__main__":
    main()
