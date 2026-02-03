#!/usr/bin/env python3
"""
Microsoft Copilot Agent Team - Setup and Validation Script
Version: 1.0.0
Description: Validates environment and prepares for deployment
"""

import os
import sys
import json
from pathlib import Path

def print_header(text):
    """Print formatted header"""
    print(f"\n{'='*60}")
    print(f"  {text}")
    print(f"{'='*60}\n")

def check_python_version():
    """Verify Python version >= 3.8"""
    print("🐍 Checking Python version...")
    if sys.version_info < (3, 8):
        print(f"❌ Python 3.8+ required. Current: {sys.version}")
        return False
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}")
    return True

def check_environment_variables():
    """Check required environment variables"""
    print("\n🔧 Checking environment variables...")
    
    required_vars = {
        "TENANT_ID": "Your Microsoft 365 Tenant ID",
        "ENVIRONMENT_URL": "Power Platform Environment URL",
    }
    
    optional_vars = {
        "CLIENT_ID": "Azure AD App Registration Client ID",
        "CLIENT_SECRET": "Azure AD App Registration Secret",
    }
    
    missing = []
    for var, description in required_vars.items():
        if not os.getenv(var):
            missing.append(f"  • {var}: {description}")
            print(f"❌ Missing: {var}")
        else:
            print(f"✅ Found: {var}")
    
    if missing:
        print(f"\n⚠️  Missing required environment variables:")
        for item in missing:
            print(item)
        print(f"\nSet them in .env file or export them:")
        print(f"  export TENANT_ID='your-tenant-id'")
        print(f"  export ENVIRONMENT_URL='https://your-env.crm.dynamics.com'")
        return False
    
    # Check optional
    print(f"\n📋 Optional variables:")
    for var, description in optional_vars.items():
        if os.getenv(var):
            print(f"✅ {var} (configured)")
        else:
            print(f"⚠️  {var} (not set - will use interactive auth)")
    
    return True

def create_config_template():
    """Create sample configuration file"""
    print("\n📝 Creating configuration template...")
    
    config_template = {
        "environment": {
            "name": "production",
            "tenant_id": "${TENANT_ID}",
            "environment_url": "${ENVIRONMENT_URL}",
            "region": "East US"
        },
        "agents": {
            "orchestrator": {
                "enabled": True,
                "max_parallel_tasks": 6,
                "timeout_seconds": 30
            },
            "m365_agent": {
                "enabled": True,
                "scopes": ["Mail.ReadWrite", "Calendars.ReadWrite", "Files.ReadWrite.All"]
            },
            "data_agent": {
                "enabled": True,
                "data_sources": ["Dataverse", "SharePoint", "Excel"]
            },
            "it_agent": {
                "enabled": True,
                "knowledge_base": "sharepoint://sites/ITSupport/KB"
            },
            "automation_agent": {
                "enabled": True
            },
            "research_agent": {
                "enabled": True
            },
            "content_agent": {
                "enabled": True,
                "templates_location": "sharepoint://sites/Templates"
            }
        },
        "security": {
            "authentication": "EntraID",
            "mfa_required": True,
            "session_timeout_minutes": 30
        },
        "monitoring": {
            "application_insights": True,
            "log_level": "INFO"
        }
    }
    
    config_dir = Path("config")
    config_dir.mkdir(exist_ok=True)
    
    config_file = config_dir / "agents.example.json"
    with open(config_file, 'w') as f:
        json.dump(config_template, f, indent=2)
    
    print(f"✅ Created: {config_file}")
    print(f"   Copy to config/agents.json and customize")
    
    return True

def check_dependencies():
    """Check if required Python packages are installed"""
    print("\n📦 Checking Python dependencies...")
    
    required_packages = [
        "requests",
        "python-dotenv",
        "pyyaml",
    ]
    
    missing = []
    for package in required_packages:
        try:
            __import__(package.replace("-", "_"))
            print(f"✅ {package}")
        except ImportError:
            missing.append(package)
            print(f"❌ {package}")
    
    if missing:
        print(f"\n⚠️  Missing packages. Install with:")
        print(f"  pip install -r requirements.txt")
        return False
    
    return True

def create_directory_structure():
    """Create necessary directories"""
    print("\n📁 Creating directory structure...")
    
    directories = [
        "config",
        "logs",
        "scripts",
        "docs",
        "tests",
        "data"
    ]
    
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
        print(f"✅ {directory}/")
    
    return True

def main():
    """Main setup routine"""
    print_header("Microsoft Copilot Agent Team - Setup")
    
    print("This script will validate your environment and prepare for deployment.\n")
    
    checks = [
        ("Python Version", check_python_version),
        ("Directory Structure", create_directory_structure),
        ("Configuration Template", create_config_template),
        ("Python Dependencies", check_dependencies),
        ("Environment Variables", check_environment_variables),
    ]
    
    results = []
    for name, check_func in checks:
        try:
            result = check_func()
            results.append((name, result))
        except Exception as e:
            print(f"❌ Error in {name}: {str(e)}")
            results.append((name, False))
    
    print_header("Setup Summary")
    
    all_passed = all(result for _, result in results)
    
    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status}: {name}")
    
    if all_passed:
        print(f"\n🎉 Setup completed successfully!")
        print(f"\nNext steps:")
        print(f"  1. Review config/agents.example.json")
        print(f"  2. Copy to config/agents.json and customize")
        print(f"  3. Set environment variables in .env")
        print(f"  4. Run: python scripts/deploy-agents.py")
        return 0
    else:
        print(f"\n⚠️  Setup incomplete. Please fix the issues above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
