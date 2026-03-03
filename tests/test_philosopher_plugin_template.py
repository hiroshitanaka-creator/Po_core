from po_core.domain.context import Context
from po_core.domain.intent import Intent
from po_core.domain.keys import CITATIONS, PO_CORE, RATIONALE
from po_core.domain.memory_snapshot import MemorySnapshot
from po_core.domain.proposal import Proposal
from po_core.domain.tensor_snapshot import TensorSnapshot
from po_core.philosophers.template import TemplatePhilosopher


def test_template_reason_contract_minimum_keys() -> None:
    ph = TemplatePhilosopher()

    out = ph.reason("  test prompt  ")

    assert "reasoning" in out
    assert "perspective" in out
    assert "metadata" in out
    assert out["metadata"]["philosopher"] == "Template Philosopher"


def test_template_propose_contract_po_core_fields() -> None:
    ph = TemplatePhilosopher()

    ctx = Context.now(request_id="plugin-template-001", user_input="What should we do?")
    proposals = ph.propose(
        ctx, Intent.neutral(), TensorSnapshot.empty(), MemorySnapshot.empty()
    )

    assert proposals
    proposal = proposals[0]
    assert isinstance(proposal, Proposal)
    assert 0.0 <= proposal.confidence <= 1.0
    assert PO_CORE in proposal.extra
    assert RATIONALE in proposal.extra[PO_CORE]
    assert CITATIONS in proposal.extra[PO_CORE]
