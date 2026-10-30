# Contributing

1. Run the checks before sending anything:

   ```bash
   python3 -m thinkpad.cli.lint
   python3 -m unittest discover tests
   ```

2. **Skills** follow [docs/SKILL-API.md](docs/SKILL-API.md). A new skill needs a manifest, a route in the system prompt if user-triggered, and passing lint.
3. **No personal content.** Examples, docs and skills must not contain real names, paths, accounts or learner data. `thinkpad-lint` flags the common ones.
4. **Envs are data, not code.** Do not add topic-specific skills. Add an example env under `examples/envs/` instead.
5. **Pedagogy changes** (guardrails, hint ladder, `tp:learn`) should say what failure they fix, ideally with a line from an interaction log.
6. New runtimes implement `thinkpad.substrate.Substrate` (`surface`, `materialise`, `preflight`).

Licensed under Apache 2.0; contributions are under the same license.
