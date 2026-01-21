import json
import re

# Load Terraform plan JSON
with open("tfplan.json") as f:
    plan = json.load(f)

# Map resource address -> action
resource_actions = {}

for rc in plan.get("resource_changes", []):
    addr = rc["address"]
    actions = rc["change"]["actions"]

    if actions == ["create"]:
        resource_actions[addr] = "create"
    elif actions == ["update"]:
        resource_actions[addr] = "update"
    elif actions == ["delete"]:
        resource_actions[addr] = "delete"
    elif actions == ["create", "delete"]:
        resource_actions[addr] = "replace"

# Load DOT graph
with open("tfplan.dot") as f:
    dot = f.read()

def color_node(match):
    node = match.group(1)

    color = "lightgray"
    style = "filled"

    action = resource_actions.get(node)

    if action == "create":
        color = "palegreen"
    elif action == "update":
        color = "gold"
    elif action in ("delete", "replace"):
        color = "lightcoral"

    return f'"{node}" [style={style}, fillcolor="{color}"];'

# Replace node definitions
dot = re.sub(r'"([^"]+)"\s*\[.*?\];', color_node, dot)

# Write colored DOT
with open("tfplan-colored.dot", "w") as f:
    f.write(dot)

print("✅ Colored Terraform graph generated")
