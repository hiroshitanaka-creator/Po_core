.PHONY: paper-experiments paper-benchmark paper-pdf paper-build

paper-experiments:
	python scripts/paper/generate_experiment_snapshot.py

paper-benchmark:
	python scripts/paper/run_comparative_benchmark.py

paper-pdf:
	python scripts/paper/build_paper_pdf.py

paper-build: paper-experiments paper-benchmark paper-pdf
