#!/usr/bin/env python3
"""Validate the structure and safety contract of a generated bot package."""

from __future__ import annotations

import argparse
import csv
import json
import re
from pathlib import Path


REQUIRED_FILES = [
    "00-project-intake.yaml",
    "01-knowledge-base.md",
    "02-prompt.md",
    "03-workflow-blueprint.md",
    "04-test-matrix.csv",
    "05-release-checklist.md",
    "06-operations-runbook.md",
    "07-stakeholder-signoff.md",
    "manifest.json",
]

REQUIRED_TEST_IDS = {
    "T01-exact",
    "T02-paraphrase",
    "T03-ambiguous",
    "T04-no-match",
    "T05-sensitive",
    "T06-multi-intent",
    "T07-quoted-selection",
    "T08-unquoted-number",
    "T09-follow-up",
    "T10-group-concurrency",
    "T11-prompt-injection",
    "T12-rollback",
}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("package", type=Path)
    args = parser.parse_args()
    package = args.package.expanduser().resolve()

    errors: list[str] = []
    warnings: list[str] = []

    for name in REQUIRED_FILES:
        if not (package / name).is_file():
            errors.append(f"missing required file: {name}")

    if errors:
        for item in errors:
            print(f"ERROR: {item}")
        return 1

    manifest = json.loads((package / "manifest.json").read_text(encoding="utf-8"))
    candidate_count = manifest.get("candidate_count")
    if not isinstance(candidate_count, int) or not 1 <= candidate_count <= 8:
        errors.append("manifest candidate_count must be an integer between 1 and 8")

    textual_files = [p for p in package.iterdir() if p.suffix in {".md", ".yaml", ".csv"}]
    placeholder_pattern = re.compile(r"\{\{[A-Z0-9_]+\}\}")
    for path in textual_files:
        text = path.read_text(encoding="utf-8")
        leftovers = sorted(set(placeholder_pattern.findall(text)))
        if leftovers:
            errors.append(f"unresolved placeholders in {path.name}: {', '.join(leftovers)}")

    prompt = (package / "02-prompt.md").read_text(encoding="utf-8")
    for phrase in ("唯一知识来源", "不得使用外部知识", "固定兜底", "不得展示"):
        if phrase not in prompt:
            errors.append(f"prompt missing required safety phrase: {phrase}")
    if candidate_count is not None and f"最多列出 {candidate_count} 条" not in prompt:
        errors.append("prompt candidate count does not match manifest")

    with (package / "04-test-matrix.csv").open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    ids = {row.get("test_id", "") for row in rows}
    missing_tests = sorted(REQUIRED_TEST_IDS - ids)
    if missing_tests:
        errors.append("test matrix missing cases: " + ", ".join(missing_tests))
    if any(not row.get("expected_result", "").strip() for row in rows):
        warnings.append("some tests still need a concrete expected_result before release")

    knowledge = (package / "01-knowledge-base.md").read_text(encoding="utf-8")
    if "KB-001" not in knowledge:
        warnings.append("knowledge base contains no sample/first approved item KB-001")
    if manifest.get("owner") in (None, "", "待确认"):
        warnings.append("content owner is not confirmed")
    if manifest.get("approved_source") in (None, "", "待确认"):
        warnings.append("approved source is not confirmed")

    for item in warnings:
        print(f"WARN: {item}")
    for item in errors:
        print(f"ERROR: {item}")

    if errors:
        print(f"Validation failed with {len(errors)} error(s).")
        return 1
    print(f"Validation passed with {len(warnings)} warning(s): {package}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

