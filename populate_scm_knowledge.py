#!/usr/bin/env python3
"""
Populate Structural Causal Models Knowledge Base

Creates a comprehensive knowledge graph about Structural Causal Models
with proper relationships for the Obsidian reasoner.
"""

import os
from pathlib import Path
import yaml


class SCMKnowledgeBuilder:
    """Builds a knowledge base about Structural Causal Models."""

    def __init__(self, output_dir: str):
        """
        Initialize the builder.

        Args:
            output_dir: Directory where markdown files will be created
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.created_files = []

    def create_file(self, filename: str, frontmatter: dict, content: str = ""):
        """Create a markdown file with YAML frontmatter."""
        filepath = self.output_dir / f"{filename}.md"

        yaml_content = yaml.dump(frontmatter, default_flow_style=False,
                                allow_unicode=True, sort_keys=False)

        full_content = f"---\n{yaml_content}---\n\n{content}"

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(full_content)

        self.created_files.append(filename)
        print(f"  ✓ Created {filename}.md")

    def build_core_concepts(self):
        """Create files for core SCM concepts."""
        print("\n[1/6] Creating core concepts...")

        # Main overview
        self.create_file(
            "Structural Causal Model",
            {
                "tags": ["overview", "causal-inference"],
                "type": "framework"
            },
            """A Structural Causal Model (SCM) is a mathematical framework for representing and reasoning about causality. It combines:

- **Graphical Models**: Directed acyclic graphs (DAGs) representing causal relationships
- **Structural Equations**: Mathematical equations defining how variables relate
- **Interventions**: Formal operations modeling external manipulations
- **Counterfactual Reasoning**: Framework for "what if" questions

## Key Components

An SCM consists of:
1. Endogenous variables (affected by the model)
2. Exogenous variables (external influences)
3. Structural equations linking variables
4. A causal graph showing dependencies

## Framework

SCM = (U, V, F) where:
- U: Exogenous (background) variables
- V: Endogenous (observable) variables
- F: Set of structural equations

## Applications

- Policy evaluation and decision making
- Root cause analysis
- Mediation and moderation analysis
- Fairness assessment in AI systems
"""
        )

        # Causality
        self.create_file(
            "Causality",
            {
                "tags": ["fundamental-concept"],
                "type": "concept",
                "parent": "[[Philosophy of Science]]"
            },
            """Causality is the relationship between causes and effects. In the context of causal inference:

- **Causal Relationship**: X causes Y if changing X leads to changes in Y
- **Correlation vs Causation**: Correlation does not imply causation
- **Counterfactual Definition**: X caused Y if Y would not have occurred without X

## Frameworks

- [[Structural Causal Model]]: Pearl's graphical approach
- [[Rubin Causal Model]]: Potential outcomes framework
- [[Granger Causality]]: Time-series causality
"""
        )

        # Causal Inference
        self.create_file(
            "Causal Inference",
            {
                "parent": "[[Causality]]",
                "tags": ["methodology"],
                "type": "field",
                "related": ["[[Statistics]]", "[[Machine Learning]]"]
            },
            """Causal inference is the process of determining causal relationships from data.

## Core Challenges

- **Confounding**: Variables affecting both cause and effect
- **Selection Bias**: Non-random sample selection
- **Reverse Causation**: Effect influences the cause

## Methods

- [[Randomized Controlled Trial]]: Gold standard for causal inference
- [[Instrumental Variables]]: Using external instruments
- [[Propensity Score Matching]]: Balancing treatment groups
- [[Difference-in-Differences]]: Before-after comparisons
- [[Regression Discontinuity]]: Exploiting cutoff thresholds
"""
        )

    def build_graph_concepts(self):
        """Create files for graph-related concepts."""
        print("\n[2/6] Creating graph concepts...")

        self.create_file(
            "Directed Acyclic Graph",
            {
                "parent": "[[Graph Theory]]",
                "tags": ["graph", "data-structure"],
                "type": "structure",
                "used_in": "[[Structural Causal Model]]"
            },
            """A Directed Acyclic Graph (DAG) is a graph with directed edges and no cycles.

## Properties

- **Directed**: Edges have a direction (A → B)
- **Acyclic**: No path from a node back to itself
- **Topological Ordering**: Nodes can be linearly ordered

## In Causal Models

