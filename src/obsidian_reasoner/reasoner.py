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
            # Original domain-specific rules
            self._rule_transitive_parent,
            self._rule_transitive_part_of,
            self._rule_contributed_to,
            self._rule_indirect_uses,
            self._rule_domain_encompasses,
            self._rule_theory_applied,
            # New OWL-inspired rules
            self._rule_symmetric_collaboration,
            self._rule_inverse_properties,
            self._rule_methodology_inheritance,
            self._rule_field_contribution,
            self._rule_cross_domain_bridge,
            self._rule_prerequisite_chain,
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
            'works_in': defaultdict(set),
            'coauthor_of': defaultdict(set),
            'collaborates_with': defaultdict(set),
            'all_facts': [],  # Store all facts for comprehensive reasoning
        }

        for fact in facts:
            relation_lower = fact.relation.lower()

            # Store all facts for access by new rules
            indexes['all_facts'].append(fact)

            # Index by specific relationship types
            if 'parent' in relation_lower:
                indexes['parent_of'][fact.subject].add(fact.object)
            elif 'part_of' in relation_lower or 'part-of' in relation_lower:
                indexes['part_of'][fact.subject].add(fact.object)
            elif 'uses' in relation_lower or 'use' in relation_lower:
                indexes['uses'][fact.subject].add(fact.object)
            elif 'created' in relation_lower:
                indexes['created'][fact.subject].add(fact.object)
            elif 'is_a' in relation_lower or 'is-a' in relation_lower:
                indexes['is_a'][fact.subject].add(fact.object)
            elif 'works_in' in relation_lower or 'field' in relation_lower:
                indexes['works_in'][fact.subject].add(fact.object)
            elif 'coauthor' in relation_lower:
                indexes['coauthor_of'][fact.subject].add(fact.object)
            elif 'collaborates' in relation_lower:
                indexes['collaborates_with'][fact.subject].add(fact.object)

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

    # =========================================================================
    # OWL-INSPIRED INFERENCE RULES
    # =========================================================================

    def _rule_symmetric_collaboration(self, indexes: Dict) -> Set[tuple]:
        """
        Rule 7: Symmetric Collaboration (OWL owl:SymmetricProperty)
        If A coauthor_of B → B coauthor_of A
        If A collaborates_with B → B collaborates_with A

        Implements symmetric property reasoning from OWL.
        """
        inferred = set()

        # Handle coauthor_of symmetry
        for person_a, coauthors in indexes['coauthor_of'].items():
            for person_b in coauthors:
                # Add reverse relationship
                inferred.add(('COAUTHOR_OF', person_b, person_a))

        # Handle collaborates_with symmetry
        for person_a, collaborators in indexes['collaborates_with'].items():
            for person_b in collaborators:
                # Add reverse relationship
                inferred.add(('COLLABORATES_WITH', person_b, person_a))

        return inferred

    def _rule_inverse_properties(self, indexes: Dict) -> Set[tuple]:
        """
        Rule 8: Inverse Properties (OWL owl:inverseOf)
        Automatically generate inverse relationships:
        - created/created_by
        - uses/used_by
        - part_of/has_part

        Implements inverse property reasoning from OWL.
        """
        inferred = set()

        # created → created_by (inverse)
        for creator, creations in indexes['created'].items():
            for creation in creations:
                inferred.add(('CREATED_BY', creation, creator))

        # uses → used_by (inverse)
        for user, tools in indexes['uses'].items():
            for tool in tools:
                inferred.add(('USED_BY', tool, user))

        # part_of → has_part (inverse)
        for part, wholes in indexes['part_of'].items():
            for whole in wholes:
                inferred.add(('HAS_PART', whole, part))

        return inferred

    def _rule_methodology_inheritance(self, indexes: Dict) -> Set[tuple]:
        """
        Rule 9: Methodology Inheritance (OWL property chain reasoning)
        If Method is_a ParentMethod, and ParentMethod uses Technique
        → Method inherits_methodology_from Technique

        Implements property chain reasoning: is_a ∘ uses → inherits_methodology_from
        """
        inferred = set()
        is_a = indexes['is_a']
        uses = indexes['uses']

        for method, parent_methods in is_a.items():
            for parent in parent_methods:
                if parent in uses:
                    for technique in uses[parent]:
                        inferred.add(('INHERITS_METHODOLOGY_FROM', method, technique))

        return inferred

    def _rule_field_contribution(self, indexes: Dict) -> Set[tuple]:
        """
        Rule 10: Field Contribution (Domain-specific compositional rule)
        If Person created Method, and Method part_of Field
        → Person contributed_to_field Field

        More specific than CONTRIBUTED_TO, focusing on field-level impact.
        """
        inferred = set()
        created = indexes['created']
        works_in = indexes['works_in']

        # Find all methods and their fields
        for creator, creations in created.items():
            for creation in creations:
                # Check if this creation is associated with a field
                if creation in works_in:
                    for field in works_in[creation]:
                        inferred.add(('CONTRIBUTED_TO_FIELD', creator, field))

        return inferred

    def _rule_cross_domain_bridge(self, indexes: Dict) -> Set[tuple]:
        """
        Rule 11: Cross-Domain Bridges (Multi-field integration detection)
        If Method uses Theory1 and Theory2, and Theory1 works_in Field1,
        and Theory2 works_in Field2 (Field1 ≠ Field2)
        → Method bridges_domains Field1, Field2

        Identifies methods that integrate multiple fields.
        """
        inferred = set()
        uses = indexes['uses']
        works_in = indexes['works_in']

        for method, theories in uses.items():
            # Find all fields involved through theories used
            fields_involved = set()
            for theory in theories:
                if theory in works_in:
                    fields_involved.update(works_in[theory])

            # If multiple fields, this method bridges them
            if len(fields_involved) >= 2:
                fields_list = sorted(list(fields_involved))
                # Create bridge relationships to each field
                for field in fields_list:
                    inferred.add(('BRIDGES_DOMAIN', method, field))

        return inferred

    def _rule_prerequisite_chain(self, indexes: Dict) -> Set[tuple]:
        """
        Rule 12: Prerequisite Chain (Learning path reasoning)
        If Concept A uses Concept B, and B uses Concept C
        → Understanding A requires_understanding C

        Creates transitive dependency chains for learning paths.
        Similar to transitive uses, but focuses on prerequisite knowledge.
        """
        inferred = set()
        uses = indexes['uses']

        # Build transitive closure of prerequisites
        for concept_a, direct_deps in uses.items():
            for concept_b in direct_deps:
                if concept_b in uses:
                    for concept_c in uses[concept_b]:
                        # concept_a needs concept_b, concept_b needs concept_c
                        # Therefore, understanding concept_a requires understanding concept_c
                        inferred.add(('REQUIRES_UNDERSTANDING', concept_a, concept_c))

        return inferred
