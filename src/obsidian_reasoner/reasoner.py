"""
Graph reasoning engine for inferring new facts.
"""

from collections import defaultdict
from typing import List, Dict, Set

from .models import Fact


class GraphReasoner:
    """
    Applies logical reasoning rules to infer new facts from existing ones.

    Implements transitive closure and compositional reasoning rules
    for knowledge graph relationships.
    """

    def __init__(self):
        """Initialize the reasoner."""
        self.rules = [
            self._rule_transitive_parent,
            self._rule_transitive_part_of,
            self._rule_contributed_to,
            self._rule_indirect_uses,
            self._rule_domain_encompasses,
            self._rule_theory_applied,
        ]

    def infer(self, facts: List[Fact]) -> List[Fact]:
        """
        Apply reasoning rules to infer new facts.

        Args:
            facts: List of known facts

        Returns:
            List of newly inferred facts
        """
        inferred = set()

        # Build indexes for efficient lookup
        indexes = self._build_indexes(facts)

        # Apply each reasoning rule
        for rule in self.rules:
            new_facts = rule(indexes)
            inferred.update(new_facts)

        return [Fact.from_tuple(f) for f in inferred]

    def _build_indexes(self, facts: List[Fact]) -> Dict[str, Dict]:
        """
        Build indexes for efficient fact lookup.

        Args:
            facts: List of facts to index

        Returns:
            Dictionary of indexes by relation type
        """
        indexes = {
            'parent_of': defaultdict(set),
            'part_of': defaultdict(set),
            'uses': defaultdict(set),
            'created': defaultdict(set),
            'is_a': defaultdict(set),
        }

        for fact in facts:
            relation_lower = fact.relation.lower()

            if 'parent' in relation_lower:
                indexes['parent_of'][fact.subject].add(fact.object)
            elif 'part_of' in relation_lower:
                indexes['part_of'][fact.subject].add(fact.object)
            elif 'uses' in relation_lower:
                indexes['uses'][fact.subject].add(fact.object)
            elif 'created' in relation_lower:
                indexes['created'][fact.subject].add(fact.object)
            elif 'is_a' in relation_lower:
                indexes['is_a'][fact.subject].add(fact.object)

        return indexes

    def _rule_transitive_parent(self, indexes: Dict) -> Set[tuple]:
        """
        Rule 1: Transitive PARENT_OF → ANCESTOR_OF
        If A parent of B, and B parent of C, then A ancestor of C.
        """
        inferred = set()
        parent_of = indexes['parent_of']

        for grandparent, children in parent_of.items():
            for child in children:
                if child in parent_of:
                    for grandchild in parent_of[child]:
                        inferred.add(('ANCESTOR_OF', grandparent, grandchild))

        return inferred

    def _rule_transitive_part_of(self, indexes: Dict) -> Set[tuple]:
        """
        Rule 2: Transitive PART_OF
        If A part of B, and B part of C, then A transitively part of C.
        """
        inferred = set()
        part_of = indexes['part_of']

        for part, wholes in part_of.items():
            for whole in wholes:
                if whole in part_of:
                    for larger_whole in part_of[whole]:
                        inferred.add(('TRANSITIVELY_PART_OF', part, larger_whole))

        return inferred

    def _rule_contributed_to(self, indexes: Dict) -> Set[tuple]:
        """
        Rule 3: Created X, X part of Y → Contributed to Y
        If Creator created X, and X is part of Y, then Creator contributed to Y.
        """
        inferred = set()
        created = indexes['created']
        part_of = indexes['part_of']

        for creator, creations in created.items():
            for creation in creations:
                if creation in part_of:
                    for whole in part_of[creation]:
                        inferred.add(('CONTRIBUTED_TO', creator, whole))

        return inferred

    def _rule_indirect_uses(self, indexes: Dict) -> Set[tuple]:
        """
        Rule 4: Uses X, X uses Y → Indirectly uses Y
        If A uses X, and X uses Y, then A indirectly uses Y.
        """
        inferred = set()
        uses = indexes['uses']

        for user, tools in uses.items():
            for tool in tools:
                if tool in uses:
                    for subtool in uses[tool]:
                        inferred.add(('INDIRECTLY_USES', user, subtool))

        return inferred

    def _rule_domain_encompasses(self, indexes: Dict) -> Set[tuple]:
        """
        Rule 5: Parent of X, X part of Y → Domain encompasses Y
        If A is parent of X, and X is part of Y, then A's domain encompasses Y.
        """
        inferred = set()
        parent_of = indexes['parent_of']
        part_of = indexes['part_of']

        for parent, children in parent_of.items():
            for child in children:
                if child in part_of:
                    for whole in part_of[child]:
                        inferred.add(('DOMAIN_ENCOMPASSES', parent, whole))

        return inferred

    def _rule_theory_applied(self, indexes: Dict) -> Set[tuple]:
        """
        Rule 6: Created by X, Used by Y → Theory applied by Y
        If X created Theory, and Y uses Theory, then X's theory is applied by Y.
        """
        inferred = set()
        created = indexes['created']
        uses = indexes['uses']

        for creator, creations in created.items():
            for creation in creations:
                for user, used_items in uses.items():
                    if creation in used_items:
                        inferred.add(('THEORY_APPLIED_BY', creator, user))

        return inferred
