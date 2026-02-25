# Po_core Repository Structure

## Purpose

This document defines the complete repository structure for Po_core's GitHub publication. It serves as a blueprint for organizing code, documentation, and resources.

---

## Repository Root Structure

```
Po_core/
├── .github/                    # GitHub specific files
│   ├── workflows/             # CI/CD workflows
│   ├── ISSUE_TEMPLATE/        # Issue templates
│   └── PULL_REQUEST_TEMPLATE.md
│
├── docs/                       # Documentation
│   ├── design/                # Design documents
│   ├── philosophy/            # Philosophical foundations
│   ├── api/                   # API documentation
│   ├── tutorials/             # Tutorials and guides
│   └── images/                # Documentation images
│
├── src/                        # Source code
│   └── po_core/               # Main package
│       ├── __init__.py
│       ├── core/              # Core system
│       ├── po_self/           # Philosophical ensemble
│       ├── po_trace/          # Audit logging
│       └── po_viewer/         # Visualization
│
├── tests/                      # Test suite
│   ├── unit/                  # Unit tests
│   ├── integration/           # Integration tests
│   ├── philosophical/         # Philosophical consistency tests
│   └── fixtures/              # Test fixtures
│
├── examples/                   # Example code and demos
│   ├── basic/                 # Basic usage examples
│   ├── advanced/              # Advanced examples
│   └── notebooks/             # Jupyter notebooks
│
├── scripts/                    # Utility scripts
│   ├── setup/                 # Setup scripts
│   ├── analysis/              # Analysis tools
│   └── deployment/            # Deployment scripts
│
├── config/                     # Configuration files
│   ├── philosophers/          # Philosopher configurations
│   └── default.yaml           # Default configuration
│
├── .gitignore                  # Git ignore rules
├── .gitattributes             # Git attributes
├── README.md                   # Project overview
├── CONTRIBUTING.md             # Contribution guidelines
├── CODE_OF_CONDUCT.md          # Code of conduct
├── LICENSE                     # GNU AGPLv3 License
├── MANIFESTO.md                # Project manifesto
├── CHANGELOG.md                # Version history
├── requirements.txt            # Python dependencies
├── requirements-dev.txt        # Development dependencies
├── setup.py                    # Package setup
├── pyproject.toml             # Modern Python packaging
└── Makefile                    # Common tasks automation
```

---

## Detailed Directory Descriptions

### `.github/` - GitHub Configuration

```
.github/
├── workflows/
│   ├── ci.yml                 # Continuous Integration
│   ├── tests.yml              # Automated testing
│   ├── docs.yml               # Documentation deployment
│   └── release.yml            # Release automation
│
├── ISSUE_TEMPLATE/
│   ├── bug_report.md
│   ├── feature_request.md
│   ├── philosophical_question.md
│   └── config.yml
│
├── PULL_REQUEST_TEMPLATE.md
└── FUNDING.yml                # Optional: funding information
```

**Purpose:** GitHub-specific automation and templates

### `docs/` - Documentation

```
docs/
├── design/
│   ├── architecture/
│   │   ├── overview.md
│   │   ├── po_core_architecture.md
│   │   ├── po_self_architecture.md
│   │   ├── po_trace_architecture.md
│   │   └── po_viewer_architecture.md
│   │
│   ├── philosophers/
│   │   ├── sartre.md          # Each philosopher's design
│   │   ├── jung.md
│   │   ├── derrida.md
│   │   ├── heidegger.md
│   │   ├── watsuji.md
│   │   ├── spinoza.md
│   │   ├── arendt.md
│   │   ├── wittgenstein.md
│   │   ├── peirce.md
│   │   ├── aristotle.md
│   │   └── new_philosopher_template.md
│   │
│   ├── tensors/
│   │   ├── freedom_pressure.md
│   │   ├── shadow_integration.md
│   │   ├── trace_rejection.md
│   │   └── tensor_interactions.md
│   │
│   └── api/
│       ├── core_api.md
│       ├── po_self_api.md
│       ├── po_trace_api.md
│       └── po_viewer_api.md
│
├── philosophy/
│   ├── foundations.md         # Philosophical foundations
│   ├── responsibility.md      # Responsibility theory
│   ├── meaning_generation.md  # Meaning generation
│   ├── ethical_framework.md   # Ethical considerations
│   └── flying_pig_philosophy.md
│
├── tutorials/
│   ├── quickstart.md
│   ├── basic_usage.md
│   ├── philosopher_integration.md
│   ├── creating_custom_philosophers.md
│   └── visualization_guide.md
│
├── api/
│   ├── reference/
│   │   ├── core.md
│   │   ├── po_self.md
│   │   ├── po_trace.md
│   │   └── po_viewer.md
│   └── generated/             # Auto-generated API docs
│
└── images/
    ├── architecture/
    ├── diagrams/
    └── examples/
```

