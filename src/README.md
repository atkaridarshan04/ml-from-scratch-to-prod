# src/ – Production ML Code

This directory contains reusable, production-grade Python code used by
training, batch inference, and online inference pipelines.

## Directory Overview
- preprocessing/   → Feature transformations shared across pipelines
- models/          → Model training and evaluation logic
- inference/       → Inference-time preprocessing and prediction utilities
- utils/           → Logging, IO helpers, common utilities

## Design Principles
- No notebook-specific code
- No hardcoded paths
- Shared logic between training and inference
- Deterministic behavior
