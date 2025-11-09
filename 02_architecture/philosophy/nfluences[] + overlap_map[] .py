# -*- coding: utf-8 -*-
"""
Philosophical influence structure for Po-like semantic/tensor analysis.

- `influences`: how each philosopher's idea is mapped to a concrete tensor/field
- `overlap_map`: how multiple philosophers form intersecting or divergent tensor zones
"""

data = {'influences': [{'philosopher': 'Sartre', 'conceptual_label': '自由＝責任圧', 'target_field': 'freedom_pressure_tensor', 'influence_type': 'scalar', 'viewer_resonance_level': 0.76}, {'philosopher': 'Jung', 'conceptual_label': '元型の沈黙', 'target_field': 'semantic_collapse_chain', 'influence_type': 'latent_trace', 'viewer_resonance_level': 0.63}, {'philosopher': 'Derrida', 'conceptual_label': '非語りの痕跡', 'target_field': 'Po_trace.rejection_log[]', 'influence_type': 'trace', 'viewer_resonance_level': 0.91}, {'philosopher': 'Heidegger', 'conceptual_label': '開示性と投企', 'target_field': 'jump_chain_trace.intent_structure', 'influence_type': 'trace_vector', 'viewer_resonance_level': 0.68}], 'overlap_map': [{'intersection_type': 'reinforced', 'tensor_overlap_zone': 'freedom_pressure_tensor ∩ persona_arc_intensity', 'associated_philosophers': ['Sartre', 'Jung'], 'trace_cluster_impact': 'jump_profile_tag = existential_rebirth'}, {'intersection_type': 'divergent', 'tensor_overlap_zone': 'Po_trace.rejection_log[] ∩ expression_arc_intensity', 'associated_philosophers': ['Derrida', 'Merleau-Ponty'], 'trace_cluster_impact': 'semantic_fluctuation = unstable_pulse'}]}


def get_influences():
    """Return the list of philosopher-to-tensor influence mappings."""
    return data["influences"]


def get_overlap_map():
    """Return definitions of tensor overlap and their semantic impacts."""
    return data["overlap_map"]


if __name__ == "__main__":
    from pprint import pprint

    print("Influences:")
    pprint(get_influences())
    print("\nOverlap map:")
    pprint(get_overlap_map())
