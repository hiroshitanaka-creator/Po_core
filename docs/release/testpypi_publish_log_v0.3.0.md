# TestPyPI Publish Evidence for v0.3.0

- Purpose: Record immutable release evidence for `po-core-flyingpig==0.3.0` TestPyPI publication and smoke verification.
- Execution time (UTC): 2026-03-08T04:04:43Z
- Commit SHA (HEAD at evidence update): `fa10c08`
- Release tag: `v0.3.0`
- Workflow run URL (TestPyPI publish): `unavailable from this offline/proxied execution environment (GitHub CONNECT tunnel returned 403)`

## Commands and observed results

1. Install from TestPyPI
   - Command:
     `python -m pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple po-core-flyingpig==0.3.0`
   - Observed result:
     `ERROR: No matching distribution found for po-core-flyingpig==0.3.0`
   - Execution context note:
     The environment cannot reach GitHub/TestPyPI endpoints through the configured proxy (`Tunnel connection failed: 403 Forbidden`), so online smoke verification could not be executed in this run.

2. Version import smoke
   - Command:
     `python -c "import po_core; print(po_core.__version__)"`
   - Observed result:
     `0.3.0`

3. Optional run smoke
   - Command:
     `python -c "from po_core import run; out = run('smoke'); print(out.get('status'))"`
   - Observed result:
     `ok`

## Result summary

- Local import smoke confirms `po_core.__version__ == 0.3.0`.
- Local runtime smoke confirms `run('smoke')` returns status `ok`.
- Network-restricted environment prevented direct TestPyPI install verification and workflow URL retrieval; those must be recorded from a network-enabled CI/GitHub runner to complete online publication evidence.
