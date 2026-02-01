"""
Simple Example: Reasoner on Obsidian Graph

This example demonstrates the basic usage of Semantica Hawksight's Reasoner
on a graph structure similar to what you would find in an Obsidian vault.
"""

from semantica.reasoning import Reasoner, Rule

# Initialize the reasoner
reasoner = Reasoner()

# Define logical rules for ML model relationships

# Rule 1: Grandparent/Ancestor Rule
# If A is parent of B, and B is parent of C, then A is ancestor of C
reasoner.add_rule(Rule(
    name="ancestor_rule",
    conditions=["?a PARENT_OF ?b", "?b PARENT_OF ?c"],
    conclusions=["?a ANCESTOR_OF ?c"]
))

# Rule 2: Type Transitivity
# If A is a B, and B is a C, then A is also a C
reasoner.add_rule(Rule(
    name="type_transitivity",
    conditions=["?a IS_A ?b", "?b IS_A ?c"],
    conclusions=["?a IS_ALSO_A ?c"]
))

# Rule 3: Usage Inheritance
# If A is a B, and B is used for C, then A can be used for C
reasoner.add_rule(Rule(
    name="usage_inheritance",
    conditions=["?a IS_A ?b", "?b USED_FOR ?c"],
    conclusions=["?a CAN_BE_USED_FOR ?c"]
))

# Rule 4: Model Category Membership
# If A is a B, and C is parent of B, then A belongs to C category
reasoner.add_rule(Rule(
    name="category_membership",
    conditions=["?a IS_A ?b", "?c PARENT_OF ?b"],
    conclusions=["?a BELONGS_TO_CATEGORY ?c"]
))

# Initial facts extracted from Obsidian vault structure
# (These would normally be extracted from the YAML frontmatter of .md files)
facts = [
    # Hierarchical structure (parent relationships)
    "Model PARENT_OF Classification",
    "Model PARENT_OF Regression",
    "Model PARENT_OF Clustering",

    # Specific models and their types
    "Logistic_Regression IS_A Classification",
    "Linear_Regression IS_A Regression",
    "Polynomial_Regression IS_A Regression",
    "KNN IS_A Clustering",
    "KNN IS_A Classification",

    # Usage relationships
    "Regression USED_FOR Prediction",
    "Classification USED_FOR Prediction",

    # Optimization algorithms
    "Gradient_Descent IS_ALGORITHM_FOR Optimization",
]

print("=" * 80)
print("SIMPLE OBSIDIAN GRAPH REASONER EXAMPLE")
print("=" * 80)
print("\n📚 INITIAL FACTS (from Obsidian vault):")
print("-" * 80)
for fact in facts:
    print(f"  • {fact}")

# Infer new facts
print("\n🧠 APPLYING REASONING RULES...")
print("-" * 80)
new_facts = reasoner.infer_facts(facts)

print("\n✨ INFERRED FACTS:")
print("-" * 80)
if new_facts:
    for fact in sorted(set(new_facts)):
        print(f"  ✓ {fact}")
else:
    print("  (No new facts inferred)")

# Demonstrate specific inferences
print("\n" + "=" * 80)
print("INTERPRETATION:")
print("=" * 80)

ancestor_facts = [f for f in new_facts if "ANCESTOR_OF" in f]
if ancestor_facts:
    print("\n1. Discovered Hierarchies:")
    for fact in sorted(set(ancestor_facts)):
        parts = fact.split()
        print(f"   → {parts[0]} is an ancestor of {parts[2]}")

category_facts = [f for f in new_facts if "BELONGS_TO_CATEGORY" in f]
if category_facts:
    print("\n2. Category Memberships:")
    for fact in sorted(set(category_facts)):
        parts = fact.split()
        print(f"   → {parts[0]} belongs to {parts[2]} category")

usage_facts = [f for f in new_facts if "CAN_BE_USED_FOR" in f]
if usage_facts:
    print("\n3. Usage Capabilities:")
    for fact in sorted(set(usage_facts)):
        parts = fact.split()
        print(f"   → {parts[0]} can be used for {parts[2]}")

print("\n" + "=" * 80)
print("💡 INSIGHTS:")
print("=" * 80)
print("""
The reasoner has automatically inferred relationships that weren't explicitly
stated in the Obsidian vault. For example:
- It discovered that specific models belong to the broader Model category
- It propagated usage information from parent categories to specific models
- It built the complete hierarchical structure

This allows for richer queries and better understanding of the knowledge graph!
""")
print("=" * 80)