**Purpose:** Comprehensive project documentation

**Note:** Selected design documents from Google Drive (120+ documents) will be curated and organized here. Not all documents need to be in the initial release.

### `src/po_core/` - Source Code

```
src/po_core/
├── __init__.py
├── __version__.py
├── config.py                   # Configuration management
├── exceptions.py               # Custom exceptions
│
├── core/
│   ├── __init__.py
│   ├── base.py                # Base classes
│   ├── tensor_manager.py      # Tensor operations
│   ├── meaning_generator.py   # Core meaning generation
│   └── response_composer.py   # Response composition
│
├── po_self/
│   ├── __init__.py
│   ├── po_self.py             # Main Po_self class
│   ├── philosophers/
│   │   ├── __init__.py
│   │   ├── base_philosopher.py
│   │   ├── sartre.py          # Freedom pressure
│   │   ├── jung.py            # Shadow integration
│   │   ├── derrida.py         # Trace/rejection
│   │   ├── heidegger.py       # Dasein/present absence
│   │   ├── watsuji.py         # Aidagara
│   │   ├── spinoza.py         # Conatus
│   │   ├── arendt.py          # Public stage
│   │   ├── wittgenstein.py    # Language games
│   │   ├── peirce.py          # Semiotic delta
│   │   └── aristotle.py       # Phronesis
│   │
│   ├── tensors/
│   │   ├── __init__.py
│   │   ├── freedom_pressure.py
│   │   ├── shadow_tensor.py
│   │   ├── trace_tensor.py
│   │   └── interaction_matrix.py
│   │
│   └── ensemble.py            # Philosopher ensemble logic
│
├── po_trace/
│   ├── __init__.py
│   ├── tracer.py              # Main tracing logic
│   ├── event_logger.py        # Event logging
│   ├── rejection_log.py       # Rejection tracking
│   ├── evolution_tracker.py   # Evolution history
│   ├── metadata.py            # Event metadata
│   └── storage/
│       ├── __init__.py
│       ├── base_storage.py
│       ├── json_storage.py
│       └── database_storage.py
│
├── po_viewer/
│   ├── __init__.py
│   ├── viewer.py              # Main viewer class
│   ├── renderers/
│   │   ├── __init__.py
│   │   ├── tensor_renderer.py
│   │   ├── graph_renderer.py
│   │   └── timeline_renderer.py
│   │
│   └── exporters/
│       ├── __init__.py
│       ├── json_exporter.py
│       ├── html_exporter.py
│       └── image_exporter.py
│
└── utils/
    ├── __init__.py
    ├── math_utils.py
    ├── text_utils.py
    └── validation.py
```

**Purpose:** Production code organized by component

**Current Status:** Framework exists in design docs; implementation at ~30%

### `tests/` - Test Suite

```
tests/
├── __init__.py
├── conftest.py                # Pytest configuration
│
├── unit/
│   ├── core/
│   ├── po_self/
│   ├── po_trace/
│   └── po_viewer/
│
├── integration/
│   ├── test_end_to_end.py
│   ├── test_philosopher_interactions.py
│   └── test_trace_viewer_integration.py
│
├── philosophical/
│   ├── test_sartre_consistency.py
│   ├── test_derrida_consistency.py
│   └── test_philosophical_axioms.py
│
└── fixtures/
    ├── sample_inputs.json
    ├── expected_outputs.json
    └── test_configurations.yaml
```

**Purpose:** Comprehensive testing across all levels

### `examples/` - Example Code

