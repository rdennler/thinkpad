---
name: media
description: PDF/epub text extraction and audio/video conversion for study material. Triggers on "extract this pdf", "absorb this book/pdf", "convert this video/audio", "transcribe this pdf". Outputs land in media/out/; absorbed sources also get ontology graph nodes.
metadata:
  api: 1
  kind: infra
  mode: infra
  terminal: allowed
  triggers: ["extract this pdf", "absorb this book", "convert this video", "convert this audio"]
  reads: ["media/<env>/"]
  writes: ["media/out/", "memory/ontology/graph.jsonl"]
  requires: ["bin:pdftotext", "bin:ffmpeg"]
  graph_reads: []
  graph_writes: ["Resource", "Concept", "Person"]
---

# tp:media — PDF Extraction & A/V Conversion

Turns source material (PDF, epub, audio, video) into text or a different format so a learning env can use it.

**Terminal:** infra skill, so shell commands are fine here. The learning-session terminal rule does not apply while this skill runs.

## Tools

| Job | Tool |
|---|---|
| PDF → text | `pdftotext -layout in.pdf out.txt` (poppler) |
| PDF page → PNG | `pdftoppm -png -r 150 -f N -l N in.pdf out` |
| A/V convert, trim, extract audio | `ffmpeg` (native) |

Run `<tool> --help` before the first use in a session; flags differ between versions.

## Dropoff Convention (absorb pipeline)

Source files land in `media/<env>/`. Absorbing a source means:

1. Extract to `media/out/<source-stem>/`.
2. Through `tp:memory`, create one `Resource` node (`part_of` the env), plus a `Concept` node per chapter or topic (`part_of` the env, its `refs` property naming the extract section). Link the Resource `about` each Concept.

Env scoping lives in the graph relations, so one env never sees another env's resources.

## Output Convention

- Outputs go to `media/out/` unless the user names a destination.
- Name outputs after the source: `<stem>.txt`, `<stem>-p<NN>.png`, `<stem>.<newext>`.
- Never overwrite silently. Suffix `-2`, `-3`, or ask.

## Flows

1. **Extract a PDF:** extract text. Report the page count and any pages that came back empty (likely scanned images). Render those pages to PNG and flag them rather than pretending the text is complete.
2. **Convert A/V:** use a native ffmpeg one-liner. Report the exact command, output path and size. Recipes: `references/recipes.md`.
3. **Absorb a book:** extract, then log to the graph as above.

## Invariants

- Report the command you ran and where output landed, one line each.
- The shell may be fish: use `(cmd)` for substitution, not `$(cmd)`.