DAGs represent causal relationships where:
- Nodes = Variables
- Edges = Direct causal effects
- Paths = Causal pathways

## Key Concepts

- [[d-separation]]: Graphical criterion for conditional independence
- [[Collider]]: Node with multiple incoming edges
- [[Confounder]]: Common cause of two variables
"""
        )

        self.create_file(
            "Causal Graph",
            {
                "parent": "[[Directed Acyclic Graph]]",
                "tags": ["causal-inference", "graph"],
                "type": "representation",
                "part_of": "[[Structural Causal Model]]"
            },
            """A causal graph is a DAG where edges represent direct causal relationships.

## Components

- **Nodes**: Variables in the system
- **Directed Edges**: X → Y means X causes Y
- **Paths**: Sequences of edges showing causal flow

## Types of Paths

- **Chain**: X → M → Y (mediation)
- **Fork**: X ← Z → Y (confounding)
- **Collider**: X → Z ← Y (selection bias)

## Applications

- Identifying confounders
- Determining adjustment sets
- Planning interventions
"""
        )

        self.create_file(
            "d-separation",
            {
                "parent": "[[Causal Graph]]",
                "tags": ["graph-theory", "independence"],
                "type": "criterion"
            },
            """d-separation (directed separation) is a graphical criterion for conditional independence in DAGs.

## Definition

Two sets of nodes X and Y are d-separated by Z if all paths between X and Y are blocked by Z.

## Blocking Rules

A path is blocked if it contains:
1. **Chain** X → M → Y with M in Z
2. **Fork** X ← M → Y with M in Z
3. **Collider** X → M ← Y with M and descendants NOT in Z

## Applications

- Identifying conditional independencies
- Determining minimal adjustment sets
- Testing causal assumptions
"""
        )

    def build_methods_and_techniques(self):
        """Create files for causal inference methods."""
        print("\n[3/6] Creating methods and techniques...")

        self.create_file(
            "do-calculus",
            {
                "parent": "[[Structural Causal Model]]",
                "tags": ["method", "intervention"],
                "type": "calculus",
                "created_by": "[[Judea Pearl]]"
            },
            """The do-calculus is a set of inference rules for causal reasoning developed by Judea Pearl.

## do-operator

- **Observation**: P(Y|X=x) - seeing X=x
- **Intervention**: P(Y|do(X=x)) - setting X=x externally

## Three Rules

1. **Insertion/deletion of observations**
2. **Action/observation exchange**
3. **Insertion/deletion of actions**

## Applications

- Computing causal effects from observational data
- Determining identifiability of causal queries
- Deriving adjustment formulas
"""
        )

        self.create_file(
            "Backdoor Criterion",
            {
                "parent": "[[Causal Graph]]",
                "tags": ["criterion", "confounding"],
                "type": "method",
                "used_for": "[[Causal Inference]]"
            },
            """The backdoor criterion identifies sufficient sets of variables to control for confounding.

## Definition

A set Z satisfies the backdoor criterion relative to (X, Y) if:
1. Z blocks all backdoor paths from X to Y
2. Z contains no descendants of X

## Backdoor Path

A path from X to Y with an arrow into X: X ← ... → Y

## Applications

- Identifying valid adjustment sets
- Controlling for confounding
- Enabling causal effect estimation
"""
        )

        self.create_file(
            "Instrumental Variables",
            {
                "parent": "[[Causal Inference]]",
                "tags": ["method", "econometrics"],
                "type": "technique",
                "used_for": "[[Confounding Control]]"
            },
            """Instrumental variables (IV) is a method for estimating causal effects in the presence of unobserved confounding.

## Requirements

An instrument Z must:
1. **Relevance**: Z affects treatment X
2. **Exclusion**: Z affects outcome Y only through X
3. **Independence**: Z is independent of confounders

## Estimation

Causal effect = Cov(Y,Z) / Cov(X,Z)

## Examples

- Randomized encouragement designs
- Natural experiments
- Mendelian randomization (genetics as IV)
"""
        )

        self.create_file(
            "Propensity Score Matching",
            {
                "parent": "[[Causal Inference]]",
                "tags": ["method", "matching"],
                "type": "technique"
            },
            """Propensity score matching balances treatment and control groups on observed covariates.

## Propensity Score

Probability of treatment given covariates: e(X) = P(T=1|X)

