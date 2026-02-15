# Multi-Agent-Contract-Enforcer

**Stop your AI agents from building a bureaucracy.**

A skill/instruction set for AI coding assistants that enforces contract-first coordination in multi-agent architectures. It prevents the organizational dysfunction that empirical research has shown emerges in every multi-agent system that coordinates through subjective evaluation -- regardless of how smart the agents are.

## The Problem

When you build a multi-agent AI system with reviewers, approval gates, and escalation hierarchies, you are not building a quality assurance pipeline. You are building a bureaucracy. And it will behave exactly like one.

Controlled experiments (McEntire, 2026) demonstrated this with mathematical precision:

| Architecture | Score | What Went Wrong |
|---|---|---|
| Single agent | 28/28 | Nothing. It just worked. |
| Hierarchical (delegation) | 18/28 | Coordinator refused to delegate. Did everything itself. |
| Stigmergic (8 parallel agents) | 9/28 | Incompatible interfaces at every service boundary. |
| Gated pipeline (11 stages) | 0/28 | Spent the entire budget planning. Wrote zero code. |

The dysfunction is not a bug in the agents. The agents are fine. The dysfunction is a property of the coordination architecture. Specifically, it follows from three information-theoretic constraints that apply to any system coordinating through compressed representations:

1. **Crawford-Sobel Degradation** -- Agent-to-agent communication through compressed channels (approve/reject, scores, review verdicts) irreversibly loses information. Each layer makes it worse.

2. **Goodhart's Law** -- Any metric used as an optimization target gets gamed. Agents that optimize "pass review" outperform agents that optimize "write correct code." The proxy-objective gap is where dysfunction lives.

3. **Data Processing Inequality** -- For any processing chain A to B to C, the information between A and C can never exceed the information between A and B. More elaborate architectures operating on already-degraded signals cannot compensate for what was lost upstream.

## The Solution: Contracts Before Code

The PACT framework (github.com/jmcentire/pact) replaces subjective agent-to-agent evaluation with mechanical verification:

```
Task -> Decompose -> Contract -> Test -> Implement -> Integrate
        (2-7 parts)  (typed      (from     (parallel,   (glue code
                      interfaces) contracts) competitive) + parent tests)
```

The key insight: LLMs are unreliable reviewers but tests are perfectly reliable judges. So you define the contracts first, generate the tests from the contracts, and let agents iterate until they pass. No advisory coordination. No "looks good to me." Pass or fail.

This skill enforces these principles whenever you work with multi-agent architectures in your AI coding assistant.

## What the Skill Does

When triggered (by keywords like "multi-agent", "swarm", "agent pipeline", "agent coordination"), the skill:

- Rejects subjective evaluation agents (reviewers, approval gates, quality assessors)
- Requires typed interface contracts before any implementation
- Mandates test suites generated from contracts as the sole acceptance criterion
- Flags anti-patterns: review chains, confidence scoring, escalation hierarchies, consensus protocols
- Enforces the "minimum viable agent count" principle
- Provides a decision framework for choosing single-agent vs. multi-agent approaches

## Installation

### Claude Code

Claude Code uses skills stored in `.claude/skills/` directories. Skills are discovered automatically based on their description metadata.

**Project-level install** (recommended for team sharing via git):

```bash
# From your project root
mkdir -p .claude/skills/multi-agent-contract-enforcer
cp claude/SKILL.md .claude/skills/multi-agent-contract-enforcer/SKILL.md

# Optional: include the validation script
mkdir -p .claude/skills/multi-agent-contract-enforcer/scripts
cp claude/scripts/validate_architecture.py \
   .claude/skills/multi-agent-contract-enforcer/scripts/
```

**User-level install** (applies to all your projects):

```bash
mkdir -p ~/.claude/skills/multi-agent-contract-enforcer
cp claude/SKILL.md ~/.claude/skills/multi-agent-contract-enforcer/SKILL.md

# Optional: validation script
mkdir -p ~/.claude/skills/multi-agent-contract-enforcer/scripts
cp claude/scripts/validate_architecture.py \
   ~/.claude/skills/multi-agent-contract-enforcer/scripts/
```

**Verification**: In Claude Code, ask "What skills do you have?" or reference multi-agent architecture in a prompt. Claude should automatically load and apply the skill based on the description triggers.

**Using the validation script**: If you have an architecture description in YAML or JSON format, you can run the validator directly:

```bash
python .claude/skills/multi-agent-contract-enforcer/scripts/validate_architecture.py \
  my_architecture.yaml
```

### Gemini CLI (Google)

Gemini CLI uses `GEMINI.md` context files loaded hierarchically from global, project, and subdirectory locations.

**Project-level install** (recommended):

```bash
# From your project root
cp gemini/GEMINI.md ./GEMINI.md
```

If you already have a `GEMINI.md` at project root, append the content or use the import syntax:

```markdown
# In your existing GEMINI.md
@./multi-agent-contract-enforcer/GEMINI.md
```

Then place the file:

```bash
mkdir -p multi-agent-contract-enforcer
cp gemini/GEMINI.md multi-agent-contract-enforcer/GEMINI.md
```

**Global install** (applies to all your projects):

```bash
# Append to your global GEMINI.md
cat gemini/GEMINI.md >> ~/.gemini/GEMINI.md
```

Or use modular imports:

```bash
mkdir -p ~/.gemini/skills
cp gemini/GEMINI.md ~/.gemini/skills/multi-agent-contract-enforcer.md
```

Then in `~/.gemini/GEMINI.md`:

```markdown
@./skills/multi-agent-contract-enforcer.md
```

