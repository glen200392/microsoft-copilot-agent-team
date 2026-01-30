# Microsoft Copilot Agent Team - Project Structure

## 📁 Complete File Organization

This document describes the complete file structure for the GitHub repository.

---

## Repository Root

```
microsoft-copilot-agent-team/
│
├── README.md                          # Project overview and quick start
├── LICENSE                            # MIT License
├── CONTRIBUTING.md                    # Contribution guidelines
├── .gitignore                         # Git ignore rules
├── requirements.txt                   # Python dependencies
├── requirements-dev.txt               # Development dependencies
│
├── docs/                              # 📚 Documentation
│   ├── architecture-analysis.md       # Initial architecture analysis
│   ├── architecture-documentation.md  # Complete architecture design
│   ├── agent-team-design.md          # Detailed agent specifications
│   ├── agent-configurations.json     # Agent configuration schemas
│   ├── test-scenarios.md             # Testing guide
│   ├── deployment-guide.md           # Deployment instructions
│   ├── user-guide.md                 # End-user documentation
│   ├── developer-guide.md            # Developer documentation
│   └── knowledge-base/               # Knowledge resources
│       └── microsoft-copilot-studio-knowledge-base.md
│
├── agents/                            # 🤖 Agent Configurations
│   ├── orchestrator/
│   │   ├── config.json               # Agent metadata
│   │   └── prompt.md                 # System prompt
│   ├── architecture-specialist/
│   │   ├── config.json
│   │   └── prompt.md
│   ├── integration-specialist/
│   │   ├── config.json
│   │   └── prompt.md
│   ├── knowledge-specialist/
│   │   ├── config.json
│   │   └── prompt.md
│   ├── code-generator/
│   │   ├── config.json
│   │   └── prompt.md
│   ├── documentation-researcher/
│   │   ├── config.json
│   │   └── prompt.md
│   └── troubleshooter/
│       ├── config.json
│       └── prompt.md
│
├── scripts/                           # ⚙️ Deployment & Management
│   ├── deploy-agents.py              # Agent deployment script
│   ├── test-suite.py                 # Test execution script
│   ├── monitor-dashboard.py          # Monitoring dashboard
│   └── utils/
│       ├── agent-helpers.py          # Helper functions
│       └── config-loader.py          # Configuration utilities
│
├── tests/                             # 🧪 Test Suites
│   ├── unit/                         # Unit tests
│   │   ├── test_orchestrator.py
│   │   ├── test_architecture_specialist.py
│   │   ├── test_integration_specialist.py
│   │   └── ...
│   ├── integration/                  # Integration tests
│   │   ├── test_agent_collaboration.py
│   │   ├── test_multi_agent_workflows.py
│   │   └── ...
│   └── e2e/                          # End-to-end tests
│       ├── test_simple_queries.py
│       ├── test_complex_projects.py
│       └── ...
│
├── examples/                          # 📝 Usage Examples
│   ├── simple-query.md               # Simple query examples
│   ├── complex-project.md            # Complex project examples
│   ├── troubleshooting.md            # Troubleshooting examples
│   └── notebooks/                    # Jupyter notebooks (optional)
│       └── agent-team-demo.ipynb
│
└── .github/                           # GitHub specific
    ├── workflows/                     # CI/CD workflows
    │   ├── test.yml                  # Automated testing
    │   └── deploy.yml                # Deployment automation
    ├── ISSUE_TEMPLATE/               # Issue templates
    │   ├── bug_report.md
    │   └── feature_request.md
    └── PULL_REQUEST_TEMPLATE.md      # PR template
```

---

## 📄 File Descriptions

### Root Files

| File | Purpose |
|------|---------|
| `README.md` | Project homepage with overview, quick start, and key features |
| `LICENSE` | MIT License for open source distribution |
| `CONTRIBUTING.md` | Guidelines for contributors |
| `.gitignore` | Specifies files to exclude from version control |
| `requirements.txt` | Python package dependencies |
| `requirements-dev.txt` | Development and testing dependencies |

### Documentation (`docs/`)

| File | Purpose |
|------|---------|
| `architecture-analysis.md` | Initial analysis of agent architecture needs |
| `architecture-documentation.md` | Complete system architecture with flowcharts |
| `agent-team-design.md` | Detailed specifications for each agent |
| `agent-configurations.json` | JSON schemas for agent configuration |
| `test-scenarios.md` | Comprehensive testing scenarios and validation |
| `deployment-guide.md` | Step-by-step deployment instructions |
| `user-guide.md` | How to use the agent team effectively |
| `developer-guide.md` | How to extend and customize agents |
| `knowledge-base/` | Reference materials and documentation |

### Agent Configurations (`agents/`)

Each agent has its own directory containing:

- `config.json`: Agent metadata, toolkits, input/output schemas
- `prompt.md`: Complete system prompt in XML format

