.PHONY: paper-experiments paper-benchmark paper-pdf paper-build x-assets x-pack x-pack-all x-metrics-init

paper-experiments:
	python scripts/paper/generate_experiment_snapshot.py

paper-benchmark:
	python scripts/paper/run_comparative_benchmark.py

paper-pdf:
	python scripts/paper/build_paper_pdf.py

paper-build: paper-experiments paper-benchmark paper-pdf

x-assets:
	python tools/demo_shopping.py
	python tools/generate_badge.py runs/high_bias_affiliate.badge.json --out runs/high_bias_affiliate.badge.svg
	python tools/generate_badge.py runs/mixed_contaminated.badge.json --out runs/mixed_contaminated.badge.svg
	python tools/generate_badge.py runs/clean_multi_merchant.badge.json --out runs/clean_multi_merchant.badge.svg
	python assets/flying_pig_anim.py

x-pack:
	@if [ -z "$(CASE)" ]; then echo "CASE is required. e.g. make x-pack CASE=high_bias_affiliate"; exit 1; fi
	python tools/build_x_pack.py --case $(CASE) --repo-url https://github.com/hiroshitanaka-creator/project-echo --out-dir dist/x

x-pack-all:
	python tools/build_x_pack.py --all --repo-url https://github.com/hiroshitanaka-creator/project-echo --out-dir dist/x

x-metrics-init:
	@mkdir -p ops
	@if [ ! -f ops/x_metrics.csv ]; then \
		echo "date,case,angle,post_url,impressions,engagements,bookmarks,profile_visits,link_clicks,github_stars_before,github_stars_after" > ops/x_metrics.csv; \
		echo "initialized ops/x_metrics.csv"; \
	else \
		echo "ops/x_metrics.csv already exists"; \
	fi