**Verification**: Run `gemini` and type `/memory show`. You should see the Multi-Agent Contract Enforcer instructions in the loaded context. Alternatively, ask about multi-agent architecture and verify it applies the contract-first principles.

**Firebase/IDX**: If using Gemini in Firebase (Project IDX), place the file at project root as `GEMINI.md` or `airules.md` and rebuild the workspace.

### GitHub Copilot

GitHub Copilot supports custom instructions through `.github/copilot-instructions.md` and `AGENTS.md` files.

**Repository-level install** (recommended for team sharing):

```bash
# From your project root
mkdir -p .github
cp github/.github/copilot-instructions.md .github/copilot-instructions.md
```

If you already have a `.github/copilot-instructions.md`, append the content:

```bash
echo "" >> .github/copilot-instructions.md
cat github/.github/copilot-instructions.md >> .github/copilot-instructions.md
```

**Using AGENTS.md** (cross-agent compatible, works with Copilot, Codex, and other agents):

```bash
cp github/AGENTS.md ./AGENTS.md
cp -r github/.github .github
```

**Path-specific install** (apply only to agent-related code):

```bash
mkdir -p .github/instructions
cat > .github/instructions/multi-agent.instructions.md << 'EOF'
---
applyTo: "**/agents/**,**/swarm/**,**/pipeline/**,**/multi_agent/**"
---

EOF
cat github/.github/copilot-instructions.md >> \
  .github/instructions/multi-agent.instructions.md
```

**Verification**: In VS Code with Copilot, open Chat and ask about multi-agent architecture. Check the References list in the response -- you should see `.github/copilot-instructions.md` listed as a reference. You can also check Settings > Extensions > GitHub Copilot > "Use Instruction Files" is enabled.

**Copilot CLI**: The instructions are loaded automatically when Copilot CLI starts. After editing, restart Copilot CLI or use `/resume SESSION-ID` to reload.

## Cross-Platform Install (All Three at Once)

If your team uses multiple AI coding assistants:

```bash
# From your project root
# Claude Code
mkdir -p .claude/skills/multi-agent-contract-enforcer/scripts
cp claude/SKILL.md .claude/skills/multi-agent-contract-enforcer/SKILL.md
cp claude/scripts/validate_architecture.py \
   .claude/skills/multi-agent-contract-enforcer/scripts/

# Gemini CLI
cp gemini/GEMINI.md ./GEMINI.md  # or append to existing

# GitHub Copilot
mkdir -p .github
cp github/.github/copilot-instructions.md .github/copilot-instructions.md
cp github/AGENTS.md ./AGENTS.md
```

All three files encode the same principles. They differ only in format and metadata conventions for each platform.

## How It Works in Practice

### Before (typical multi-agent anti-pattern)

```
User Request
  -> Planner Agent (decomposes task)
    -> Architect Agent (designs solution)
      -> Architect Review Agent (reviews design)  <-- middle management
        -> Coder Agent (writes code)
          -> Code Review Agent (reviews code)      <-- middle management
            -> QA Agent (checks quality)            <-- middle management
              -> Integration Agent (assembles)
                -> Final Review Agent               <-- middle management
```

Result: 0/28 score. Budget exhausted on planning and review. Zero working code produced.

### After (contract-first, enforced by this skill)

```
User Request
  -> Decompose (2-7 independent components)
  -> For each component:
       Contract Author -> Test Author -> [Mechanical Validation Gate]
  -> For each validated component:
       Code Author -> [Run Contract Tests] -> pass/fail
  -> Integrate (glue code + parent-level composition tests)
```

Result: 28/28 score (single agent) or parallel implementation with shared contracts.

## Core Principles (Quick Reference)

1. **No subjective evaluation agents.** Tests are the only judge.
2. **Contracts before code.** Typed interfaces defined before implementation.
3. **Tests from contracts.** Executable test suites derived mechanically.
4. **Independent implementation.** Agents get contract + tests, nothing else.
5. **Minimize agent count.** Start with one. Justify each addition.
6. **Mechanical gates only.** Pass/fail, not "looks good."
7. **Parallel over sequential.** Independent components, concurrent execution.
8. **Budget awareness.** Coordination overhead below 20%.

## Theoretical Foundation

The skill is grounded in three bodies of work:

**Information Theory**: Crawford-Sobel (1982) proved that sender-receiver communication degrades as objectives diverge. The Data Processing Inequality guarantees this degradation is irreversible across processing chains.

**Organizational Economics**: Goodhart's Law (1975) establishes that any proxy metric used as a target ceases to measure what it was designed to measure. Skalse et al. (2022) formalized this: no non-trivial proxy reward can be guaranteed unhackable.

**Empirical AI Research**: Chen et al. (2025) found multi-agent variants degrade sequential reasoning by 39-70%. Pappu et al. (2026) showed LLM teams underperform their best individual member by 8-38%. Xu et al. (2026) demonstrated a single agent matches homogeneous multi-agent workflows.

## References

- McEntire, J. (2026). "The Organizational Physics of Multi-Agent AI: Substrate-Independent Dysfunction in Autonomous Software Engineering Swarms."
- PACT Framework: https://github.com/jmcentire/pact
- Crawford, V. & Sobel, J. (1982). "Strategic Information Transmission." Econometrica.
- Goodhart, C. (1975). "Problems of Monetary Management."
- Chen, L. et al. (2025). "Towards a Science of Scaling Agent Systems." Google Research.
- Pappu, A. et al. (2026). "Multi-Agent Teams Hold Experts Back."
- Xu, Z. et al. (2026). "Rethinking the Value of Multi-Agent Workflow."

## License

Apache 2.0
