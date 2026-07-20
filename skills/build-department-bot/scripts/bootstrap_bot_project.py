#!/usr/bin/env python3
"""Create a department-bot project package from bundled templates."""

from __future__ import annotations

import argparse
import json
import re
import shutil
from datetime import date
from pathlib import Path


DEFAULT_FALLBACK = (
    "这个问题暂时超出知识库范围。请联系人工支持渠道获取准确答复。"
)

OUTPUT_NAMES = {
    "project-intake.yaml": "00-project-intake.yaml",
    "knowledge-base-template.md": "01-knowledge-base.md",
    "prompt-template.md": "02-prompt.md",
    "workflow-blueprint.md": "03-workflow-blueprint.md",
    "test-matrix.csv": "04-test-matrix.csv",
    "release-checklist.md": "05-release-checklist.md",
    "ops-runbook.md": "06-operations-runbook.md",
    "stakeholder-signoff.md": "07-stakeholder-signoff.md",
}


def safe_slug(value: str) -> str:
    slug = re.sub(r"[^a-zA-Z0-9\u4e00-\u9fff]+", "-", value.strip()).strip("-")
    return slug or "department-bot"


def replace_tokens(text: str, values: dict[str, str]) -> str:
    for key, value in values.items():
        text = text.replace("{{" + key + "}}", value)
    return text


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--department", required=True)
    parser.add_argument("--bot-name", required=True)
    parser.add_argument("--owner", default="待确认")
    parser.add_argument("--approved-source", default="待确认")
    parser.add_argument(
        "--mode",
        choices=("exact-faq", "guided-retrieval", "action-workflow"),
        default="exact-faq",
    )
    parser.add_argument("--candidate-count", type=int, default=5)
    parser.add_argument("--fallback", default=DEFAULT_FALLBACK)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()

    if not 1 <= args.candidate_count <= 8:
        parser.error("--candidate-count must be between 1 and 8")

    skill_dir = Path(__file__).resolve().parent.parent
    assets_dir = skill_dir / "assets"
    output_dir = args.output or Path.cwd() / "bot-projects" / safe_slug(args.department)
    output_dir = output_dir.expanduser().resolve()

    if output_dir.exists() and any(output_dir.iterdir()) and not args.force:
        parser.error(f"output directory is not empty: {output_dir}; use --force to overwrite package files")
    output_dir.mkdir(parents=True, exist_ok=True)

    values = {
        "DEPARTMENT": args.department,
        "BOT_NAME": args.bot_name,
        "OWNER": args.owner,
        "APPROVED_SOURCE": args.approved_source,
        "MODE": args.mode,
        "CANDIDATE_COUNT": str(args.candidate_count),
        "FALLBACK_TEXT": args.fallback,
        "DATE": date.today().isoformat(),
    }

    created: list[str] = []
    for source_name, output_name in OUTPUT_NAMES.items():
        source = assets_dir / source_name
        target = output_dir / output_name
        if not source.exists():
            raise FileNotFoundError(f"missing bundled template: {source}")
        rendered = replace_tokens(source.read_text(encoding="utf-8"), values)
        target.write_text(rendered, encoding="utf-8")
        created.append(output_name)

    manifest = {
        "schema_version": 1,
        "created_on": values["DATE"],
        "department": args.department,
        "bot_name": args.bot_name,
        "owner": args.owner,
        "approved_source": args.approved_source,
        "mode": args.mode,
        "candidate_count": args.candidate_count,
        "files": created,
        "status": "draft",
    }
    (output_dir / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    print(f"Created bot package: {output_dir}")
    for name in created + ["manifest.json"]:
        print(f"- {name}")
    print("Next: populate approved knowledge, record expected answers, then run validate_bot_package.py")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