## Methods

- **Nearest neighbor matching**
- **Caliper matching**
- **Stratification**
- **Inverse probability weighting**

## Assumptions

- Unconfoundedness (no unmeasured confounding)
- Common support (overlap)
- Correct propensity score specification
"""
        )

    def build_advanced_concepts(self):
        """Create files for advanced SCM concepts."""
        print("\n[4/6] Creating advanced concepts...")

        self.create_file(
            "Counterfactual",
            {
                "parent": "[[Structural Causal Model]]",
                "tags": ["reasoning", "what-if"],
                "type": "concept"
            },
            """Counterfactuals are statements about what would have happened under different conditions.

## Definition

"What would Y have been, had X been x?"
Notation: Y_x or Y(x)

## Three Levels of Causation (Pearl's Ladder)

1. **Association**: P(Y|X) - observation
2. **Intervention**: P(Y|do(X)) - doing
3. **Counterfactual**: P(Y_x|X',Y') - imagining

## Applications

- Individual-level causal effects
- Fairness in machine learning
- Legal reasoning
- Policy analysis
"""
        )

        self.create_file(
            "Mediation Analysis",
            {
                "parent": "[[Causal Inference]]",
                "tags": ["method", "mechanisms"],
                "type": "analysis",
                "uses": "[[Structural Causal Model]]"
            },
            """Mediation analysis studies how causes produce effects through intermediate variables (mediators).

## Framework

X → M → Y

- X: Treatment/exposure
- M: Mediator
- Y: Outcome

## Effects

- **Total Effect**: Overall effect of X on Y
- **Direct Effect**: Effect not through M
- **Indirect Effect**: Effect through M

## Applications

- Understanding causal mechanisms
- Intervention design
- Process evaluation
"""
        )

        self.create_file(
            "Confounder",
            {
                "parent": "[[Causal Graph]]",
                "tags": ["bias", "confounding"],
                "type": "pattern"
            },
            """A confounder is a variable that influences both treatment and outcome, creating spurious association.

## Structure

Z → X
Z → Y

This creates a backdoor path: X ← Z → Y

## Control Methods

- [[Randomization]]: Random assignment eliminates confounding
- [[Adjustment]]: Conditioning on confounders
- [[Instrumental Variables]]: Using external instruments
- [[Propensity Score Matching]]: Balancing on confounders

## Types

- **Observed**: Measured confounders
- **Unobserved**: Hidden confounders
"""
        )

        self.create_file(
            "Collider",
            {
                "parent": "[[Causal Graph]]",
                "tags": ["bias", "selection"],
                "type": "pattern"
            },
            """A collider is a variable caused by two or more variables.

## Structure

X → M ← Y

## Collider Bias

Conditioning on a collider creates spurious association between its causes.

## Examples

- Selection bias
- Berkson's paradox
- Sample selection

## Rule

Never condition on a collider when estimating causal effects!
"""
        )

    def build_researchers(self):
        """Create files for key researchers."""
        print("\n[5/6] Creating researcher profiles...")

        self.create_file(
            "Judea Pearl",
            {
                "tags": ["researcher", "ai", "causality"],
                "type": "person",
                "field": ["[[Artificial Intelligence]]", "[[Causal Inference]]"],
                "known_for": ["[[Structural Causal Model]]", "[[do-calculus]]"]
            },
            """Judea Pearl is a computer scientist and philosopher, winner of the Turing Award (2011).

## Contributions

- Developed [[Structural Causal Model]] framework
- Created [[do-calculus]] for causal reasoning
- [[Bayesian Networks]] for probabilistic reasoning
- Causal hierarchy (ladder of causation)

## Key Works

- "Causality: Models, Reasoning, and Inference" (2000)
- "The Book of Why" (2018) - popular science
- Causal inference in statistics: A primer (2016)

## Impact

Revolutionized causal inference by providing:
- Graphical representation of causality
- Mathematical tools for intervention
- Framework for counterfactual reasoning
"""
        )

        self.create_file(
            "Donald Rubin",
            {
                "tags": ["researcher", "statistics"],
                "type": "person",
                "field": ["[[Statistics]]", "[[Causal Inference]]"],
                "known_for": ["[[Rubin Causal Model]]", "[[Propensity Score Matching]]"]
            },
            """Donald Rubin is a statistician known for the Rubin Causal Model (potential outcomes framework).

