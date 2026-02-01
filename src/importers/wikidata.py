#!/usr/bin/env python3
"""
Wikidata Structural Causal Models Importer

This script queries Wikidata for knowledge about Structural Causal Models (SCM)
and related concepts, then creates Obsidian markdown files with proper relationships.
"""

import os
import re
import json
from pathlib import Path
from typing import List, Dict, Set, Optional
from SPARQLWrapper import SPARQLWrapper, JSON
import yaml


class WikidataImporter:
    """
    Imports knowledge about Structural Causal Models from Wikidata
    into an Obsidian vault with proper relationships.
    """

    WIKIDATA_ENDPOINT = "https://query.wikidata.org/sparql"

    def __init__(self, output_dir: str):
        """
        Initialize the importer.

        Args:
            output_dir: Directory where markdown files will be created
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.sparql = SPARQLWrapper(self.WIKIDATA_ENDPOINT)
        self.sparql.setReturnFormat(JSON)
        self.created_files = set()

    def sanitize_filename(self, name: str) -> str:
        """
        Sanitize a string to be used as a filename.

        Args:
            name: Original name

        Returns:
            Sanitized filename
        """
        # Replace invalid characters
        name = re.sub(r'[<>:"/\\|?*]', '', name)
        # Replace multiple spaces with single space
        name = re.sub(r'\s+', ' ', name)
        # Trim and return
        return name.strip()

    def query_wikidata(self, query: str) -> List[Dict]:
        """
        Execute a SPARQL query against Wikidata.

        Args:
            query: SPARQL query string

        Returns:
            List of result bindings
        """
        try:
            self.sparql.setQuery(query)
            results = self.sparql.query().convert()
            return results["results"]["bindings"]
        except Exception as e:
            print(f"Error querying Wikidata: {e}")
            return []

    def get_structural_causal_models_data(self) -> List[Dict]:
        """
        Query Wikidata for Structural Causal Models and related concepts.

        Returns:
            List of entities with their properties
        """
        query = """
        SELECT DISTINCT ?item ?itemLabel ?itemDescription ?superclass ?superclassLabel
               ?partOf ?partOfLabel ?subjectOf ?subjectOfLabel
        WHERE {
          # Start with Structural Causal Model and related concepts
          VALUES ?searchTerm {
            wd:Q7628072   # Structural Causal Model (if exists)
          }

          {
            # Direct item
            ?item wdt:P31|wdt:P279* ?searchTerm .
          } UNION {
            # Or search by label/description
            ?item rdfs:label|schema:description ?label .
            FILTER(CONTAINS(LCASE(?label), "causal model") ||
                   CONTAINS(LCASE(?label), "structural equation") ||
                   CONTAINS(LCASE(?label), "causal inference"))
            FILTER(LANG(?label) = "en")
          }

          # Get superclass/subclass relationships
          OPTIONAL { ?item wdt:P279 ?superclass . }

          # Get part-of relationships
          OPTIONAL { ?item wdt:P361 ?partOf . }

          # Get subject matter
          OPTIONAL { ?item wdt:P921 ?subjectOf . }

          # Get labels
          SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }

          # Filter to keep relevant items
          FILTER(?item != wd:Q7628072)
        }
        LIMIT 100
        """

        return self.query_wikidata(query)

    def get_causal_inference_concepts(self) -> List[Dict]:
        """
        Query Wikidata for causal inference related concepts.

        Returns:
            List of causal inference concepts
        """
        query = """
        SELECT DISTINCT ?item ?itemLabel ?itemDescription
               ?superclass ?superclassLabel ?field ?fieldLabel
        WHERE {
          # Key concepts in causal inference
          VALUES ?topic {
            wd:Q1137724    # Causality
            wd:Q1195958    # Causal inference
            wd:Q842346     # Directed acyclic graph
            wd:Q1053745    # Statistical model
          }

          {
            ?item wdt:P279* ?topic .
          } UNION {
            ?item wdt:P31 ?topic .
          } UNION {
            ?item wdt:P361 ?topic .
          }

          OPTIONAL { ?item wdt:P279 ?superclass . }
          OPTIONAL { ?item wdt:P101 ?field . }

          SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
        }
        LIMIT 100
        """

        return self.query_wikidata(query)

    def get_researchers_and_methods(self) -> List[Dict]:
        """
        Query Wikidata for researchers and methods in causal inference.

        Returns:
            List of researchers and methods
        """
        query = """
        SELECT DISTINCT ?item ?itemLabel ?itemDescription
               ?type ?typeLabel ?field ?fieldLabel
        WHERE {
          {
            # Methods and techniques
            ?item wdt:P31 wd:Q2695280 .  # Statistical method
            ?item rdfs:label|schema:description ?label .
            FILTER(CONTAINS(LCASE(?label), "causal") ||
                   CONTAINS(LCASE(?label), "inference") ||
                   CONTAINS(LCASE(?label), "propensity"))
            FILTER(LANG(?label) = "en")
          } UNION {
            # Researchers (notable people in causal inference)
            VALUES ?researcher {
              wd:Q92743      # Judea Pearl
              wd:Q92760      # Donald Rubin
            }
            ?item wdt:P31 wd:Q5 .
            ?item wdt:P106|wdt:P101 ?field .
            {
              ?item wdt:P737 ?researcher .
            } UNION {
              ?item wdt:P802 ?researcher .
            } UNION {
              BIND(?researcher AS ?item)
            }
          }

          OPTIONAL { ?item wdt:P31 ?type . }
          OPTIONAL { ?item wdt:P101 ?field . }

          SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
        }
        LIMIT 50
        """

        return self.query_wikidata(query)

    def create_markdown_file(self, name: str, description: str,
                            frontmatter: Dict, content: str = "") -> Path:
        """
        Create an Obsidian markdown file with YAML frontmatter.

        Args:
            name: Name of the entity
            description: Description text
            frontmatter: Dictionary of frontmatter properties
            content: Additional markdown content

        Returns:
            Path to created file
        """
        filename = self.sanitize_filename(name) + ".md"
        filepath = self.output_dir / filename

        # Build frontmatter YAML
        yaml_content = yaml.dump(frontmatter, default_flow_style=False, allow_unicode=True)

        # Build full content
        full_content = f"---\n{yaml_content}---\n\n"

        if description:
            full_content += f"{description}\n\n"

        if content:
            full_content += content + "\n"

        # Write file
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(full_content)

        self.created_files.add(filename)
        return filepath

    def extract_wikidata_id(self, uri: str) -> str:
        """
        Extract Wikidata ID from a URI.

        Args:
            uri: Wikidata URI

        Returns:
            Wikidata ID (e.g., Q12345)
        """
        match = re.search(r'/(Q\d+)$', uri)
        return match.group(1) if match else ""

    def process_entity(self, entity: Dict) -> Optional[Path]:
        """
        Process a Wikidata entity and create a markdown file.

        Args:
            entity: Entity data from SPARQL query

        Returns:
            Path to created file or None if skipped
        """
        # Extract basic info
        item_uri = entity.get("item", {}).get("value", "")
        name = entity.get("itemLabel", {}).get("value", "")
        description = entity.get("itemDescription", {}).get("value", "")

        if not name or name.startswith("Q"):
            return None

        # Build frontmatter
        frontmatter = {}

        # Add Wikidata ID
        wikidata_id = self.extract_wikidata_id(item_uri)
        if wikidata_id:
            frontmatter["wikidata_id"] = wikidata_id

        # Add superclass relationships
        if "superclass" in entity and entity["superclass"].get("value"):
            superclass_label = entity.get("superclassLabel", {}).get("value", "")
            if superclass_label and not superclass_label.startswith("Q"):
                frontmatter["parent"] = f"[[{superclass_label}]]"

        # Add part-of relationships
        if "partOf" in entity and entity["partOf"].get("value"):
            part_of_label = entity.get("partOfLabel", {}).get("value", "")
            if part_of_label and not part_of_label.startswith("Q"):
                frontmatter["part_of"] = f"[[{part_of_label}]]"

        # Add field relationships
        if "field" in entity and entity["field"].get("value"):
            field_label = entity.get("fieldLabel", {}).get("value", "")
            if field_label and not field_label.startswith("Q"):
                frontmatter["field"] = f"[[{field_label}]]"

        # Add type relationships
        if "type" in entity and entity["type"].get("value"):
            type_label = entity.get("typeLabel", {}).get("value", "")
            if type_label and not type_label.startswith("Q"):
                frontmatter["type"] = f"[[{type_label}]]"

        # Add tags
        frontmatter["tags"] = ["causal-inference", "wikidata"]

        # Create the file
        return self.create_markdown_file(name, description, frontmatter)

    def create_scm_overview(self):
        """
        Create a main overview page for Structural Causal Models.
        """
        frontmatter = {
            "tags": ["overview", "causal-inference", "structural-causal-model"],
            "type": "concept"
        }

        content = """# Structural Causal Models