```
examples/
├── README.md
│
├── basic/
│   ├── hello_po_core.py       # Simplest example
│   ├── three_philosopher_bot.py
│   └── basic_tracing.py
│
├── advanced/
│   ├── custom_philosopher.py
│   ├── tensor_visualization.py
│   ├── evolution_analysis.py
│   └── multi_agent_debate.py
│
└── notebooks/
    ├── quickstart.ipynb
    ├── philosopher_exploration.ipynb
    └── trace_analysis.ipynb
```

**Purpose:** Demonstrate usage patterns

### `scripts/` - Utility Scripts

```
scripts/
├── setup/
│   ├── install_dependencies.sh
│   ├── setup_dev_environment.sh
│   └── verify_installation.py
│
├── analysis/
│   ├── analyze_traces.py
│   ├── tensor_statistics.py
│   └── philosophical_metrics.py
│
└── deployment/
    ├── build_package.sh
    └── deploy_docs.sh
```

**Purpose:** Automation and utilities

### `config/` - Configuration

```
config/
├── philosophers/
│   ├── sartre.yaml
│   ├── jung.yaml
│   └── ... (one per philosopher)
│
├── default.yaml               # Default system config
└── example.yaml               # Example custom config
```

**Purpose:** Runtime configuration

---

## Files in Repository Root

### Core Documentation Files

| File | Purpose | Status |
|------|---------|--------|
| `README.md` | Project overview, quickstart | ✅ Complete |
| `CONTRIBUTING.md` | Contribution guidelines | ✅ Complete |
| `CODE_OF_CONDUCT.md` | Community standards | ✅ Complete |
| `LICENSE` | GNU AGPLv3 License | ✅ Complete |
| `MANIFESTO.md` | Flying Pig Philosophy | ✅ Complete |
| `CHANGELOG.md` | Version history | 🔄 To Create |

### Python Packaging Files

| File | Purpose | Status |
|------|---------|--------|
| `requirements.txt` | Production dependencies | 🔄 To Create |
| `requirements-dev.txt` | Development dependencies | 🔄 To Create |
| `setup.py` | Legacy package setup | 🔄 To Create |
| `pyproject.toml` | Modern Python packaging | 🔄 To Create |

### Configuration Files

| File | Purpose | Status |
|------|---------|--------|
| `.gitignore` | Ignored files | ✅ Complete |
| `.gitattributes` | Git file handling | 🔄 To Create |
| `Makefile` | Common tasks | 🔄 To Create |

---

## Initial Release Strategy

### Phase 1: Foundation (Week 1)

**Goal:** Establish project presence

**Include:**

- ✅ README.md
- ✅ CONTRIBUTING.md
- ✅ CODE_OF_CONDUCT.md
- ✅ LICENSE
- ✅ MANIFESTO.md
- ✅ .gitignore
- 🔄 Basic directory structure
- 🔄 Selected design documents (10-15 key documents)

**Exclude (for now):**

- Full implementation code (in progress)
- All 120+ design documents (too overwhelming)
- Complete test suite (being developed)

### Phase 2: Core Implementation (Weeks 2-4)

**Goal:** Demonstrate functional prototype

**Add:**

- Core tensor system
- 3-philosopher bot (Sartre, Jung, Derrida)
- Basic Po_trace logging
- Simple examples
- Unit tests

### Phase 3: Expansion (Months 2-3)

**Goal:** Build toward full vision

**Add:**

- Remaining philosophers (gradual integration)
- Po_core Viewer
- Integration tests
- Advanced examples
- Comprehensive documentation

---

## What Goes Where?

### GitHub Repository

**Should include:**

- Core code and architecture
- Essential design documents
- API documentation
- Examples and tutorials
- Test suite
- Contribution infrastructure

**Should NOT include:**

- Personal research notes
- Draft documents (keep in Google Drive)
- Large binary files (models, datasets)
- Temporary experimental code
- 120+ raw design documents (curate first)

### Google Drive

**Should keep:**

- Complete archive of all 120+ design documents
- Draft documents and work-in-progress
- Large PDFs and papers
- Personal research notes
- Experimental analyses
- Meeting notes and planning documents

### Strategy

1. **Curate** key design documents for GitHub
2. **Keep** comprehensive archive in Google Drive
3. **Link** from GitHub docs to Google Drive for deeper materials
4. **Gradually migrate** polished documents to GitHub over time

