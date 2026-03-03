.PHONY: paper-experiments paper-pdf paper-build

paper-experiments:
	python scripts/paper/generate_experiment_snapshot.py

paper-pdf:
	python scripts/paper/build_paper_pdf.py

paper-build: paper-experiments paper-pdf
