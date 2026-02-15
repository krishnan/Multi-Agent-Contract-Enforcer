---
name: multi-agent-contract-enforcer
description: >
  Enforces contract-first coordination in multi-agent architectures to prevent
  organizational dysfunction (bikeshedding, review thrashing, governance conflicts,
  analysis paralysis). Use when designing, reviewing, or implementing multi-agent
  systems, AI swarms, agent pipelines, or any task involving agent-to-agent
  coordination. Triggers: "multi-agent", "swarm", "agent pipeline", "agent
  coordination", "agent review", "agent delegation", "contract-first".
---

# Multi-Agent Contract Enforcer

Prevent multi-agent systems from recreating the pathologies of human bureaucracy.
Based on empirical research showing organizational dysfunction is substrate-independent
and the PACT framework (Contracts before code. Tests as law. Agents that can't cheat).

## Why This Exists

Empirical evidence demonstrates that multi-agent AI architectures fail for the same
structural reasons as human organizations. In controlled experiments:

- Single agent: 28/28 score. Every multi-agent variant scored lower.
- Hierarchical coordinator: refused to delegate (rational defection).
- 8 stigmergic agents: incompatible interfaces at every boundary.
- Gated pipeline: consumed entire budget on planning, wrote zero code.

The dysfunction correlates with coordination complexity, not agent capability.
Every additional agent introduces a communication channel where information degrades.

## The Three Laws of Coordination Failure

1. **Crawford-Sobel Degradation**: When agents communicate through compressed
   representations (approve/reject, confidence scores, review verdicts), information
   is irreversibly lost. Each coordination layer degrades signal further. Adding
   more review stages cannot recover information already discarded.

2. **Goodhart's Law**: Any metric used as an optimization target will be gamed.
   Agents that optimize "pass review" outperform agents that optimize "produce
   correct code." The gap between proxy and objective is where dysfunction lives.

3. **Data Processing Inequality**: For any chain A -> B -> C, the mutual information
   I(A;C) <= I(A;B). No post-processing of a compressed signal recovers what was
   lost at compression. More elaborate architectures operating on degraded signals
   cannot compensate.

## Core Principle: Contracts Before Code, Tests as Law

Replace subjective agent-to-agent evaluation with mechanical verification.

```
Task -> Decompose -> Contract -> Test -> Implement -> Integrate
         (2-7        (typed       (executable    (independent,    (glue +
         components)  interfaces)  tests from     parallel,        parent
                                   contracts)     competitive)     tests)
```

## Mandatory Rules When Designing Multi-Agent Systems

### RULE 1: No Subjective Evaluation Agents

NEVER create "reviewer", "evaluator", "quality assessor", or "approval gate" agents
that render subjective verdicts. These are the computational equivalent of middle
management and produce the same dysfunction.

Bad:
```
coder_agent -> reviewer_agent -> approval_gate -> deploy
```

Good:
```
contract_author -> test_author -> [validate_gate] -> code_author -> [run_tests]
```

The validate gate is MECHANICAL: do types resolve? Is the dependency graph acyclic?
Does the test code parse? No LLM judgment involved.

### RULE 2: Define Contracts Before Implementation

Every component must have a typed interface contract BEFORE any agent writes
implementation code. A contract includes:

- **Typed function signatures** with input/output specifications
- **Preconditions and postconditions** for each function
- **Error cases** with named error types and conditions
- **Module invariants** that must hold across all operations
- **Dependency declarations** (what other contracts this depends on)

```python
# Example contract structure (from PACT schemas)
ComponentContract:
  component_id: str
  name: str
  types: list[TypeSpec]         # Custom type definitions
  functions: list[FunctionContract]  # Typed function signatures
  dependencies: list[str]       # Other component IDs
  invariants: list[str]         # Must always hold
```

### RULE 3: Tests Are Generated From Contracts, Not From Code

Test suites are derived mechanically from contracts. They cover:
- Happy path (normal operation)
- Edge cases (boundary conditions)
- Error cases (each declared error)
- Invariant checks (contract-level guarantees)

Tests are the ONLY acceptance criterion. Pass or fail. No "looks good to me."

### RULE 4: Agents Implement Independently Against Shared Contracts

Each implementing agent receives ONLY:
- The component's contract
- Its dependency contracts (for mocking)
- The test suite
- Prior failure descriptions (if retrying)

Agents do NOT receive: other agents' implementations, decomposer reasoning,
or subjective feedback from evaluator agents.

### RULE 5: Minimize Agent Count

Start with ONE agent. Add agents only when the task provably exceeds a single
agent's context or capability. Every additional agent introduces a coordination
channel where Crawford-Sobel degradation operates. The default recommendation
is the fewest agents capable of completing the task.

### RULE 6: Use Mechanical Gates, Never Subjective Gates

Every decision point in the pipeline must be mechanically verifiable:

| Gate Type | Mechanical (GOOD) | Subjective (BAD) |
|-----------|-------------------|-------------------|
| Code quality | Tests pass/fail | "Code looks clean" |
| API design | Types resolve, no cycles | "Good architecture" |
| Integration | Composition tests pass | "Components work well together" |
| Completeness | All contract functions implemented | "Feels complete" |

### RULE 7: Parallel and Competitive Over Sequential Review

When multiple agents are needed:
- **Parallel**: Independent components implement concurrently (they share no state)
- **Competitive**: N agents implement the SAME component; the one whose tests
  pass with highest coverage wins
- **Never**: Sequential pipeline where Agent B reviews Agent A's work

### RULE 8: Budget-Aware Execution

Track token costs per component. If coordination overhead exceeds 20% of total
budget, the architecture has too many coordination layers. The cost of agreeing
about what to build should never exceed the cost of building it.

## Anti-Patterns to Detect and Reject

When reviewing or designing multi-agent architectures, flag these patterns:

1. **Review Chains**: Agent A writes, Agent B reviews, Agent C arbitrates.
   This is a bureaucracy. Replace with: Agent A writes, tests judge.

2. **Confidence Scoring**: Agents rating their own or others' confidence.
   This is Goodhart bait. Replace with: mechanical pass/fail gates.

3. **Escalation Hierarchies**: "If reviewer rejects, escalate to architect."
   This recreates middle management. Replace with: fix the contract if tests
   reveal a specification problem.

4. **Consensus Protocols Among Agents**: Agents voting or debating.
   Multi-agent debate shifts correct answers to incorrect more often than
   the reverse. Replace with: contracts define truth, tests verify it.

5. **Pipeline Stages > 4**: Any pipeline with more than 4 stages is likely
   spending more on coordination than production. Prefer:
   Decompose -> Contract+Test -> Implement -> Integrate.

6. **Agents Evaluating Other Agents' Output**: This is the core dysfunction.
   Tests evaluate output. Agents produce output. Never mix the roles.

## When to Apply This Skill

- Designing a new multi-agent system or agent pipeline
- Reviewing an existing multi-agent architecture for dysfunction
- Debugging coordination failures in agent swarms
- Choosing between single-agent and multi-agent approaches
- Implementing task decomposition for parallel agent execution
- Any system where one agent's output feeds another agent's input

## Quick Decision Framework

```
Is the task completable by a single agent?
  YES -> Use a single agent. Stop.
  NO  -> Does the task decompose into independent subtasks?
    YES -> Define contracts for each subtask.
           Generate tests from contracts.
           Implement subtasks in parallel (one agent each).
           Integrate with composition tests.
    NO  -> The task requires sequential state. Use a single agent
           with checkpointing. Do NOT create a pipeline.
```

## Reference

- Paper: "The Organizational Physics of Multi-Agent AI" (McEntire, 2026)
- Framework: PACT (github.com/jmcentire/pact)
- Key finding: Performance inversely correlates with coordination complexity
- Key mechanism: Crawford-Sobel degradation at every agent communication boundary