## Contributions

- [[Rubin Causal Model]]: Potential outcomes framework
- [[Propensity Score Matching]]: Balancing treatment groups
- Multiple imputation for missing data
- Bayesian statistics applications

## Potential Outcomes Framework

- Y(1): Potential outcome under treatment
- Y(0): Potential outcome under control
- Causal effect: Y(1) - Y(0)

## Key Insight

The fundamental problem of causal inference: We never observe both Y(1) and Y(0) for the same unit.
"""
        )

    def build_applications(self):
        """Create files for applications."""
        print("\n[6/6] Creating application areas...")

        self.create_file(
            "Fairness in Machine Learning",
            {
                "parent": "[[Machine Learning]]",
                "tags": ["ethics", "ai", "fairness"],
                "type": "application",
                "uses": ["[[Structural Causal Model]]", "[[Counterfactual]]"]
            },
            """Causal inference provides formal frameworks for fairness in ML systems.

## Causal Fairness Criteria

- **Counterfactual Fairness**: Decision unchanged in counterfactual world
- **Path-Specific Fairness**: Blocking unfair causal pathways
- **Interventional Fairness**: Fair under hypothetical interventions

## Advantages over Statistical Fairness

- Distinguishes legitimate from illegitimate influences
- Handles proxy variables properly
- Provides actionable interventions

## Tools

- [[Causal Graph]]: Represents fairness assumptions
- [[Counterfactual]]: Individual-level fairness
- [[Mediation Analysis]]: Identifying discrimination pathways
"""
        )

        self.create_file(
            "Policy Evaluation",
            {
                "parent": "[[Causal Inference]]",
                "tags": ["application", "policy", "economics"],
                "type": "application",
                "uses": "[[Structural Causal Model]]"
            },
            """Using causal inference to evaluate the impact of policies and interventions.

## Questions

- What is the effect of a policy?
- Who benefits most?
- What are the mechanisms?
- What are unintended consequences?

## Methods

- [[Randomized Controlled Trial]]: Experimental evaluation
- [[Difference-in-Differences]]: Before-after comparisons
- [[Regression Discontinuity]]: Exploiting cutoffs
- [[Instrumental Variables]]: Natural experiments

## Challenges

- External validity
- Compliance and attrition
- Spillover effects
- Long-term effects
"""
        )

        self.create_file(
            "Root Cause Analysis",
            {
                "parent": "[[Causal Inference]]",
                "tags": ["application", "diagnostics"],
                "type": "application",
                "uses": ["[[Structural Causal Model]]", "[[Counterfactual]]"]
            },
            """Identifying the fundamental causes of observed effects or failures.

## Approach

1. Build [[Causal Graph]] of system
2. Observe effect/failure
3. Trace back through causal pathways
4. Identify root causes using [[Counterfactual]] reasoning

## Applications

- System debugging
- Incident analysis
- Quality control
- Medical diagnosis

## SCM Advantages

- Distinguishes symptoms from causes
- Identifies multiple contributing factors
- Suggests effective interventions
"""
        )

    def build_all(self):
        """Build the complete knowledge base."""
        print("=" * 80)
        print("STRUCTURAL CAUSAL MODELS KNOWLEDGE BASE BUILDER")
        print("=" * 80)
        print(f"\nOutput directory: {self.output_dir}\n")

        self.build_core_concepts()
        self.build_graph_concepts()
        self.build_methods_and_techniques()
        self.build_advanced_concepts()
        self.build_researchers()
        self.build_applications()

        print("\n" + "=" * 80)
        print("BUILD SUMMARY")
        print("=" * 80)
        print(f"Total files created: {len(self.created_files)}")
        print(f"Output directory: {self.output_dir}")
        print("\nCreated files:")
        for filename in sorted(self.created_files):
            print(f"  • {filename}")
        print("\n" + "=" * 80)


def main():
    """Main function."""
    builder = SCMKnowledgeBuilder("graph/CausalInference")
    builder.build_all()
    print("\n✓ Knowledge base created successfully!")
    print("\nNext steps:")
    print("  1. Run the reasoner: python demo_reasoner.py")
    print("  2. Explore the graph in Obsidian")
    print("=" * 80)


if __name__ == "__main__":
    main()
