import json
import re
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

EDGE_RE = re.compile(r'("?[^"]+"?)\s*->\s*("?[^"]+"?)')


def sanitize(text: str) -> str:
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
            match = EDGE_RE.search(line)
            if match:
                src = match.group(1).strip('"')
                dst = match.group(2).strip('"')
                edges.append((src, dst))
    return edges


def generate_dot(actions, edges):
    lines = [
        "digraph terraform {",
        "  rankdir=LR;",
        '  node [shape=box style="rounded,filled" fontname="Helvetica"];',
        '  edge [color="#999999"];'
    ]

    # Nodes
    for addr, action in actions.items():
        color = COLORS.get(action, COLORS["no-op"])
        label = sanitize(f"{addr}\\n{action.upper()}")
        lines.append(f'"{addr}" [fillcolor="{color}" label="{label}"];')

    # Edges (ALWAYS quoted)
    for src, dst in edges:
        lines.append(f'"{src}" -> "{dst}";')

    lines.append("}")
    Path(OUT_DOT).write_text("\n".join(lines))


def main():
    actions = load_plan_actions()
    edges = load_edges()
    generate_dot(actions, edges)


if __name__ == "__main__":
    main()
