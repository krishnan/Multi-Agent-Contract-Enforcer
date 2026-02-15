#!/usr/bin/env python3
"""Validate a multi-agent architecture description for dysfunction patterns.

Usage: python validate_architecture.py <architecture_description_file>

Reads a YAML or JSON file describing an agent architecture and checks for
known dysfunction patterns documented in "The Organizational Physics of
Multi-Agent AI" (McEntire, 2026).
"""

import json
import sys
from pathlib import Path

try:
    import yaml
    HAS_YAML = True
except ImportError:
    HAS_YAML = False


DYSFUNCTION_PATTERNS = {
    "review_chain": {
        "keywords": ["reviewer", "review_agent", "code_review", "approval_gate",
                      "quality_check", "evaluator", "assessor", "judge_agent"],
        "severity": "HIGH",
        "description": "Subjective review agents create Crawford-Sobel degradation",
        "fix": "Replace with mechanical test verification against contracts",
    },
    "escalation_hierarchy": {
        "keywords": ["escalate", "arbiter", "escalation", "override",
                      "force_approve", "supervisor", "manager_agent"],
        "severity": "HIGH",
        "description": "Escalation hierarchies recreate middle management",
        "fix": "Remove escalation layers; use contract tests as the sole arbiter",
    },
    "confidence_scoring": {
        "keywords": ["confidence_score", "confidence_threshold", "quality_score",
                      "rating", "score_gate", "confidence_gate"],
        "severity": "MEDIUM",
        "description": "Confidence scores are Goodhart-vulnerable proxies",
        "fix": "Replace with binary pass/fail mechanical gates (tests pass or not)",
    },
    "consensus_protocol": {
        "keywords": ["vote", "consensus", "debate", "deliberation",
                      "majority", "agreement", "negotiate"],
        "severity": "MEDIUM",
        "description": "Agent consensus shifts correct answers to incorrect more often than reverse",
        "fix": "Define truth via contracts; verify via tests; no voting",
    },
    "excessive_pipeline": {
        "keywords": [],  # checked by stage count
        "severity": "HIGH",
        "description": "Pipelines with >4 stages spend more on coordination than production",
        "fix": "Reduce to: decompose -> contract+test -> implement -> integrate",
    },
    "agent_evaluates_agent": {
        "keywords": ["review_output", "check_work", "validate_code",
                      "assess_quality", "grade_output", "feedback_loop"],
        "severity": "HIGH",
        "description": "Agents evaluating other agents' output is the core dysfunction",
        "fix": "Only tests evaluate output; agents only produce output",
    },
}


def load_architecture(filepath: str) -> dict:
    """Load architecture description from YAML or JSON."""
    path = Path(filepath)
    content = path.read_text()

    if path.suffix in (".yaml", ".yml"):
        if not HAS_YAML:
            print("ERROR: pyyaml required for YAML files. Install: pip install pyyaml")
            sys.exit(1)
        return yaml.safe_load(content)
    elif path.suffix == ".json":
        return json.loads(content)
    else:
        # try JSON first, then YAML
        try:
            return json.loads(content)
        except json.JSONDecodeError:
            if HAS_YAML:
                return yaml.safe_load(content)
            raise ValueError(f"Cannot parse {filepath}. Use .json or .yaml format.")


def check_keywords(text: str, keywords: list[str]) -> list[str]:
    """Check if any dysfunction keywords appear in the text."""
    text_lower = text.lower()
    return [kw for kw in keywords if kw.lower() in text_lower]


def flatten_to_text(obj, depth=0) -> str:
    """Recursively flatten a dict/list to searchable text."""
    if depth > 10:
        return ""
    if isinstance(obj, str):
        return obj
    if isinstance(obj, dict):
        parts = []
        for k, v in obj.items():
            parts.append(str(k))
            parts.append(flatten_to_text(v, depth + 1))
        return " ".join(parts)
    if isinstance(obj, (list, tuple)):
        return " ".join(flatten_to_text(item, depth + 1) for item in obj)
    return str(obj)


