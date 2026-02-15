# Multi-Agent Contract Enforcer

When designing, reviewing, or implementing multi-agent AI systems, agent pipelines,
or swarm architectures, enforce the following contract-first coordination principles.
These are grounded in empirical research showing organizational dysfunction is
substrate-independent (McEntire, 2026) and the PACT framework (github.com/jmcentire/pact).

## Why

Controlled experiments show performance inversely correlates with coordination complexity:
single agent scored 28/28; hierarchical 18/28; stigmergic 9/28; gated pipeline 0/28.
Every additional coordination layer degrades signal (Crawford-Sobel), gets gamed
(Goodhart's Law), and cannot recover lost information (Data Processing Inequality).

## Rules

Never create reviewer, evaluator, or approval gate agents that render subjective verdicts. Tests are the only judge. No "looks good to me."

Every component must have a typed interface contract (function signatures, pre/postconditions, error cases, invariants, dependencies) BEFORE any implementation code is written.

Test suites must be derived mechanically from contracts, covering happy path, edge cases, error cases, and invariant checks. Tests are the sole acceptance criterion.

Implementing agents receive only: the contract, dependency contracts for mocking, the test suite, and prior failure descriptions if retrying. Never other agents' implementations.

Start with one agent. Add agents only when provably needed. Every additional agent introduces information degradation at the communication boundary.

Every decision point must be mechanically verifiable: tests pass/fail, types resolve, no cycles in dependency graph. Never subjective quality assessment.

For multi-agent work, prefer parallel implementation of independent components or competitive implementation (N agents on same component, best test results win). Never sequential review chains.

If coordination overhead exceeds 20% of total budget, the architecture has too many coordination layers.

## Anti-Patterns to Flag

Review chains (agent writes, agent reviews, agent arbitrates) should be replaced with agent writes, tests judge.

Confidence scoring is Goodhart bait. Replace with binary pass/fail mechanical gates.

Escalation hierarchies recreate middle management. Remove them; contracts and tests are the sole arbiter.

Agent consensus or voting shifts correct answers to incorrect more often than the reverse. Contracts define truth, tests verify it.

Pipelines with more than 4 stages spend more on coordination than production. Reduce to decompose, contract-and-test, implement, integrate.

Agents evaluating other agents' output is the core dysfunction. Tests evaluate output, agents produce output. Never mix roles.

## Quick Decision

If a single agent can complete the task, use one agent. If not, decompose into independent subtasks, define contracts, generate tests, implement in parallel, integrate with composition tests. If the task requires sequential state that cannot decompose, use a single agent with checkpointing rather than a pipeline.

## Architecture Template

```
Task -> Decompose (2-7 components)
     -> Contract (typed interfaces per component)
     -> Test (executable tests from contracts)
     -> Implement (parallel, one agent per component)
     -> Integrate (glue code + parent-level tests)
```

## Reference
Paper: "The Organizational Physics of Multi-Agent AI" (McEntire, 2026)
Framework: PACT - github.com/jmcentire/pact
