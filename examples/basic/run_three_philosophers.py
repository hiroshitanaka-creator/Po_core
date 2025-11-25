"""Example: run Po_self three-philosopher ensemble with tracing."""
from pathlib import Path

from po_core.po_self import PoSelfEnsemble
from po_core.po_trace import PoTraceLogger


def main() -> None:
    prompt = "Should we seek authenticity or comfort when facing uncertainty?"
    ensemble = PoSelfEnsemble()
    result = ensemble.infer(prompt)

    logger = PoTraceLogger(path=Path("examples/basic/po_trace_example.ndjson"), ndjson=True)
    logger.record_prompt(prompt)
    logger.record_tensors(result)
    logger.record_contributions(
        f"{tensor.name}: {tensor.description} -> {tensor.value}" for tensor in result.philosopher_tensors
    )
    log_path = logger.save()

    print("Prompt:", prompt)
    print("Composite tensor value:", result.composite_tensor.value if result.composite_tensor else "n/a")
    print("Tensor details:")
    for tensor in result.philosopher_tensors:
        print(f" - {tensor.name}: {tensor.value} ({tensor.description})")
    print("Trace saved to", log_path)


if __name__ == "__main__":
    main()
