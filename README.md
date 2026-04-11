# YouTube Creator Ops

**Plan, stage, publish, and verify a YouTube Shorts run through OpenClaw with one reusable run bundle.**

YouTube Creator Ops is a small public OpenClaw skill for YouTube publishing runs. It creates a
machine-readable run manifest, records publish steps with evidence, checks the resulting bundle, and
renders a shareable markdown report for launch review or debugging.

## Quick Start

```bash
python3 skill/youtube-creator-ops/scripts/init_youtube_creator_run.py \
  --out /tmp/youtube-run.json \
  --run-id demo-short \
  --channel "Demo Channel" \
  --goal "Publish one Shorts test clip" \
  --browser-profile creator-main \
  --kind short \
  --stage dry_run \
  --visibility unlisted \
  --video-file assets/demo-short.mp4 \
  --title "Demo Shorts publish" \
  --surface upload \
  --surface checks \
  --surface publish

python3 skill/youtube-creator-ops/scripts/append_youtube_creator_step.py \
  --manifest /tmp/youtube-run.json \
  --step-id open-studio \
  --surface upload \
  --action "Open YouTube Studio upload flow" \
  --expected "Studio loads with upload controls visible" \
  --actual "Studio loaded normally" \
  --status passed \
  --screenshot artifacts/studio-home.png

python3 skill/youtube-creator-ops/scripts/check_youtube_creator_bundle.py \
  --manifest /tmp/youtube-run.json \
  --repo-root . \
  --out /tmp/youtube-run-check.json

python3 skill/youtube-creator-ops/scripts/render_youtube_creator_report.py \
  --manifest /tmp/youtube-run.json \
  --out /tmp/youtube-run-report.md
```

## What It Covers

- one machine-readable run manifest for YouTube Studio publishes
- evidence-backed step logging for upload, checks, metadata, publish, and verification
- bundle validation for missing failure detail, missing screenshots, and absolute artifact paths
- a shareable markdown report for launch review, debugging, or handoff

## Included

- `skill/youtube-creator-ops/SKILL.md`
- `skill/youtube-creator-ops/agents/openai.yaml`
- `skill/youtube-creator-ops/scripts/init_youtube_creator_run.py`
- `skill/youtube-creator-ops/scripts/append_youtube_creator_step.py`
- `skill/youtube-creator-ops/scripts/check_youtube_creator_bundle.py`
- `skill/youtube-creator-ops/scripts/render_youtube_creator_report.py`

## Use Cases

- publish a YouTube Short through a logged-in OpenClaw browser profile
- keep one auditable record of title, visibility, checks, publish outcome, and public URL
- debug a failed Studio flow with screenshots and step-by-step evidence instead of chat notes
- hand a publishing run to another operator without rewriting the workflow from memory

## License

MIT
