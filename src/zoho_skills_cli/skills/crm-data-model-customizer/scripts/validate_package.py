#!/usr/bin/env python3
"""Mechanical subset of the Phase 8 validation pass (spec FR-014).

Checks that are purely structural (no judgment required) are done here:
  1. No orphan elements (empty req_ids) anywhere in the canonical YAML.
  2. Every field/module reference used by pipelines/blueprints/automation/personas
     resolves to an actual module.field defined in `modules`.

Judgment-based checks (naming consistency, [DOCS] citation quality, requirement
coverage narrative, etc.) remain the LLM's responsibility per SKILL.md Phase 8 and are
not duplicated here.

CLI:
    python3 validate_package.py <handoff-spec.yaml>

Exit code 0 and prints "PASS" if no structural failures found; otherwise exit code 1
and prints each failure, one per line, prefixed "FAIL: ".
"""
import sys

import yaml


def _field_index(model: dict) -> set[str]:
    fields = set()
    for module in model.get("modules", []):
        mod = module["api_name"]
        for field in module.get("fields", []):
            fields.add(f"{mod}.{field['api_name']}")
    return fields


def _module_index(model: dict) -> set[str]:
    return {m["api_name"] for m in model.get("modules", [])}


def validate(model: dict) -> list[str]:
    failures: list[str] = []
    field_index = _field_index(model)
    module_index = _module_index(model)

    for module in model.get("modules", []):
        if not module.get("req_ids"):
            failures.append(f"orphan module: {module['api_name']} has empty req_ids")
        for field in module.get("fields", []):
            if not field.get("req_ids"):
                failures.append(
                    f"orphan field: {module['api_name']}.{field['api_name']} has empty req_ids"
                )
        for rel in module.get("relationships", []):
            if not rel.get("req_ids"):
                failures.append(
                    f"orphan relationship: {module['api_name']} -> {rel['target_module']} has empty req_ids"
                )
            if rel["target_module"] not in module_index:
                failures.append(
                    f"dangling reference: {module['api_name']} relationship targets unknown module {rel['target_module']}"
                )

    for pipeline in model.get("pipelines", []):
        for stage in pipeline.get("stages", []):
            if not stage.get("req_ids"):
                failures.append(f"orphan pipeline stage: {stage['name']} has empty req_ids")
            for f in stage.get("required_fields", []):
                if f not in field_index:
                    failures.append(f"dangling reference: pipeline stage {stage['name']} requires unknown field {f}")

    for blueprint in model.get("blueprints", []):
        for transition in blueprint.get("transitions", []):
            if not transition.get("req_ids"):
                failures.append(
                    f"orphan blueprint transition: {blueprint['module']} {transition['from']}->{transition['to']} has empty req_ids"
                )
            for f in transition.get("mandatory_fields", []):
                if f not in field_index:
                    failures.append(
                        f"dangling reference: blueprint transition {transition['from']}->{transition['to']} requires unknown field {f}"
                    )

    for rule in model.get("automation_rules", []):
        if not rule.get("req_ids"):
            failures.append(f"orphan automation rule: {rule['rule_id']} has empty req_ids")
        for f in rule.get("reads_fields", []) + rule.get("writes_fields", []):
            if f not in field_index:
                failures.append(f"dangling reference: rule {rule['rule_id']} references unknown field {f}")

    writers: dict[str, list[str]] = {}
    for rule in model.get("automation_rules", []):
        for f in rule.get("writes_fields", []):
            writers.setdefault(f, []).append(rule["rule_id"])

    for persona in model.get("personas", []):
        if not persona.get("req_ids"):
            failures.append(f"orphan persona: {persona['persona']} has empty req_ids")
        for kpi in persona.get("kpis", []):
            if not kpi.get("req_ids"):
                failures.append(f"orphan KPI: {kpi['name']} has empty req_ids")
            for f in kpi.get("source_fields", []):
                if f not in field_index:
                    failures.append(f"dangling reference: KPI {kpi['name']} references unknown field {f}")

    return failures


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: validate_package.py <handoff-spec.yaml>", file=sys.stderr)
        return 2
    with open(sys.argv[1], "r", encoding="utf-8") as f:
        model = yaml.safe_load(f)

    failures = validate(model)
    if failures:
        for failure in failures:
            print(f"FAIL: {failure}")
        return 1
    print("PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
