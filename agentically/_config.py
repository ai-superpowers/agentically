"""Registry and environment configuration."""

import os

# GitHub repository that hosts the agents/ registry.
# Override via environment variables for forks or local testing.
REGISTRY_ORG: str = os.environ.get("AGENTICALLY_ORG", "ai-superpowers")
REGISTRY_REPO: str = os.environ.get("AGENTICALLY_REPO", "agentically")
REGISTRY_BRANCH: str = os.environ.get("AGENTICALLY_BRANCH", "main")
