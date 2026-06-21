#!/usr/bin/env python3
"""Generate starter leadership artifacts from built-in templates."""

from __future__ import annotations

import argparse
from pathlib import Path
from textwrap import dedent


ARTIFACTS: dict[str, str] = {
    "board-report": """
        # Board / Shareholder Technology Report

        ## Executive Summary
        - Reporting period:
        - Business objective:
        - Current technology posture:
        - Top decision needed:
        - Material change since last report:

        ## Scorecard
        | Area | Status | Trend | Evidence | Owner | Next action |
        |---|---|---|---|---|---|
        | Strategy / roadmap | | | | | |
        | Delivery predictability | | | | | |
        | Reliability / incidents | | | | | |
        | Cybersecurity / risk | | | | | |
        | Audit / compliance | | | | | |
        | Finance / budget | | | | | |
        | People / organization | | | | | |

        ## Decisions Requested
        | Decision | Options | Recommendation | Deadline | Consequence of delay |
        |---|---|---|---|---|
        | | | | | |
    """,
    "roadmap": """
        # Technology Roadmap

        ## Context
        - Business outcome:
        - Strategy horizon:
        - Constraints:
        - Risk appetite:

        ## Portfolio Allocation
        | Category | Capacity % | Major work | Risk if underfunded |
        |---|---:|---|---|
        | Run | | | |
        | Grow | | | |
        | Transform | | | |
        | Protect | | | |

        ## Roadmap
        | Horizon | Initiative | Outcome | Owner | Dependencies | Cyber/risk impact | Funding | Exit criteria |
        |---|---|---|---|---|---|---|---|
        | 0-90 days | | | | | | | |
        | 3-12 months | | | | | | | |
        | 1-3 years | | | | | | | |
    """,
    "cyber-strategy": """
        # Cybersecurity Strategy Brief

        ## Business Context
        - Critical business processes:
        - Crown jewels:
        - Regulatory/customer obligations:
        - Risk appetite:

        ## Accountability
        | Area | Accountable role | Operator | Risk acceptor | Evidence owner |
        |---|---|---|---|---|
        | Cyber strategy | | | | |
        | IAM/PAM | | | | |
        | SOC/detection | | | | |
        | Incident response | | | | |
        | AppSec | | | | |
        | Data security/privacy | | | | |
        | Third-party risk | | | | |

        ## Board Metrics
        - Critical asset owner coverage:
        - MFA/PAM coverage:
        - Critical vulnerability age:
        - Detection coverage:
        - Incident tabletop status:
        - Backup restore test:
        - Audit findings age:
        - Exceptions age:
        - Funding gap:
    """,
    "risk-register": """
        # Technology Risk Register

        | ID | Risk statement | Category | Impact | Likelihood | Current controls | Treatment | Owner | Due date | Status |
        |---|---|---|---|---|---|---|---|---|---|
        | R-001 | Because ..., ... may ..., causing ... | Delivery / Cyber / Finance / People / Compliance / Reliability | | | | Mitigate / Accept / Avoid / Transfer | | | |
    """,
    "reliability-review": """
        # Risk And Reliability Review

        ## Scope
        - Business process / system:
        - Critical users / customers:
        - Risk owner:
        - Risk appetite:

        ## Iceberg Scan
        | Visible event/signal | Hidden contributor | Evidence | Confidence | Next data needed |
        |---|---|---|---|---|
        | | | | | |

        ## Control Map
        | Risk | Barrier | Redundancy | Recovery | Last tested | Gap |
        |---|---|---|---|---|---|
        | | | | | | |

        ## Human Reliability
        | Behavior/event | Classification | Context/system factors | Response |
        |---|---|---|---|
        | | Error / At-risk choice / Reckless choice / Intentional harm | | |
    """,
    "performance-system": """
        # Performance Management System

        ## KRA / CSF / KPI Cascade
        | KRA | Critical success factor | Critical information | KPI | Owner | Source | Threshold | Decision trigger |
        |---|---|---|---|---|---|---|---|
        | | | | | | | | |

        ## Balanced Scorecard
        | Perspective | Objective | KPI | Target | Trend | Decision needed |
        |---|---|---|---|---|---|
        | Business value | | | | | |
        | Customer/stakeholder | | | | | |
        | Internal process | | | | | |
        | Learning/capability | | | | | |
        | Risk/resilience | | | | | |

        ## Improvement Backlog
        | Metric miss | RCA method | Action | Owner | Due date | Evidence |
        |---|---|---|---|---|---|
        | | 5 Whys / Fishbone / FMEA / CRT / DMAIC / Inquiry | | | | |
    """,
    "quantification-map": """
        # Executive And Managerial Quantification Map

        ## Context
        - Role:
        - Audience:
        - Business objective:
        - Reporting cadence:

        ## Executive Scorecard
        | Domain | Metric | Trend | Target/appetite | Interpretation | Decision ask | Confidence |
        |---|---|---|---|---|---|---|
        | Business value | | | | | | |
        | Portfolio allocation | | | | | | |
        | Roadmap confidence | | | | | | |
        | Reliability/resilience | | | | | | |
        | Cyber/IAM | | | | | | |
        | Financial discipline | | | | | | |
        | Technical debt/architecture | | | | | | |
        | People/org | | | | | | |
        | AI/data | | | | | | |

        ## Manager System Metrics
        | Signal | Metric | Current | Risk | Action |
        |---|---|---|---|---|
        | 1:1 health | | | | |
        | Skip-level coverage | | | | |
        | Feedback quality | | | | |
        | Delegation | | | | |
        | Manager load | | | | |
        | Team health | | | | |
    """,
    "skip-level-review": """
        # Skip-Level Signal Map

        ## Scope
        - Organization/team:
        - Leader:
        - Managers in scope:
        - Review period:
        - Confidentiality boundary:

        ## Coverage
        | Team | Format | People reached | Target coverage | Date | Notes |
        |---|---|---:|---:|---|---|
        | | 1:1 / Group / Office hours / Observation | | | | |

        ## Themes
        | Theme | Evidence | Teams affected | Severity | Confidence | Manager/system owner | Action |
        |---|---|---|---|---|---|---|
        | | | | Low / Medium / High | Low / Medium / High | | |

        ## Manager Accountability Review
        | Manager | Team health | Escalation quality | Delegation | Feedback/1:1 health | Follow-through | Support needed |
        |---|---|---|---|---|---|---|
        | | | | | | | |
    """,
    "ai-data-rd-evaluation": """
        # AI / Data / R&D Evaluation

        ## Decision Context
        - Initiative:
        - Business problem:
        - User / customer:
        - Requested decision:

        ## Hypothesis And Evaluation
        | Hypothesis | Type | Prediction | Evaluation method | Success threshold |
        |---|---|---|---|---|
        | | Universal / Existential / Statistical / Working / Compound | | | |

        ## Agent / AI Governance
        | Layer | Design | Risk | Control |
        |---|---|---|---|
        | Inputs/context | | | |
        | Memory/state | | | |
        | Decision engine | | | |
        | Learning loop | | | |
        | Actions/tools | | | |
        | Monitoring/logging | | | |

        ## ROI And Value
        | Value type | Baseline | Expected impact | Confidence | Evidence |
        |---|---|---|---|---|
        | Cost | | | | |
        | Revenue/mission | | | | |
        | Risk reduction | | | | |
        | Customer trust | | | | |
    """,
    "org-review": """
        # Engineering Organization Review

        ## Team Map
        | Team | Mission | Manager | Headcount | Systems owned | Stakeholders | Dependencies |
        |---|---|---|---:|---|---|---|
        | | | | | | | |

        ## Capacity Allocation
        | Team | Run | Grow | Transform | Protect | Notes |
        |---|---:|---:|---:|---:|---|
        | | | | | | |

        ## Risks
        - Decision rights:
        - Manager span:
        - Succession:
        - Critical systems:
        - Cyber/security ownership:
    """,
    "appraisal": """
        # Appraisal And 360 Calibration

        ## Person / Role
        - Name:
        - Role:
        - Level:
        - Period:

        ## Evidence
        | Dimension | Evidence | Impact | Feedback source |
        |---|---|---|---|
        | Outcomes | | | |
        | Technical judgment | | | |
        | Collaboration | | | |
        | Reliability/security ownership | | | |
        | Leadership at level | | | |

        ## Calibration
        - Proposed rating:
        - Evidence quality:
        - Bias checks:
        - Final rating:
    """,
    "meeting-brief": """
        # Leadership Meeting Brief

        ## Meeting
        - Purpose:
        - Audience:
        - Decision/input needed:
        - Owner:

        ## Pre-Read
        - Context:
        - Current evidence:
        - Options:
        - Risks:
        - Recommendation:

        ## Decisions And Actions
        | Decision/action | Owner | Due date | Evidence of completion |
        |---|---|---|---|
        | | | | |
    """,
}


def render(kind: str) -> str:
    if kind not in ARTIFACTS:
        known = ", ".join(sorted(ARTIFACTS))
        raise SystemExit(f"Unknown artifact type '{kind}'. Known types: {known}")
    return dedent(ARTIFACTS[kind]).strip() + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate a starter technology leadership artifact.")
    parser.add_argument("--type", required=True, choices=sorted(ARTIFACTS), help="Artifact type to generate")
    parser.add_argument("--output", "-o", help="Output file. Defaults to stdout.")
    args = parser.parse_args()

    content = render(args.type)
    if args.output:
        path = Path(args.output)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        print(f"[ok] wrote {path}")
    else:
        print(content, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