Structural Causal Models (SCM) are mathematical frameworks for representing and reasoning about causality. They combine graphical models with structural equations to represent causal relationships.

## Core Components

- [[Causal Graph]]: Directed acyclic graph representing causal relationships
- [[Structural Equations]]: Mathematical equations defining relationships
- [[Interventions]]: Operations that model external manipulations
- [[Counterfactuals]]: Reasoning about "what if" scenarios

## Related Concepts

- [[Causal Inference]]: Methods for inferring causal relationships from data
- [[Directed Acyclic Graph]]: Graph structure without cycles
- [[Bayesian Network]]: Probabilistic graphical model
- [[Pearl Causality]]: Judea Pearl's framework for causality

## Applications

- [[Policy Evaluation]]: Assessing impact of interventions
- [[Root Cause Analysis]]: Identifying sources of effects
- [[Mediation Analysis]]: Understanding causal pathways
- [[Confounding Control]]: Addressing spurious associations

## Key Researchers

- [[Judea Pearl]]: Pioneer of causal inference and SCM
- [[Donald Rubin]]: Rubin Causal Model
"""

        self.create_markdown_file(
            "Structural Causal Model",
            "Mathematical framework for causal reasoning",
            frontmatter,
            content
        )

    def import_all(self):
        """
        Import all Structural Causal Models related knowledge from Wikidata.
        """
        print("=" * 80)
        print("WIKIDATA STRUCTURAL CAUSAL MODELS IMPORTER")
        print("=" * 80)
        print(f"\nOutput directory: {self.output_dir}")

        # Create overview page
        print("\n[1/4] Creating SCM overview page...")
        self.create_scm_overview()
        print("     ✓ Created Structural Causal Model.md")

        # Query and process SCM data
        print("\n[2/4] Querying Wikidata for Structural Causal Models...")
        scm_data = self.get_structural_causal_models_data()
        print(f"     Found {len(scm_data)} results")

        created_count = 0
        for entity in scm_data:
            if self.process_entity(entity):
                created_count += 1

        print(f"     ✓ Created {created_count} markdown files")

        # Query and process causal inference concepts
        print("\n[3/4] Querying Wikidata for causal inference concepts...")
        causal_data = self.get_causal_inference_concepts()
        print(f"     Found {len(causal_data)} results")

        created_count = 0
        for entity in causal_data:
            if self.process_entity(entity):
                created_count += 1

        print(f"     ✓ Created {created_count} markdown files")

        # Query and process researchers and methods
        print("\n[4/4] Querying Wikidata for researchers and methods...")
        researcher_data = self.get_researchers_and_methods()
        print(f"     Found {len(researcher_data)} results")

        created_count = 0
        for entity in researcher_data:
            if self.process_entity(entity):
                created_count += 1

        print(f"     ✓ Created {created_count} markdown files")

        # Summary
        print("\n" + "=" * 80)
        print("IMPORT SUMMARY")
        print("=" * 80)
        print(f"Total files created: {len(self.created_files)}")
        print(f"Output directory: {self.output_dir}")
        print("\nYou can now run the reasoner to infer relationships:")
        print("  python demo_reasoner.py")
        print("=" * 80)


def main():
    """Main function."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Import Structural Causal Models knowledge from Wikidata"
    )
    parser.add_argument(
        "--output",
        "-o",
        default="graph/CausalInference",
        help="Output directory for markdown files (default: graph/CausalInference)"
    )
    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="Verbose output"
    )

    args = parser.parse_args()

    # Create importer and run
    importer = WikidataImporter(args.output)

    try:
        importer.import_all()
    except KeyboardInterrupt:
        print("\n\nImport interrupted by user.")
        return 1
    except Exception as e:
        print(f"\n❌ Error during import: {e}")
        import traceback
        traceback.print_exc()
        return 1

    return 0


if __name__ == "__main__":
    exit(main())
