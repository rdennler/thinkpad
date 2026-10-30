# Tool Guidance — Claude in Chrome

Used by `tp:reverse-engineer` on web targets. These are the browser tools (`mcp__claude-in-chrome__*`) that act in the learner's real Chrome.

## Loading

The tools may be deferred. Load everything the task needs in **one** ToolSearch call:

```
select:mcp__claude-in-chrome__tabs_context_mcp,mcp__claude-in-chrome__tabs_create_mcp,mcp__claude-in-chrome__navigate,mcp__claude-in-chrome__computer,mcp__claude-in-chrome__read_page,mcp__claude-in-chrome__find,mcp__claude-in-chrome__get_page_text,mcp__claude-in-chrome__read_network_requests,mcp__claude-in-chrome__read_console_messages,mcp__claude-in-chrome__javascript_tool,mcp__claude-in-chrome__gif_creator
```

## Which tool for which question

| Question | Tool |
|---|---|
| What tabs are open? | `tabs_context_mcp` (always first in a session) |
| Open the target | `tabs_create_mcp`, then `navigate` |
| What does it look like or do? | `computer` (screenshot, click, type), `gif_creator` for a recording |
| How is it structured? | `read_page`, `find` |
| What text is on it? | `get_page_text` |
| What did it ask the server? | `read_network_requests` |
| What did it log or throw? | `read_console_messages` with a `pattern` |
| What is the value of X in the page? | `javascript_tool`, read-only expressions |

## Habits

- Open a **new tab** for the target. Never reuse a tab id from a previous session; if a tool says the tab is invalid, call `tabs_context_mcp` again.
- Filter console output with `pattern`; unfiltered logs flood the context.
- Keep tool output small: ask for the slice you need.
- GIFs: capture extra frames before and after the action, and give the file a meaningful name.
- Don't trigger `alert`, `confirm` or `prompt`. They block the extension. If one appears, tell the learner to dismiss it.
- After two failed attempts on the same action, stop and ask. Don't loop.

Safety rules for what you may do with these tools: `harness/guardrails/web-safety.md`.
