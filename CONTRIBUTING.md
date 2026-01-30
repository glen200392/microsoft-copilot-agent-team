# Contributing to Microsoft Copilot Agent Team

Thank you for your interest in contributing! This document provides guidelines for contributing to the project.

---

## 📋 Table of Contents

- [Code of Conduct](#code-of-conduct)
- [How Can I Contribute?](#how-can-i-contribute)
- [Development Setup](#development-setup)
- [Contribution Workflow](#contribution-workflow)
- [Coding Standards](#coding-standards)
- [Testing Guidelines](#testing-guidelines)
- [Documentation](#documentation)
- [Community](#community)

---

## 📜 Code of Conduct

This project adheres to a Code of Conduct that all contributors are expected to follow. By participating, you agree to:

- Use welcoming and inclusive language
- Respect differing viewpoints and experiences
- Accept constructive criticism gracefully
- Focus on what is best for the community
- Show empathy towards other community members

---

## 🤝 How Can I Contribute?

### Reporting Bugs

Before creating a bug report, please check existing issues to avoid duplicates.

**When reporting a bug, include:**
- Clear, descriptive title
- Steps to reproduce the issue
- Expected behavior vs actual behavior
- Agent logs (if available)
- Environment details (OS, Python version, etc.)
- Screenshots or error messages

**Use this template:**
```markdown
**Bug Description**
A clear description of what the bug is.

**To Reproduce**
1. Go to '...'
2. Run command '...'
3. See error

**Expected Behavior**
What you expected to happen.

**Actual Behavior**
What actually happened.

**Environment**
- OS: [e.g., Windows 11, macOS 14]
- Python Version: [e.g., 3.11]
- Agent Version: [e.g., 1.0.0]

**Additional Context**
Any other relevant information.
```

### Suggesting Enhancements

We welcome feature requests! Please provide:
- Clear use case description
- Expected benefits
- Suggested implementation approach (if you have one)
- Examples from similar projects (optional)

### Contributing Code

We accept contributions in these areas:

1. **New Specialist Agents**
   - Security & Compliance Specialist
   - Performance Optimization Specialist
   - Deployment Specialist
   - Custom domain-specific specialists

2. **Core Improvements**
   - Orchestrator routing logic enhancements
   - Performance optimizations
   - Error handling improvements
   - New tool integrations

3. **Testing**
   - Additional test scenarios
   - Integration test coverage
   - Performance benchmarks

4. **Documentation**
   - Tutorial improvements
   - API documentation
   - Use case examples
   - Translation to other languages

---

## 🛠️ Development Setup

### Prerequisites

```bash
# Required
Python 3.10 or higher
Git

# Optional
Microsoft 365 account (for testing integrations)
Azure subscription (for production deployments)
```

### Clone and Setup

```bash
# Clone the repository
git clone https://github.com/yourusername/microsoft-copilot-agent-team.git
cd microsoft-copilot-agent-team

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install development dependencies
pip install -r requirements-dev.txt
```

### Project Structure

```
microsoft-copilot-agent-team/
├── agents/              # Agent configurations
│   ├── orchestrator/
│   ├── architecture-specialist/
│   └── ...
├── docs/               # Documentation
├── scripts/            # Deployment and utility scripts
├── tests/              # Test suites
└── examples/           # Usage examples
```

---

## 🔄 Contribution Workflow

### 1. Fork and Branch

```bash
# Fork the repository on GitHub, then:
git clone https://github.com/YOUR-USERNAME/microsoft-copilot-agent-team.git
cd microsoft-copilot-agent-team

# Create a feature branch
git checkout -b feature/your-feature-name
# Or for bug fixes:
git checkout -b fix/bug-description
```

### 2. Make Changes

- Write clear, concise code
- Follow existing code style
- Add tests for new functionality
- Update documentation as needed

### 3. Test Your Changes

```bash
# Run unit tests
python scripts/test-suite.py --level 1

# Run integration tests
python scripts/test-suite.py --level 2

# Run all tests
python scripts/test-suite.py --all
```

### 4. Commit

```bash
# Stage your changes
git add .

# Commit with descriptive message
git commit -m "feat: add Security Specialist agent"
# Or for fixes:
git commit -m "fix: resolve orchestrator timeout issue"
```

**Commit Message Format:**
```
<type>: <short description>

<optional longer description>

<optional footer>
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `test`: Adding or updating tests
- `refactor`: Code refactoring
- `perf`: Performance improvements
- `chore`: Maintenance tasks

### 5. Push and Create PR

```bash
# Push to your fork
git push origin feature/your-feature-name

# Go to GitHub and create a Pull Request
```

**PR Template:**
```markdown
## Description
Brief description of your changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Performance improvement

## Testing
- [ ] Unit tests pass
- [ ] Integration tests pass
- [ ] Manual testing completed

## Checklist
- [ ] Code follows project style guidelines
- [ ] Documentation updated
- [ ] Tests added/updated
- [ ] No breaking changes (or documented)
```

---

## 💻 Coding Standards

### Python Style

Follow [PEP 8](https://pep8.org/) with these specifics:

```python
# Good
def create_agent(name: str, config: dict) -> Agent:
    """
    Create a new agent instance.
    
    Args:
        name: Agent name
        config: Configuration dictionary
        
    Returns:
        Configured Agent instance
    """
    agent = Agent(name)
    agent.configure(config)
    return agent

# Avoid
def createagent(n, c):
    a = Agent(n)
    a.configure(c)
    return a
```

### Agent Prompt Standards

```xml
<!-- Use structured XML format for prompts -->
<identity>
Clear, concise agent identity
</identity>

<purpose>
What the agent does and why
</purpose>

<capabilities>
• Bullet point list
• Of specific capabilities
</capabilities>

<workflow>
Step-by-step process description
</workflow>
```

### Configuration Files

```json
{
  "id": "agent-id",
  "name": "Human Readable Name",
  "description": "Clear description",
  "toolkits": ["Toolkit1", "Toolkit2"],
  "input_schema": {
    "type": "object",
    "properties": {}
  }
}
```

---

## 🧪 Testing Guidelines

### Writing Tests

```python
import pytest
from agents import Orchestrator

def test_orchestrator_routing_architecture():
    """Test that architecture queries route to Architecture Specialist."""
    orchestrator = Orchestrator()
    query = "How do I design a conversation flow?"
    
    result = orchestrator.analyze_request(query)
    
    assert result.target_agent == "architecture-specialist"
    assert result.confidence > 0.9

def test_multi_agent_collaboration():
    """Test complex scenario with multiple agents."""
    orchestrator = Orchestrator()
    query = "Build an HR agent with SharePoint and Teams"
    
    result = orchestrator.process(query)
    
    assert "architecture-specialist" in result.agents_used
    assert "knowledge-specialist" in result.agents_used
    assert "integration-specialist" in result.agents_used
    assert result.success == True
```

### Test Coverage

- Aim for 80%+ code coverage
- Cover happy paths and edge cases
- Include integration tests for agent collaboration
- Add performance tests for critical paths

### Running Tests

```bash
# Run specific test file
pytest tests/unit/test_orchestrator.py

# Run with coverage
pytest --cov=agents tests/

# Run specific test
pytest tests/unit/test_orchestrator.py::test_routing
```

---

## 📚 Documentation

### Documentation Requirements

When adding new features:

1. **Update README.md** if it affects usage
2. **Add inline documentation** (docstrings, comments)
3. **Update architecture docs** if design changes
4. **Add examples** for new capabilities
5. **Update CHANGELOG.md**

### Documentation Style

```python
def process_request(request: str, context: dict = None) -> Response:
    """
    Process a user request through the agent team.
    
    This function analyzes the request, routes to appropriate specialists,
    and integrates their outputs into a cohesive response.
    
    Args:
        request: User's natural language request
        context: Optional context dictionary with previous conversation
                history or user preferences
                
    Returns:
        Response object containing:
        - answer: Integrated response text
        - agents_used: List of agents that contributed
        - files_created: Any files generated
        - references: Source citations
        
    Raises:
        ValueError: If request is empty or malformed
        TimeoutError: If processing exceeds timeout limit
        
    Example:
        >>> response = process_request(
        ...     "Design a customer support agent",
        ...     context={"complexity": "simple"}
        ... )
        >>> print(response.answer)
    """
```

---

## 👥 Community

### Getting Help

- **Documentation**: Check the [docs/](../docs/) folder first
- **Discussions**: Use [GitHub Discussions](https://github.com/yourusername/microsoft-copilot-agent-team/discussions)
- **Issues**: Search existing [issues](https://github.com/yourusername/microsoft-copilot-agent-team/issues)
- **Chat**: Join our community chat (link TBD)

### Asking Questions

Good questions include:
- What you're trying to accomplish
- What you've already tried
- Relevant code snippets or logs
- Your environment details

### Recognition

Contributors will be recognized in:
- README.md acknowledgments
- Release notes
- Project website (when available)

---

## 📝 License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

## 🙏 Thank You!

Every contribution helps make this project better. Whether it's:
- Reporting a bug
- Suggesting a feature
- Fixing a typo
- Adding a test
- Improving documentation

Your effort is appreciated! 🎉

---

**Questions?** Open an issue or start a discussion. We're here to help!

*Last Updated: 2026-01-30*
