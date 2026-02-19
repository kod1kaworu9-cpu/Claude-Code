"""
Example usage of the AgentTeam multi-agent system.

Before running, set your API key:
    export ANTHROPIC_API_KEY=your_key_here
Or create a .env file with:
    ANTHROPIC_API_KEY=your_key_here
"""

import sys
import os

# Allow running from the examples/ directory
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src import AgentTeam
from src.agents import ResearchAgent, CoderAgent, ReviewerAgent, WriterAgent


# ── Example 1: Default team (all agents) ─────────────────────────────────────

def example_default_team():
    """Use the default team to solve a multi-faceted task."""
    team = AgentTeam.default()
    result = team.run(
        "Implement a Python function that finds the longest common subsequence (LCS) "
        "of two strings. Include an explanation of the algorithm, the implementation, "
        "and a code review."
    )
    print("\n=== Final Result ===")
    print(result)


# ── Example 2: Custom team (subset of agents) ─────────────────────────────────

def example_custom_team():
    """Use a custom subset of agents for a focused task."""
    team = AgentTeam(agents=["researcher", "writer"])
    result = team.run(
        "Explain the trade-offs between REST and GraphQL APIs for a new project."
    )
    print("\n=== Final Result ===")
    print(result)


# ── Example 3: Custom agent ───────────────────────────────────────────────────

def example_custom_agent():
    """Add a custom agent to the team."""
    import anthropic
    from src.agents import BaseAgent

    class SecurityAgent(BaseAgent):
        """Custom agent that reviews code for security issues."""

        def __init__(self, client: anthropic.Anthropic):
            super().__init__(
                name="SecurityAgent",
                role="Security Expert",
                instructions=(
                    "You are a security expert. Review code and systems for:\n"
                    "- Common vulnerabilities (OWASP Top 10)\n"
                    "- Input validation issues\n"
                    "- Authentication/authorization flaws\n"
                    "- Data exposure risks\n"
                    "Provide a security score (1-10) and list of findings."
                ),
                client=client,
            )

    team = AgentTeam(agents=["coder"])
    team.add_agent(SecurityAgent(client=team.client))

    result = team.run(
        "Write a simple Python login function that checks username and password, "
        "then review it for security issues."
    )
    print("\n=== Final Result ===")
    print(result)


# ── Main ──────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    examples = {
        "1": ("Default team - LCS algorithm", example_default_team),
        "2": ("Custom team - REST vs GraphQL", example_custom_team),
        "3": ("Custom agent - Security review", example_custom_agent),
    }

    print("Available examples:")
    for key, (name, _) in examples.items():
        print(f"  {key}. {name}")

    choice = input("\nChoose an example (1-3): ").strip()
    if choice in examples:
        _, fn = examples[choice]
        fn()
    else:
        print("Invalid choice. Running example 1.")
        example_default_team()
