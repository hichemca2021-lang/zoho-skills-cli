#!/usr/bin/env python3
"""Deterministic generator: canonical handoff-spec YAML -> Mermaid erDiagram (.mmd).

No LLM involved. Diagrams are generated from the YAML, never hand-edited, so the
diagram and the canonical model can never diverge (spec FR-009).

CLI:
    python3 yaml_to_mermaid.py <input.yaml> <output.mmd> [--domain NAME]

Without --domain, emits the overview diagram (keys + relationships only, all modules).
With --domain NAME, emits a detailed diagram for modules tagged with that domain only,
including all fields (max ~12 entities recommended per idea-doc diagram-readability rule).
"""
import argparse
import sys

import yaml

TYPE_TOKENS = {
    "string", "text", "int", "decimal", "currency", "boolean", "date", "datetime",
    "picklist", "multipicklist", "email", "phone", "url", "lookup", "ownerlookup",
    "formula", "autonumber", "file", "subform",
}


def load_model(path: str) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def _sanitize(name: str) -> str:
    return name.replace(" ", "_")


def render_overview(model: dict) -> str:
    lines = ["erDiagram"]
    modules = model.get("modules", [])
    for module in modules:
        mod_name = _sanitize(module["api_name"])
        for rel in module.get("relationships", []):
            target = _sanitize(rel["target_module"])
            label = rel["lookup_field_api_name"]
            cardinality = rel.get("cardinality", "many_to_one")
            if cardinality == "many_to_one":
                lines.append(f'  {target} ||--o{{ {mod_name} : "{label}"')
            elif cardinality == "many_to_many":
                lines.append(f'  {target} }}o--o{{ {mod_name} : "{label}"')
            elif cardinality == "subform":
                lines.append(f'  {target} ||--|{{ {mod_name} : "subform:{label}"')
    for module in modules:
        mod_name = _sanitize(module["api_name"])
        lines.append(f"  {mod_name} {{")
        key_field = module.get("fields", [None])
        key_field = key_field[0] if key_field else None
        if key_field:
            req = ",".join(key_field.get("req_ids", []))
            lines.append(f'    string {key_field["api_name"]} PK "{req}"')
        lines.append("  }")
    return "\n".join(lines) + "\n"


def render_domain(model: dict, domain: str) -> str:
    lines = ["erDiagram"]
    modules = [m for m in model.get("modules", []) if m.get("domain") == domain]
    if len(modules) > 12:
        print(
            f"warning: domain '{domain}' has {len(modules)} entities (>12); "
            "idea-doc readability rule recommends splitting further",
            file=sys.stderr,
        )
    for module in modules:
        mod_name = _sanitize(module["api_name"])
        for rel in module.get("relationships", []):
            target = _sanitize(rel["target_module"])
            label = rel["lookup_field_api_name"]
            lines.append(f'  {target} ||--o{{ {mod_name} : "{label}"')
    for module in modules:
        mod_name = _sanitize(module["api_name"])
        lines.append(f"  {mod_name} {{")
        for field in module.get("fields", []):
            ftype = field.get("type")
            if ftype not in TYPE_TOKENS:
                raise ValueError(
                    f"unknown field type token '{ftype}' on {mod_name}.{field['api_name']}"
                )
            req = ",".join(field.get("req_ids", []))
            lines.append(f'    {ftype} {field["api_name"]} "{req}"')
        lines.append("  }")
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input_yaml")
    parser.add_argument("output_mmd")
    parser.add_argument("--domain", default=None)
    args = parser.parse_args()

    model = load_model(args.input_yaml)
    content = render_domain(model, args.domain) if args.domain else render_overview(model)

    with open(args.output_mmd, "w", encoding="utf-8") as f:
        f.write(content)
    return 0


if __name__ == "__main__":
    sys.exit(main())