def count_stages(arch: dict) -> int:
    """Count pipeline stages in the architecture."""
    stages = arch.get("stages", arch.get("pipeline", arch.get("phases", [])))
    if isinstance(stages, list):
        return len(stages)
    if isinstance(stages, dict):
        return len(stages)
    return 0


def count_agents(arch: dict) -> int:
    """Count agents in the architecture."""
    agents = arch.get("agents", arch.get("roles", arch.get("workers", [])))
    if isinstance(agents, (list, dict)):
        return len(agents)
    return 0


def validate(arch: dict) -> list[dict]:
    """Run all dysfunction checks. Returns list of findings."""
    findings = []
    full_text = flatten_to_text(arch)

    for pattern_name, pattern in DYSFUNCTION_PATTERNS.items():
        if pattern_name == "excessive_pipeline":
            stage_count = count_stages(arch)
            if stage_count > 4:
                findings.append({
                    "pattern": pattern_name,
                    "severity": pattern["severity"],
                    "description": pattern["description"],
                    "fix": pattern["fix"],
                    "evidence": f"Found {stage_count} stages (max recommended: 4)",
                })
            continue

        matched = check_keywords(full_text, pattern["keywords"])
        if matched:
            findings.append({
                "pattern": pattern_name,
                "severity": pattern["severity"],
                "description": pattern["description"],
                "fix": pattern["fix"],
                "evidence": f"Keywords found: {', '.join(matched)}",
            })

    # Check agent count
    agent_count = count_agents(arch)
    if agent_count > 7:
        findings.append({
            "pattern": "excessive_agents",
            "severity": "MEDIUM",
            "description": f"Architecture has {agent_count} agents. More agents = more coordination overhead.",
            "fix": "Reduce to minimum viable agent count. Start with 1, justify each addition.",
            "evidence": f"Agent count: {agent_count}",
        })

    # Check for contract-first indicators (positive)
    has_contracts = any(
        kw in full_text.lower()
        for kw in ["contract", "interface_spec", "typed_interface", "componentcontract"]
    )
    has_tests = any(
        kw in full_text.lower()
        for kw in ["test_suite", "contract_test", "mechanical_gate", "pass_fail"]
    )

    if not has_contracts:
        findings.append({
            "pattern": "missing_contracts",
            "severity": "HIGH",
            "description": "No contract definitions found. Agents will produce incompatible interfaces.",
            "fix": "Define typed interface contracts BEFORE implementation begins.",
            "evidence": "No contract-related keywords in architecture description",
        })

    if not has_tests:
        findings.append({
            "pattern": "missing_test_gates",
            "severity": "HIGH",
            "description": "No mechanical test gates found. Acceptance will rely on subjective evaluation.",
            "fix": "Generate executable tests from contracts. Tests are the only acceptance criterion.",
            "evidence": "No test-gate-related keywords in architecture description",
        })

    return findings


def main():
    if len(sys.argv) < 2:
        print("Usage: python validate_architecture.py <architecture_file.yaml|json>")
        print("\nValidates a multi-agent architecture for dysfunction patterns.")
        sys.exit(1)

    filepath = sys.argv[1]
    if not Path(filepath).exists():
        print(f"ERROR: File not found: {filepath}")
        sys.exit(1)

    arch = load_architecture(filepath)
    findings = validate(arch)

    if not findings:
        print("PASS: No dysfunction patterns detected.")
        print("Architecture appears to follow contract-first coordination principles.")
        sys.exit(0)

    print(f"FINDINGS: {len(findings)} potential dysfunction pattern(s) detected\n")

    for i, f in enumerate(findings, 1):
        print(f"  [{f['severity']}] {i}. {f['pattern']}")
        print(f"    Problem:  {f['description']}")
        print(f"    Evidence: {f['evidence']}")
        print(f"    Fix:      {f['fix']}")
        print()

    high_count = sum(1 for f in findings if f["severity"] == "HIGH")
    if high_count > 0:
        print(f"FAIL: {high_count} HIGH severity issue(s). Architecture needs redesign.")
        sys.exit(1)
    else:
        print("WARN: Issues found but none are HIGH severity. Review recommended.")
        sys.exit(0)


if __name__ == "__main__":
    main()
