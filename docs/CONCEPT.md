# Concept

## The problem

Asking an AI to help you learn usually means asking it to do the work. You get a working answer and no new skill. The faster the agent, the worse this gets.

## The idea

Treat tutoring as a harness problem. The model is fixed. What changes the outcome is the system around it:

- **Guardrails** that forbid handing over the target.
- **Skills** that make each learning move repeatable: the hint ladder, the verbalization gate, predict-then-reveal.
- **Memory** that survives between sessions, so "where was I" costs nothing.
- **A schedule** derived from your own commitments, so the agent names today's block before anything else.
- **A feedback loop**: retros turn how a session felt into concrete proposals to change the harness itself.

## The learner's contract

1. You write the thing being learned. The agent scaffolds around it.
2. You predict before the agent reveals.
3. You explain it back in your own words before a unit counts as done.
4. Consistency is the metric. The agent never reports minutes and never guilts a missed day.

## Learning by reverse engineering

Building from a blank page is slow when you don't know what good looks like. Taking apart something that works is faster: see the behavior, guess how it's built, check, then rebuild a small version yourself. `tp:reverse-engineer` does this against live websites in your own Chrome, one rung at a time, or against source code.

## What thinkPad is not

- Not a curriculum. You bring the topic; envs are empty on purpose.
- Not an autograder. Grills are manual and low stakes.
- Not a time tracker.