---

## Naming Conventions

### Files

- **Python files:** `snake_case.py`
- **Markdown files:** `lowercase-with-dashes.md` or `CamelCase.md` for major docs
- **Config files:** `lowercase.yaml`, `lowercase.json`
- **Test files:** `test_feature_name.py`

### Directories

- **Python packages:** `snake_case/`
- **Documentation:** `lowercase/` or `CamelCase/` for major sections
- **General:** `lowercase-with-dashes/`

### Classes & Functions

```python
# Classes: PascalCase
class FreedomPressureTensor:
    pass

# Functions: snake_case
def calculate_semantic_delta():
    pass

# Constants: UPPER_SNAKE_CASE
MAX_PHILOSOPHERS = 21
```

---

## GitHub-Specific Features

### Topics (Tags)

Suggested topics for GitHub repository:

- `artificial-intelligence`
- `philosophy`
- `ethics`
- `pytorch`
- `tensors`
- `explainable-ai`
- `responsible-ai`
- `sartre`
- `phenomenology`
- `existentialism`

### About Section

```
AI system integrating 10+ philosophers as dynamic tensors for
responsible meaning generation. Built on the Flying Pig Philosophy.
```

### Website

Link to documentation: `https://[username].github.io/Po_core/` (future)

---

## Migration Plan from Google Drive

### Step 1: Curate Design Documents

From 120+ documents, select ~15-20 essential ones:

- Po_core specification v1.0
- Po_self architecture
- Po_trace design
- Po_core Viewer design
- Key philosopher implementations
- Tensor interaction matrix

### Step 2: Convert Format

- Ensure markdown format
- Add proper headers and structure
- Include images/diagrams where needed
- Update links to work in GitHub

### Step 3: Organize by Category

Place documents in appropriate directories:

- Architecture → `docs/design/architecture/`
- Philosophers → `docs/design/philosophers/`
- API specs → `docs/design/api/`

### Step 4: Create Index

Create navigation documents:

- `docs/design/README.md` — Design document index
- `docs/philosophy/README.md` — Philosophy document index
- `docs/api/README.md` — API documentation index

---

## Next Steps

### Immediate (Today)

1. ✅ Create CODE_OF_CONDUCT.md
2. ✅ Create .gitignore
3. ✅ Create this structure document
4. 🔄 Create basic directory structure
5. 🔄 Create placeholder files

### This Week

1. Create packaging files (requirements.txt, setup.py, pyproject.toml)
2. Create CHANGELOG.md
3. Curate and migrate 15-20 key design documents
4. Set up basic directory structure with placeholder files
5. Create initial examples/

### Next Week

1. Initialize GitHub repository
2. Push initial structure
3. Set up GitHub Actions for CI
4. Create issue templates
5. Invite first collaborators

---

## Questions & Decisions Needed

### Decision Points

1. **Repository Name**
   - Current: `Po_core`
   - Alternative: `po-core`, `PoCore`, `po_core`
   - **Recommendation:** `Po_core` (matches documentation)

2. **Organization vs Personal**
   - Personal account: `[username]/Po_core`
   - Organization: `FlyingPigAI/Po_core`
   - **Recommendation:** Start personal, migrate to org later if needed

3. **Initial Version**
   - Start at v0.1.0 (pre-alpha)
   - **Recommendation:** v0.1.0-alpha

4. **Documentation Hosting**
   - GitHub Pages
   - Read the Docs
   - **Recommendation:** GitHub Pages initially

---

## Success Metrics

### For Initial Release

- [ ] All foundation files present (README, CONTRIBUTING, etc.)
- [ ] Basic directory structure established
- [ ] 10-15 key design documents migrated
- [ ] Clear contribution pathways established
- [ ] First 3-5 GitHub stars ⭐

### For v0.2.0

- [ ] Working 3-philosopher prototype
- [ ] 20+ unit tests
- [ ] Basic examples functional
- [ ] 5-10 design documents added
- [ ] First external contributor

---

*This document reflects the Flying Pig Philosophy: we plan boldly, build iteratively, and adjust gracefully based on what we learn.*

**Document Status:** Draft v1.0
**Last Updated:** 2025-11-02
**Next Review:** After initial GitHub publication
