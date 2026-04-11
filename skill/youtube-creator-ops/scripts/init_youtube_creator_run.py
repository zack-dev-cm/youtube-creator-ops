#!/usr/bin/env python3
"""Create a machine-readable manifest for one YouTube Shorts publish run."""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

VALID_KINDS = {"short"}
VALID_VISIBILITY = {"draft", "private", "unlisted", "public"}
VALID_AUDIENCE = {"unspecified", "made_for_kids", "not_made_for_kids"}
VALID_STAGES = {"dry_run", "live"}


def dedupe(values: list[str]) -> list[str]:
    seen: set[str] = set()
    out: list[str] = []
    for value in values:
        normalized = value.strip()
        if not normalized or normalized in seen:
            continue
        seen.add(normalized)
        out.append(normalized)
    return out


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", required=True, help="Output JSON file.")
    parser.add_argument("--run-id", required=True, help="Stable identifier for this publish run.")
    parser.add_argument("--channel", required=True, help="Public YouTube channel or brand name.")
    parser.add_argument("--goal", required=True, help="What this publish run is trying to accomplish.")
    parser.add_argument("--browser-profile", default="", help="OpenClaw browser profile label.")
    parser.add_argument("--kind", choices=sorted(VALID_KINDS), default="short", help="Publish type.")
    parser.add_argument("--stage", choices=sorted(VALID_STAGES), default="dry_run", help="Execution stage.")
    parser.add_argument("--visibility", choices=sorted(VALID_VISIBILITY), default="draft", help="Target visibility.")
    parser.add_argument("--audience", choices=sorted(VALID_AUDIENCE), default="unspecified", help="Audience setting.")
    parser.add_argument("--video-file", default="", help="Relative path to the video asset.")
    parser.add_argument("--title", default="", help="Planned title.")
    parser.add_argument("--description-file", default="", help="Relative path to the description text.")
    parser.add_argument("--thumbnail-file", default="", help="Relative path to the thumbnail asset.")
    parser.add_argument("--target-url", default="https://studio.youtube.com/", help="Studio URL.")
    parser.add_argument("--surface", action="append", default=[], help="Repeatable surface name such as upload or publish.")
    parser.add_argument("--tag", action="append", default=[], help="Repeatable tag for grouping runs.")
    args = parser.parse_args()

    out_path = Path(args.out).expanduser().resolve()
    out_path.parent.mkdir(parents=True, exist_ok=True)

    payload = {
        "schema_version": "1.0",
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "run": {
            "run_id": args.run_id.strip(),
            "channel": args.channel.strip(),
            "goal": args.goal.strip(),
            "browser_profile": args.browser_profile.strip(),
            "kind": args.kind,
            "stage": args.stage,
            "visibility": args.visibility,
            "audience": args.audience,
            "target_url": args.target_url.strip() or "https://studio.youtube.com/",
            "surfaces": dedupe(args.surface),
            "tags": dedupe(args.tag),
        },
        "assets": {
            "video_file": args.video_file.strip(),
            "title": args.title.strip(),
            "description_file": args.description_file.strip(),
            "thumbnail_file": args.thumbnail_file.strip(),
        },
        "steps": [],
        "summary": {
            "status": "in_progress",
            "passed_steps": 0,
            "failed_steps": 0,
            "blocked_steps": 0,
            "published_url": "",
            "issue_keys": [],
        },
    }

    out_path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(out_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
