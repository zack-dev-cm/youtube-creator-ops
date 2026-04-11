#!/usr/bin/env python3
"""Render a markdown report from a YouTube publish run manifest."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from urllib.parse import urlsplit, urlunsplit


def load_manifest(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def is_absolute_or_private(path_text: str) -> bool:
    return path_text.startswith("/") or path_text.startswith("~") or ":\\" in path_text or path_text.startswith("file://")


def safe_display_path(path_text: str) -> str:
    value = path_text.strip()
    if not value:
        return "n/a"
    if is_absolute_or_private(value):
        return "[redacted-private-path]"
    return value


def safe_youtube_url(url: str) -> str:
    value = url.strip()
    if not value:
        return "n/a"
    try:
        parts = urlsplit(value)
    except ValueError:
        return "[redacted-private-url]"
    host = (parts.hostname or "").lower()
    if parts.scheme != "https":
        return "[redacted-private-url]"
    if host == "youtu.be" or host.endswith(".youtube.com") or host == "youtube.com":
        return urlunsplit((parts.scheme, parts.netloc, parts.path, "", ""))
    return "[redacted-private-url]"


def format_artifacts(artifacts: dict[str, str]) -> list[str]:
    labels = {
        "screenshot": "screenshot",
        "snapshot_json": "snapshot",
        "console_log": "console",
        "video_proof": "video",
    }
    out: list[str] = []
    for key, label in labels.items():
        value = artifacts.get(key, "").strip()
        if value:
            out.append(f"{label}: `{safe_display_path(value)}`")
    return out


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", required=True, help="Run manifest JSON.")
    parser.add_argument("--out", required=True, help="Output markdown file.")
    args = parser.parse_args()

    manifest_path = Path(args.manifest).expanduser().resolve()
    out_path = Path(args.out).expanduser().resolve()
    out_path.parent.mkdir(parents=True, exist_ok=True)

    payload = load_manifest(manifest_path)
    run = payload.get("run", {})
    assets = payload.get("assets", {})
    summary = payload.get("summary", {})
    steps = payload.get("steps", [])

    lines = [
        "# YouTube Creator Run Report",
        "",
        f"- Run: `{run.get('run_id', '')}`",
        f"- Channel: {run.get('channel', '')}",
        f"- Goal: {run.get('goal', '')}",
        f"- Browser profile: {run.get('browser_profile', '') or 'n/a'}",
        f"- Kind: {run.get('kind', '')}",
        f"- Stage: {run.get('stage', '')}",
        f"- Visibility: {run.get('visibility', '')}",
        f"- Audience: {run.get('audience', '')}",
        f"- Studio URL: {safe_youtube_url(run.get('target_url', ''))}",
        f"- Video file: {safe_display_path(assets.get('video_file', ''))}",
        f"- Title: {assets.get('title', '') or 'n/a'}",
        f"- Description file: {safe_display_path(assets.get('description_file', ''))}",
        f"- Thumbnail file: {safe_display_path(assets.get('thumbnail_file', ''))}",
        f"- Overall status: **{summary.get('status', 'unknown')}**",
        f"- Passed / Failed / Blocked: {summary.get('passed_steps', 0)} / {summary.get('failed_steps', 0)} / {summary.get('blocked_steps', 0)}",
        f"- Published URL: {safe_youtube_url(summary.get('published_url', ''))}",
        "",
        "## Steps",
        "",
    ]

    for index, step in enumerate(steps, start=1):
        lines.append(f"### {index}. {step.get('step_id', f'step-{index}')}")
        lines.append(f"- Surface: {step.get('surface', '') or 'n/a'}")
        lines.append(f"- Status: **{step.get('status', 'unknown')}**")
        lines.append(f"- Action: {step.get('action', '')}")
        lines.append(f"- Expected: {step.get('expected', '')}")
        lines.append(f"- Actual: {step.get('actual', '')}")
        if step.get("note"):
            lines.append(f"- Note: {step['note']}")
        if step.get("issue_keys"):
            lines.append(f"- Issue keys: {', '.join(step['issue_keys'])}")
        if step.get("published_url"):
            lines.append(f"- Published URL: {safe_youtube_url(step['published_url'])}")
        artifact_parts = format_artifacts(step.get("artifacts", {}))
        if artifact_parts:
            lines.append(f"- Artifacts: {'; '.join(artifact_parts)}")
        lines.append("")

    out_path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")
    print(out_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
