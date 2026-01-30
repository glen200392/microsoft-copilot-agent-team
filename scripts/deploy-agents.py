#!/usr/bin/env python3
"""
Microsoft Copilot Agent Team - Deployment Script

This script deploys the agent team in phases:
- Phase 1: Core Triangle (Orchestrator, Architecture, Integration)
- Phase 2: Expanded (Knowledge, Code Generator)
- Phase 3: Full Team (Documentation Researcher, Troubleshooter)

Usage:
    python deploy-agents.py --phase 1
    python deploy-agents.py --phase 2
    python deploy-agents.py --phase 3
    python deploy-agents.py --all
"""

import argparse
import json
import sys
from pathlib import Path
from typing import List, Dict

# Agent configuration data
AGENT_CONFIGS = {
    "phase1": [
        {
            "id": "microsoft-copilot-orchestrator",
            "name": "Microsoft Copilot Orchestrator",
            "description": "Central coordinator for task routing and integration",
            "toolkits": ["Agent Management", "Task Management", "File Management", "Web Search"],
            "prompt_file": "agents/orchestrator/prompt.md"
        },
        {
            "id": "microsoft-architecture-specialist",
            "name": "Microsoft Architecture Specialist",
            "description": "Expert in Copilot Studio architecture and conversation design",
            "toolkits": ["Web Search & Scrape", "File Management"],
            "prompt_file": "agents/architecture-specialist/prompt.md"
        },
        {
            "id": "microsoft-integration-specialist",
            "name": "Microsoft Integration Specialist",
            "description": "Expert in API integration and Power Platform connectors",
            "toolkits": ["Web Search & Scrape", "Python Execution", "File Management"],
            "prompt_file": "agents/integration-specialist/prompt.md"
        }
    ],
    "phase2": [
        {
            "id": "microsoft-knowledge-specialist",
            "name": "Microsoft Knowledge Specialist",
            "description": "Expert in RAG design and knowledge management",
            "toolkits": ["Web Search & Scrape", "Python Execution", "File Management"],
            "prompt_file": "agents/knowledge-specialist/prompt.md"
        },
        {
            "id": "microsoft-code-generator",
            "name": "Microsoft Code Generator",
            "description": "Expert in generating scripts and automation code",
            "toolkits": ["Python Execution", "File Management"],
            "prompt_file": "agents/code-generator/prompt.md"
        }
    ],
    "phase3": [
        {
            "id": "microsoft-documentation-researcher",
            "name": "Microsoft Documentation Researcher",
            "description": "Expert in finding and synthesizing official documentation",
            "toolkits": ["Web Search & Scrape", "File Management"],
            "prompt_file": "agents/documentation-researcher/prompt.md"
        },
        {
            "id": "microsoft-troubleshooter",
            "name": "Microsoft Troubleshooter",
            "description": "Expert in diagnosing and resolving issues",
            "toolkits": ["Web Search", "Python Execution", "File Management"],
            "prompt_file": "agents/troubleshooter/prompt.md"
        }
    ]
}


def print_banner():
    """Print deployment banner."""
    print("=" * 60)
    print("  Microsoft Copilot Agent Team - Deployment Script")
    print("=" * 60)
    print()


def validate_environment():
    """Validate deployment environment."""
    print("🔍 Validating environment...")
    
    # Check if running in correct directory
    if not Path("docs").exists():
        print("❌ Error: Must run from project root directory")
        return False
    
    # Check for required configuration files
    config_file = Path("docs/agent-configurations.json")
    if not config_file.exists():
        print("❌ Error: agent-configurations.json not found")
        return False
    
    print("✅ Environment validation passed")
    return True


def load_agent_prompt(prompt_file: str) -> str:
    """Load agent prompt from file."""
    # In a real deployment, this would load from actual prompt files
    # For this demo, we return a placeholder
    return f"# Agent prompt would be loaded from {prompt_file}"


def deploy_agent(agent_config: Dict) -> bool:
    """
    Deploy a single agent.
    
    In a real implementation, this would:
    1. Call the agent management API (manage_agents)
    2. Configure the agent with prompts and tools
    3. Verify deployment success
    
    For this demo script, we simulate the deployment.
    """
    print(f"  📦 Deploying: {agent_config['name']}")
    print(f"     ID: {agent_config['id']}")
    print(f"     Tools: {', '.join(agent_config['toolkits'])}")
    
    # Simulate deployment (in real implementation, call manage_agents here)
    # Example:
    # manage_agents(
    #     action="create",
    #     name=agent_config["name"],
    #     description=agent_config["description"],
    #     selected_toolkits=agent_config["toolkits"]
    # )
    
    print(f"  ✅ Deployed: {agent_config['name']}")
    return True


def deploy_phase(phase: str) -> bool:
    """Deploy a specific phase of agents."""
    agents = AGENT_CONFIGS.get(phase, [])
    
    if not agents:
        print(f"❌ Error: Unknown phase '{phase}'")
        return False
    
    print(f"\n🚀 Deploying Phase {phase[-1]}...")
    print(f"   Agents to deploy: {len(agents)}")
    print()
    
    success_count = 0
    for agent in agents:
        if deploy_agent(agent):
            success_count += 1
        print()
    
    print(f"📊 Phase {phase[-1]} Summary:")
    print(f"   Deployed: {success_count}/{len(agents)} agents")
    
    if success_count == len(agents):
        print(f"✅ Phase {phase[-1]} deployment successful")
        return True
    else:
        print(f"⚠️  Phase {phase[-1]} deployment incomplete")
        return False


def deploy_all():
    """Deploy all agents in sequence."""
    print("\n🚀 Deploying ALL agents...")
    print()
    
    phases = ["phase1", "phase2", "phase3"]
    results = []
    
    for phase in phases:
        result = deploy_phase(phase)
        results.append(result)
        print()
    
    total_agents = sum(len(AGENT_CONFIGS[p]) for p in phases)
    successful = sum(results)
    
    print("=" * 60)
    print("📊 DEPLOYMENT SUMMARY")
    print("=" * 60)
    print(f"Total Phases: {len(phases)}")
    print(f"Successful Phases: {successful}/{len(phases)}")
    print(f"Total Agents: {total_agents}")
    print()
    
    if all(results):
        print("✅ ALL AGENTS DEPLOYED SUCCESSFULLY")
        print()
        print("Next steps:")
        print("1. Run tests: python scripts/test-suite.py --all")
        print("2. Verify agents: Check agent management dashboard")
        print("3. Test usage: Try sample queries")
        return True
    else:
        print("⚠️  DEPLOYMENT INCOMPLETE")
        print("Please check errors above and retry")
        return False


def main():
    """Main deployment function."""
    parser = argparse.ArgumentParser(
        description="Deploy Microsoft Copilot Agent Team"
    )
    parser.add_argument(
        "--phase",
        type=int,
        choices=[1, 2, 3],
        help="Deploy specific phase (1, 2, or 3)"
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Deploy all phases"
    )
    
    args = parser.parse_args()
    
    print_banner()
    
    # Validate environment
    if not validate_environment():
        sys.exit(1)
    
    # Deploy based on arguments
    if args.all:
        success = deploy_all()
    elif args.phase:
        phase_key = f"phase{args.phase}"
        success = deploy_phase(phase_key)
    else:
        print("❌ Error: Must specify --phase or --all")
        parser.print_help()
        sys.exit(1)
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
