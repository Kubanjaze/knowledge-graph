# Phase 93 — Knowledge Graph Builder (v1.0)

## Goal
Build a knowledge graph connecting compounds → KRAS → diseases (with simulated disease associations), visualize with NetworkX.

## CLI
```bash
PYTHONUTF8=1 python main.py --compounds data/compounds.csv
```

## Outputs
- `output/knowledge_graph.png` — graph visualization
- `output/graph_stats.csv` — node/edge statistics
- Console: graph summary

## Logic
1. Load compounds from compounds.csv
2. Create KRAS target node
3. Connect compounds to KRAS (edge weight = pIC50)
4. Add simulated disease associations (NSCLC, pancreatic, colorectal, etc.)
5. Connect KRAS to diseases with association scores
6. Visualize with spring layout, node colors by type

## Key Concepts
- Knowledge graph construction with typed nodes/edges
- NetworkX spring layout visualization
- Multi-entity relationship modeling

## Verification Checklist
- [ ] `--help` works
- [ ] Graph has compound + target + disease nodes
- [ ] Edges connect compounds→KRAS→diseases
- [ ] PNG saved with color-coded node types

## Risks
- Disease associations are simulated (not from real API)
