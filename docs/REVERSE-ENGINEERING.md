# Reverse engineering a website

`tp:reverse-engineer` teaches you how a live site works by taking it apart in your real Chrome, one rung at a time. You predict, it shows evidence, you explain, and at the end you rebuild a small version yourself.

## Setup

1. Install the Claude-in-Chrome extension and connect it to Claude Code.
2. Use any env, or ask for a new one ("new env for web experiments").
3. Say: `reverse engineer <url>, I want to know how <specific thing> works`.

## Pick targets you are allowed to study

Public pages, sites you own, or sites where you have permission. The skill asks, writes the answer into the inventory, and refuses otherwise. It observes only: it will not submit forms, buy things, replay requests, or touch credentials. Secrets are redacted from every note. Full rules: `harness/guardrails/web-safety.md`.

## The ladder

| Rung | You predict | You see |
|---|---|---|
| R1 Behavior | what the page does | screenshots, optional GIF |
| R2 Surface | how it's built | DOM structure |
| R3 Wire | what it asks the server | the real network calls |
| R4 State | where the data lives | read-only values in the page |
| R5 Why | why the authors chose this | you argue, then compare to the evidence |
| R6 Rebuild | what the smallest version needs | you build it |
| R7 Diff | where yours differs | the same probes, side by side |

One rung per turn. You never skip the prediction, and the agent never writes your clone's logic.

## Pause and resume

Targets live in `envs/<env>/reverse-engineering/inventory.md` with their rung, the evidence so far, and a specific next move. Say `reverse engineering inventory` to list them, or `resume reverse engineering <target>` to continue with no recap.

## Good first targets

A search box with instant results, an infinite-scroll feed on a public site, a docs site's client-side search, your own project. Avoid anything behind a login.