**Agent Directories:**
- `orchestrator/` - Central coordinator
- `architecture-specialist/` - Architecture and design expert
- `integration-specialist/` - API and integration expert
- `knowledge-specialist/` - RAG and knowledge management expert
- `code-generator/` - Script generation expert
- `documentation-researcher/` - Documentation search expert
- `troubleshooter/` - Problem diagnosis expert

### Scripts (`scripts/`)

| Script | Purpose |
|--------|---------|
| `deploy-agents.py` | Deploy agents in phases (Phase 1, 2, 3, or all) |
| `test-suite.py` | Run unit, integration, or end-to-end tests |
| `monitor-dashboard.py` | Real-time monitoring of agent performance |
| `utils/` | Helper functions and utilities |

### Tests (`tests/`)

| Directory | Purpose |
|-----------|---------|
| `unit/` | Test individual agent functionality |
| `integration/` | Test agent collaboration and workflows |
| `e2e/` | Test complete user scenarios end-to-end |

### Examples (`examples/`)

| File | Purpose |
|------|---------|
| `simple-query.md` | Examples of basic single-agent queries |
| `complex-project.md` | Examples of multi-agent project workflows |
| `troubleshooting.md` | Examples of debugging and problem-solving |
| `notebooks/` | Interactive Jupyter notebooks for demonstrations |

---

## 🔑 Key Configuration Files

### `agents/orchestrator/config.json`

```json
{
  "id": "microsoft-copilot-orchestrator",
  "name": "Microsoft Copilot Orchestrator",
  "layer": "L1_COORDINATOR",
  "toolkits": [
    "Agent Management",
    "Task Management",
    "File Management",
    "Web Search"
  ],
  "routing_rules": {
    "architecture": ["設計", "架構", "Topics"],
    "integration": ["API", "連接器", "Power Automate"],
    "knowledge": ["知識庫", "RAG", "SharePoint"]
  }
}
```

### `requirements.txt`

```txt
# Core dependencies
requests>=2.31.0
pydantic>=2.5.0
python-dotenv>=1.0.0

# Optional: For local testing
pytest>=7.4.0
pytest-cov>=4.1.0
```

---

## 🚀 Setup Instructions

### For Users

1. Clone the repository
2. Review `README.md` for quick start
3. Follow `docs/deployment-guide.md` to deploy agents
4. Check `examples/` for usage patterns

### For Developers

1. Clone the repository
2. Install dev dependencies: `pip install -r requirements-dev.txt`
3. Read `CONTRIBUTING.md` for contribution guidelines
4. Review `docs/developer-guide.md` for architecture details
5. Run tests: `python scripts/test-suite.py --all`

### For Contributors

1. Fork the repository
2. Create feature branch
3. Follow coding standards in `CONTRIBUTING.md`
4. Add tests for new features
5. Update documentation
6. Submit pull request

---

## 📦 Deployment Artifacts

When deployed, the system creates:

```
deployment/
├── agent-registry.json        # Deployed agent metadata
├── deployment-log.txt         # Deployment history
└── monitoring/
    ├── performance-metrics.json
    └── error-logs/
```

---

## 🔄 Version Control Strategy

### Branches

- `main` - Stable production-ready code
- `develop` - Integration branch for features
- `feature/*` - Individual feature branches
- `fix/*` - Bug fix branches
- `release/*` - Release preparation branches

### Tags

- `v1.0.0` - Major releases
- `v1.1.0` - Minor releases
- `v1.0.1` - Patch releases

---

## 📊 File Statistics

| Category | Count | Total Size |
|----------|-------|------------|
| Documentation | 10 files | ~150 KB |
| Agent Configs | 14 files | ~50 KB |
| Scripts | 4 files | ~20 KB |
| Tests | 12+ files | ~40 KB |
| Examples | 4+ files | ~15 KB |

**Total Project Size:** ~275 KB (documentation and configuration)

---

## 🔍 Finding Files

### Quick Reference

**Need to...**
- Understand architecture? → `docs/architecture-documentation.md`
- Deploy agents? → `scripts/deploy-agents.py` + `docs/deployment-guide.md`
- Add new agent? → Follow structure in `agents/*/`
- Write tests? → `tests/` + `docs/test-scenarios.md`
- Contribute? → `CONTRIBUTING.md`
- Use the system? → `README.md` + `examples/`

---

## 🛠️ Maintenance

### Regular Updates

- **Monthly**: Review and update `knowledge-base/`
- **Quarterly**: Update dependencies in `requirements.txt`
- **Per Release**: Update `CHANGELOG.md` and version numbers
- **As Needed**: Update agent prompts based on Microsoft docs changes

### Deprecation Policy

- Deprecated files moved to `deprecated/` folder
- Kept for one major version before removal
- Migration guides provided in `docs/migrations/`

---

**Last Updated:** 2026-01-30  
**Structure Version:** 1.0.0
