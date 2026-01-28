import json
import re
import hashlib
from pathlib import Path

PLAN_JSON = "tfplan.json"
BASE_DOT = "base.dot"
OUT_DOT = "tfplan.dot"

COLORS = {
    "create": "#c7f5d9",
    "update": "#fff3bf",
    "delete": "#f8c7cc",
    "no-op": "#e0e0e0"
}

EDGE_RE = re.compile(r'"?([^"\s]+)"?\s*->\s*"?(.*?)"?$')


def safe_id(text: str) -> str:
    """
    Generate a DOT-safe node id
    """
    return "n_" + hashlib.md5(text.encode()).hexdigest()


def sanitize_label(text: str) -> str:
    return (
        text.replace("\\", "\\\\")
            .replace('"', '\\"')
            .replace("\n", "\\n")
    )


def load_plan_actions():
    with open(PLAN_JSON) as f:
        plan = json.load(f)

    actions = {}
    for rc in plan.get("resource_changes", []):
        addr = rc["address"]
        act = ",".join(rc["change"]["actions"])
        actions[addr] = act

    return actions


def load_edges():
    edges = []
    with open(BASE_DOT) as f:
        for line in f:
            if "->" not in line:
                continue
            parts = line.strip().strip(";").split("->")
            if len(parts) != 2:
                continue
            src = parts[0].strip().strip('"')
            dst = parts[1].strip().strip('"')
            edges.append((src, dst))
    return edges


def generate_dot(actions, edges):
    id_map = {addr: safe_id(addr) for addr in actions.keys()}

    lines = [
        "digraph terraform {",
        "  rankdir=LR;",
        '  node [shape=box style="rounded,filled" fontname="Helvetica"];',
        '  edge [color="#999999"];'
    ]

    # Nodes
    for addr, action in actions.items():
        node_id = id_map[addr]
        color = COLORS.get(action, COLORS["no-op"])
        label = sanitize_label(f"{addr}\\n{action.upper()}")

        lines.append(
            f'{node_id} [fillcolor="{color}" label="{label}"];'
        )

    # Edges
    for src, dst in edges:
        if src in id_map and dst in id_map:
            lines.append(f'{id_map[src]} -> {id_map[dst]};')

    lines.append("}")
    Path(OUT_DOT).write_text("\n".join(lines))


def main():
    actions = load_plan_actions()
    edges = load_edges()
    generate_dot(actions, edges)


if __name__ == "__main__":
    main()
