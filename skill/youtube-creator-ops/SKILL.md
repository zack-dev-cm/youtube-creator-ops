---
name: youtube-creator-ops
description: Public OpenClaw skill for planning, staging, executing, and verifying a YouTube Shorts publish run through a logged-in browser profile with one reusable evidence bundle.
homepage: https://github.com/zack-dev-cm/youtube-creator-ops
user-invocable: true
metadata: {"openclaw":{"homepage":"https://github.com/zack-dev-cm/youtube-creator-ops","skillKey":"youtube-creator-ops","requires":{"anyBins":["python3","python"]}}}
---

# YouTube Creator Ops

## Goal

Turn one YouTube Shorts publish run into a reusable artifact bundle:

- one machine-readable run manifest
- one ordered publish log with screenshots and URLs
- one structural bundle check
- one shareable markdown report

This skill is for YouTube Studio publishing through OpenClaw.
It assumes the browser profile is already authenticated.

## Use This Skill When

- the user wants to publish a YouTube Short through OpenClaw
- you need one clean record of upload, checks, visibility, and final URL
- the same YouTube Studio workflow keeps getting repeated from memory
- a failed publish needs screenshots, expected-versus-actual steps, and a handoff report
- the run should stay operator-visible instead of hidden background automation

## Quick Start

1. Initialize the run manifest.
   - Use `python3 {baseDir}/scripts/init_youtube_creator_run.py --out <json> --run-id <id> --channel <channel> --goal <goal>`.
   - Add `--browser-profile`, `--stage dry_run|live`, `--visibility`, `--video-file`, `--title`, and repeatable `--surface` fields.

2. Execute the YouTube Studio flow through OpenClaw.
   - Open the Studio page in a logged-in profile.
   - Record each meaningful step with `append_youtube_creator_step.py`.
   - Capture screenshots and public URLs as the run progresses.

3. Default to `dry_run`.
   - Keep the manifest in `dry_run` stage until the final publish click is intentionally approved.
   - Switch to `live` only when the operator wants the run to reach a public or unlisted post.

4. Pause for operator-owned auth if needed.
   - If YouTube shows CAPTCHA, passkey, login, or 2FA, stop the automated step log and let the operator complete it in the same browser profile.
   - Resume only after the authenticated Studio session is back.

5. Check the bundle before sharing it.
   - Use `python3 {baseDir}/scripts/check_youtube_creator_bundle.py --manifest <json> --repo-root <repo> --out <json>`.
   - Fix missing screenshots, incomplete failed steps, or absolute artifact paths before final handoff.

6. Render the report.
   - Use `python3 {baseDir}/scripts/render_youtube_creator_report.py --manifest <json> --out <md>`.
   - Share the report instead of loose screenshots and chat fragments.

## Operating Rules

### Profile rules

- Use a logged-in browser profile dedicated to the publishing context when possible.
- Do not claim a run is autonomous if login, CAPTCHA, passkey, or 2FA still requires operator action.
- Keep the publish run in one visible operator-controlled browser session.
- Treat the final publish click as a deliberate operator-approved action, even when the earlier steps are automated.

### Publish rules

- Record expected result and actual result for every step that matters.
- Capture a screenshot for failed or blocked steps and important checkpoints.
- Store final published URL when the run succeeds.
- Prefer relative artifact paths so the bundle can move between machines.

### Safety rules

- Do not store cookies, secrets, or access tokens in notes or artifacts.
- Do not use private absolute filesystem paths in the final bundle.
- Treat moderation delays and post-processing lag as publish outcomes to record, not as silent success.

## Bundled Scripts

- `scripts/init_youtube_creator_run.py`
  - Create a machine-readable manifest for one YouTube publish run.
- `scripts/append_youtube_creator_step.py`
  - Append one evidence-backed step to the publish manifest.
- `scripts/check_youtube_creator_bundle.py`
  - Validate the resulting run bundle before handoff or release review.
- `scripts/render_youtube_creator_report.py`
  - Render a concise markdown report from the publish manifest.
