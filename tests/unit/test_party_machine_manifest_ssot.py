from po_core.party_machine import (
    HARMONIOUS_CLUSTERS,
    HIGH_TENSION_PAIRS,
    OPTIMAL_4_COMBOS,
    PhilosopherPartyMachine,
)
from po_core.philosophers.manifest import get_public_philosopher_specs


def _canonical_ids() -> set[str]:
    return {spec.philosopher_id for spec in get_public_philosopher_specs()}


def test_party_machine_available_philosophers_match_manifest() -> None:
    machine = PhilosopherPartyMachine(verbose=False)
    assert set(machine.available_philosophers) == _canonical_ids()


def test_party_machine_static_roster_data_only_references_manifest_ids() -> None:
    canonical = _canonical_ids()

    combo_ids = {
        philosopher_id
        for combos in OPTIMAL_4_COMBOS.values()
        for combo in combos
        for philosopher_id in combo
    }
    tension_ids = {pid for pair in HIGH_TENSION_PAIRS for pid in pair}
    cluster_ids = {
        philosopher_id
        for cluster in HARMONIOUS_CLUSTERS.values()
        for philosopher_id in cluster
    }

    all_ids = combo_ids | tension_ids | cluster_ids
    assert all_ids <= canonical
