"""
Setup script for Obsidian Graph Reasoner.
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="obsidian-graph-reasoner",
    version="0.1.0",
    author="Arthur Sarazin",
    description="A reasoning engine for Obsidian knowledge graphs",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/heretica/graph-reasoner-obsidian",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=[
        "pyyaml>=5.4.0",
        "SPARQLWrapper>=1.8.5",
        "requests>=2.25.0",
    ],
    entry_points={
        "console_scripts": [
            "obsidian-analyze=src.cli.analyze:main",
            "obsidian-persist=src.cli.persist:main",
        ],
    },
)
