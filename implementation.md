# Phase 93 — Knowledge Graph Builder (v1.1)

## Goal
Build a knowledge graph connecting compounds → KRAS → diseases, visualize with NetworkX.

## CLI
```bash
PYTHONUTF8=1 python main.py --compounds data/compounds.csv
```

## Outputs
- `output/knowledge_graph.png` — graph with compounds (left, colored by family), KRAS (center), diseases (right)
- `output/graph_stats.csv` — node type and degree for all 53 nodes
- Console summary

## Logic
1. Load 45 compounds, connect to KRAS with pIC50-weighted edges
2. Add 7 simulated disease associations (based on Open Targets data)
3. Custom layout: compounds in circle (left), KRAS center, diseases right
4. Color by node type: compounds by family, KRAS red, diseases orange

## Key Concepts
- Multi-entity knowledge graph (compound → target → disease)
- NetworkX with typed nodes and custom layout
- Simulated disease association scores

## Verification Checklist
- [x] `--help` works
- [x] 53 nodes: 45 compounds + 1 target + 7 diseases
- [x] 52 edges: 45 inhibits + 7 associated_with
- [x] PNG saved with color-coded node types
- [x] Stats CSV saved

## Results
- KRAS is hub node with degree 52 (connected to all compounds and diseases)
- Highest disease association: Noonan Syndrome (0.83), NSCLC (0.81)
- Graph clearly shows compound → target → disease pathway

## Deviations
- Disease associations are simulated (scores based on Phase 85 real data)

## Risks
- Simulated data for diseases (not live API)
