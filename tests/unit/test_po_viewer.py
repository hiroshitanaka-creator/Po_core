import json

from click.testing import CliRunner

from po_core.cli import main
from po_core.ensemble import run_ensemble
from po_core.po_viewer import build_viewer_payload


EXPECTED_TENSION_TEMPLATE = [
    {
        "philosopher": "aristotle",
        "confidence": 0.88,
        "tension": 0.12,
        "drivers": [
            "Aristotle reflects on 'What does it mean to live authentically?'.",
            "analysis",
            "deterministic",
        ],
    },
    {
        "philosopher": "nietzsche",
        "confidence": 0.83,
        "tension": 0.17,
        "drivers": [
            "Nietzsche reflects on 'What does it mean to live authentically?'.",
            "analysis",
            "deterministic",
        ],
    },
    {
        "philosopher": "wittgenstein",
        "confidence": 0.78,
        "tension": 0.22,
        "drivers": [
            "Wittgenstein reflects on 'What does it mean to live authentically?'.",
            "analysis",
            "deterministic",
        ],
    },
]

EXPECTED_PRESSURE_TEMPLATE = [
    {
        "dimension": "aristotle",
        "pressure": 0.66,
        "narrative": "Confidence-weighted ethical guard from aristotle",
    },
    {
        "dimension": "nietzsche",
        "pressure": 0.62,
        "narrative": "Confidence-weighted ethical guard from nietzsche",
    },
    {
        "dimension": "wittgenstein",
        "pressure": 0.58,
        "narrative": "Confidence-weighted ethical guard from wittgenstein",
    },
]


def _expected_semantic(prompt: str) -> list[dict]:
    return [
        {
            "stage": "prompt",
            "signal": prompt,
            "influence": ["user"],
            "cumulative_meaning": "User intent seeds the reasoning graph.",
        },
        {
            "stage": "ensemble",
            "signal": " | ".join(
                [
                    "Aristotle reflects on 'What does it mean to live authentically?'.",
                    "Nietzsche reflects on 'What does it mean to live authentically?'.",
                    "Wittgenstein reflects on 'What does it mean to live authentically?'.",
                ]
            ),
            "influence": ["aristotle", "nietzsche", "wittgenstein"],
            "cumulative_meaning": "Deterministic philosophers contribute weighted reflections.",
        },
        {
            "stage": "trace",
            "signal": "ensemble_started → ensemble_completed",
            "influence": ["system"],
            "cumulative_meaning": "System-level lifecycle ready for visualization layers.",
        },
    ]


def _expected_source_trace(prompt: str) -> dict:
    return {
        "prompt": prompt,
        "philosophers": ["aristotle", "nietzsche", "wittgenstein"],
        "created_at": "<timestamp>",
        "events": [
            {"event": "ensemble_started", "philosophers": 3},
            {"event": "ensemble_completed", "results_recorded": 3, "status": "ok"},
        ],
    }


def _normalize_dynamic_fields(payload: dict) -> dict:
    normalized = dict(payload)
    normalized["generated_at"] = "<timestamp>"
    normalized["source_trace"] = dict(payload.get("source_trace", {}))
    normalized["source_trace"]["created_at"] = "<timestamp>"
    return normalized


def test_build_viewer_payload_shapes_trace(sample_prompt):
    trace = run_ensemble(sample_prompt)
    payload = build_viewer_payload(trace).to_dict()

    normalized = _normalize_dynamic_fields(payload)
    assert normalized == {
        "prompt": sample_prompt,
        "generated_at": "<timestamp>",
        "tension_map": EXPECTED_TENSION_TEMPLATE,
        "ethical_pressure": EXPECTED_PRESSURE_TEMPLATE,
        "semantic_evolution": _expected_semantic(sample_prompt),
        "source_trace": _expected_source_trace(sample_prompt),
    }


def test_cli_viewer_export_outputs_json(sample_prompt):
    runner = CliRunner()
    result = runner.invoke(main, ["viewer", "export", sample_prompt, "--format", "json"])

    assert result.exit_code == 0
    payload = json.loads(result.output)

    normalized = _normalize_dynamic_fields(payload)
    assert normalized["prompt"] == sample_prompt
    assert normalized["tension_map"] == EXPECTED_TENSION_TEMPLATE
    assert normalized["ethical_pressure"] == EXPECTED_PRESSURE_TEMPLATE
    assert normalized["semantic_evolution"] == _expected_semantic(sample_prompt)
    assert normalized["source_trace"]["events"] == _expected_source_trace(sample_prompt)["events"]
