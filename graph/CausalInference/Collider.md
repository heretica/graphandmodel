---
parent: '[[Causal Graph]]'
tags:
- bias
- selection
type: pattern
---

A collider is a variable caused by two or more variables.

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
