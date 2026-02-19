"""AgentTeam: High-level interface for building and running a multi-agent team."""

import os
import anthropic
from dotenv import load_dotenv

from .agents.base_agent import BaseAgent, DEFAULT_MODEL
from .agents.specialized_agents import (
    ResearchAgent,
    CoderAgent,
    ReviewerAgent,
    WriterAgent,
    AGENT_REGISTRY,
)
from .agents.orchestrator import OrchestratorAgent


class AgentTeam:
    """A team of specialized agents coordinated by an orchestrator.

    Usage:
        team = AgentTeam.default()
        result = team.run("Build a Python function to parse CSV files and summarize the data.")
        print(result)

    Or with a custom set of agents:
        team = AgentTeam(
            agents=["researcher", "coder"],
            api_key="your-key",
        )
        result = team.run("Research and implement a binary search tree in Python.")
    """

    def __init__(
        self,
        agents: list[str | BaseAgent] | None = None,
        api_key: str | None = None,
        model: str = DEFAULT_MODEL,
        verbose: bool = True,
    ):
        """Initialize an agent team.

        Args:
            agents: List of agent names (from AGENT_REGISTRY) or BaseAgent instances.
                    Defaults to all available agents: researcher, coder, reviewer, writer.
            api_key: Anthropic API key. Falls back to ANTHROPIC_API_KEY env var.
            model: Claude model to use for all agents.
            verbose: If True, print delegation events to stdout.
        """
        load_dotenv()
        api_key = api_key or os.environ.get("ANTHROPIC_API_KEY")
        if not api_key:
            raise ValueError(
                "Anthropic API key is required. Set ANTHROPIC_API_KEY env var or pass api_key."
            )

        self.client = anthropic.Anthropic(api_key=api_key)
        self.model = model
        self.verbose = verbose

        # Build sub-agents
        if agents is None:
            agents = list(AGENT_REGISTRY.keys())

        self.sub_agents: list[BaseAgent] = []
        for agent in agents:
            if isinstance(agent, str):
                agent_cls = AGENT_REGISTRY.get(agent.lower())
                if agent_cls is None:
                    available = ", ".join(AGENT_REGISTRY.keys())
                    raise ValueError(
                        f"Unknown agent '{agent}'. Available: {available}"
                    )
                self.sub_agents.append(agent_cls(client=self.client, model=model))
            elif isinstance(agent, BaseAgent):
                self.sub_agents.append(agent)
            else:
                raise TypeError(f"Expected str or BaseAgent, got {type(agent)}")

        self.orchestrator = OrchestratorAgent(
            sub_agents=self.sub_agents,
            client=self.client,
            model=model,
        )

    @classmethod
    def default(cls, api_key: str | None = None, model: str = DEFAULT_MODEL) -> "AgentTeam":
        """Create a team with all default agents (researcher, coder, reviewer, writer)."""
        return cls(api_key=api_key, model=model)

    def run(self, task: str) -> str:
        """Run the team on a task.

        The orchestrator analyzes the task, delegates subtasks to specialized
        agents, and synthesizes a final response.

        Args:
            task: The task or question to solve.

        Returns:
            The orchestrator's final synthesized response.
        """
        if self.verbose:
            print(f"\n[AgentTeam] Task: {task}")
            print(f"[AgentTeam] Team: {[a.name for a in self.sub_agents]}")
            print("-" * 60)

        result = self.orchestrator.run(task)

        if self.verbose:
            print("-" * 60)
            print("[AgentTeam] Complete.")

        return result

    def add_agent(self, agent: BaseAgent) -> None:
        """Add a new agent to the team."""
        self.sub_agents.append(agent)
        # Rebuild orchestrator with updated agent list
        self.orchestrator = OrchestratorAgent(
            sub_agents=self.sub_agents,
            client=self.client,
            model=self.model,
        )

    def __repr__(self) -> str:
        names = [a.name for a in self.sub_agents]
        return f"AgentTeam(agents={names}, model={self.model!r})"
