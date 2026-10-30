# The Ladder in Detail

Tool names are the Claude-in-Chrome tools (`mcp__claude-in-chrome__<name>`). Load them in one ToolSearch call before R1; the recipe is in `harness/tool-guidance/claude-in-chrome.md`.

Every rung has the same three beats: **Predict → Reveal → Explain.** Ask the prediction in plain words and wait for the answer before touching a tool.

## R1 — Behavior

- *Predict:* "When you type in the box, what do you think happens, and when?"
- *Reveal:* `navigate` to the target in your own tab, then `computer` (screenshot, and the interaction the learner described). For a fast interaction, record it with `gif_creator` (capture extra frames before and after) and name the file for what it shows.
- *Explain:* "Describe in your words what changed on screen. What did you not see?"
- *Evidence card:* the observed behavior, one line.

## R2 — Surface

- *Predict:* "If you had to build this page, what elements would you use? Where would the results go?"
- *Reveal:* `read_page` for the structure, `find` for the specific element the learner is curious about, `get_page_text` when the question is about copy or rendering. Show only the relevant slice, not the whole tree.
- *Explain:* "What is the minimal structure that gives this behavior?"

## R3 — Wire

- *Predict:* "What do you think the browser asks the server for? What do you think comes back?"
- *Reveal:* `read_network_requests` after performing the interaction. Walk the requests in order: method, URL path, query shape, status, payload shape. Trim to the relevant 3–5 calls. **Redact** headers, cookies, tokens and ids as `<redacted:kind>`.
- *Explain:* "Which request is the one that matters? What is in it that the page needs?"
- Never replay or modify a request against the live service.

## R4 — State

- *Predict:* "Once the data arrives, where does it live? What happens to the old data?"
- *Reveal:* only **read-only** expressions through `javascript_tool` (property reads, `typeof`, `Object.keys`, `JSON.stringify` of a small non-sensitive slice). Check `read_console_messages` with a `pattern` to keep output small. Do not call functions that mutate state, and never read storage or cookies that may hold credentials.
- *Explain:* "Draw the data flow from request to pixels in four boxes."

## R5 — Why

- *Predict (the learner argues):* "What is the obvious simpler way to build this? Why might the authors not have done that?"
- *Reveal:* nothing new. Compare their argument to the evidence cards. Where the evidence can't settle it, say "not observable from the client" and mark the claim as a hypothesis.
- *Explain:* the learner states the product problem the design solves, in one sentence.

## R6 — Rebuild

- The learner chooses the smallest slice that reproduces the R1 behavior. You may scaffold an empty project and a mock endpoint that returns the data shape from R3 (plumbing). The learner writes every line of the logic.
- Predict-then-run applies: before they run it, "what should happen?"
- Terminal follows the env's `terminal` setting. With `plumbing`, you run installs and the dev server, not tests that grade their logic.

## R7 — Diff

- Run R1 on the clone and R3 on the clone's requests. Put the two side by side with the original's evidence cards.
- Ask: "What does your version do that the original doesn't? What does the original do that yours doesn't? Which difference would you fix first, and why?"
- Mark the target `done` only when the learner has explained at least one gap in their own words.
