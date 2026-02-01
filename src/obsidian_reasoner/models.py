"""
Data models for the Obsidian reasoning system.
"""

from dataclasses import dataclass
from typing import List, Tuple


@dataclass
class Fact:
    """Represents a relationship fact in the knowledge graph."""
    relation: str
    subject: str
    object: str

    def as_tuple(self) -> Tuple[str, str, str]:
        """Convert to tuple format (relation, subject, object)."""
        return (self.relation, self.subject, self.object)

    @classmethod
    def from_tuple(cls, fact_tuple: Tuple[str, str, str]) -> 'Fact':
        """Create Fact from tuple format."""
        return cls(
            relation=fact_tuple[0],
            subject=fact_tuple[1],
            object=fact_tuple[2]
        )


@dataclass
class EntityMetadata:
    """Metadata about an entity in the knowledge graph."""
    name: str
    file_path: str
    frontmatter: dict
    has_frontmatter: bool = True
