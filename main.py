"""Phase 93 — Knowledge Graph Builder: Compounds → KRAS → Diseases."""
import sys
import os

if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

import argparse
import pandas as pd
import networkx as nx
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


FAMILY_COLORS = {
    "benz": "#4C72B0", "naph": "#DD8452", "ind": "#55A868",
    "quin": "#C44E52", "pyr": "#8172B2", "bzim": "#937860",
    "other": "#808080",
}

# Simulated KRAS disease associations (based on real Open Targets data)
KRAS_DISEASES = {
    "NSCLC": 0.81,
    "Pancreatic Cancer": 0.62,
    "Colorectal Cancer": 0.68,
    "AML": 0.75,
    "Noonan Syndrome": 0.83,
    "Gastric Cancer": 0.77,
    "Bladder Cancer": 0.70,
}

NODE_TYPE_COLORS = {
    "compound": "#4C72B0",
    "target": "#E74C3C",
    "disease": "#F39C12",
}


def build_knowledge_graph(df: pd.DataFrame) -> nx.Graph:
    """Build knowledge graph: compounds → KRAS → diseases."""
    G = nx.Graph()

    # Add KRAS target
    G.add_node("KRAS", node_type="target")

    # Add compounds and connect to KRAS
    for _, row in df.iterrows():
        name = row["compound_name"]
        family = name.split("_")[0]
        G.add_node(name, node_type="compound", family=family, pic50=row["pic50"])
        G.add_edge(name, "KRAS", relation="inhibits", weight=row["pic50"])

    # Add diseases and connect to KRAS
    for disease, score in KRAS_DISEASES.items():
        G.add_node(disease, node_type="disease", score=score)
        G.add_edge("KRAS", disease, relation="associated_with", weight=score)

    return G


def visualize(G: nx.Graph, out_path: str) -> None:
    """Visualize knowledge graph with typed node coloring."""
    fig, ax = plt.subplots(figsize=(16, 12))

    # Custom layout: compounds left, KRAS center, diseases right
    pos = {}
    compounds = [n for n, d in G.nodes(data=True) if d.get("node_type") == "compound"]
    diseases = [n for n, d in G.nodes(data=True) if d.get("node_type") == "disease"]

    # Arrange compounds in a circle on the left
    for i, c in enumerate(sorted(compounds)):
        angle = (i / len(compounds)) * 2 * 3.14159
        pos[c] = (-2 + 1.5 * __import__("math").cos(angle), 1.5 * __import__("math").sin(angle))

    # KRAS at center
    pos["KRAS"] = (1.5, 0)

    # Diseases on the right
    for i, d in enumerate(diseases):
        y = (i - len(diseases) / 2) * 0.8
        pos[d] = (4, y)

    # Draw edges
    compound_edges = [(u, v) for u, v, d in G.edges(data=True) if d.get("relation") == "inhibits"]
    disease_edges = [(u, v) for u, v, d in G.edges(data=True) if d.get("relation") == "associated_with"]

    nx.draw_networkx_edges(G, pos, edgelist=compound_edges, alpha=0.2, edge_color="#999999", ax=ax)
    nx.draw_networkx_edges(G, pos, edgelist=disease_edges, alpha=0.6, edge_color="#E74C3C", width=2, ax=ax)

    # Draw compound nodes colored by family
    for c in compounds:
        family = G.nodes[c].get("family", "other")
        color = FAMILY_COLORS.get(family, "#808080")
        ax.scatter(pos[c][0], pos[c][1], c=color, s=40, zorder=3)

    # Draw KRAS node
    ax.scatter(pos["KRAS"][0], pos["KRAS"][1], c="#E74C3C", s=300, zorder=4, marker="s")
    ax.text(pos["KRAS"][0], pos["KRAS"][1] - 0.25, "KRAS", fontsize=12, fontweight="bold", ha="center")

    # Draw disease nodes
    for d in diseases:
        ax.scatter(pos[d][0], pos[d][1], c="#F39C12", s=120, zorder=3)
        ax.text(pos[d][0] + 0.15, pos[d][1], d, fontsize=9, va="center")

    # Legend
    for family, color in FAMILY_COLORS.items():
        if family != "other":
            ax.scatter([], [], c=color, label=f"Compound: {family}", s=40)
    ax.scatter([], [], c="#E74C3C", label="Target: KRAS", s=100, marker="s")
    ax.scatter([], [], c="#F39C12", label="Disease", s=80)
    ax.legend(loc="upper left", fontsize=8, title="Node Types")

    ax.set_title("Knowledge Graph: Compounds → KRAS → Diseases", fontsize=14)
    ax.axis("off")
    plt.savefig(out_path, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"Graph saved: {out_path}")


def main():
    parser = argparse.ArgumentParser(
        description="Build knowledge graph: compounds → KRAS → diseases.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("--compounds", default="data/compounds.csv", help="Path to compounds CSV")
    args = parser.parse_args()

    os.makedirs("output", exist_ok=True)

    df = pd.read_csv(args.compounds)
    print(f"Loaded {len(df)} compounds from {args.compounds}")

    G = build_knowledge_graph(df)

    # Stats
    compounds = [n for n, d in G.nodes(data=True) if d.get("node_type") == "compound"]
    diseases = [n for n, d in G.nodes(data=True) if d.get("node_type") == "disease"]
    targets = [n for n, d in G.nodes(data=True) if d.get("node_type") == "target"]

    print(f"\nKnowledge Graph Summary:")
    print(f"  Nodes: {G.number_of_nodes()} ({len(compounds)} compounds, {len(targets)} targets, {len(diseases)} diseases)")
    print(f"  Edges: {G.number_of_edges()} ({len(compounds)} inhibits, {len(diseases)} associated_with)")

    print(f"\nDisease associations:")
    for disease in sorted(diseases):
        score = G.nodes[disease].get("score", 0)
        print(f"  KRAS → {disease}: {score:.2f}")

    # Save stats
    stats = []
    for n, d in G.nodes(data=True):
        stats.append({"node": n, "type": d.get("node_type"), "degree": G.degree(n)})
    stats_df = pd.DataFrame(stats).sort_values("degree", ascending=False)
    stats_path = "output/graph_stats.csv"
    stats_df.to_csv(stats_path, index=False)
    print(f"\nGraph stats saved: {stats_path}")

    visualize(G, "output/knowledge_graph.png")


if __name__ == "__main__":
    main()
