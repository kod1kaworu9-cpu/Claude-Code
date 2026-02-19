"""Orchestrator agent that coordinates the agent team."""

import json
from typing import Any
import anthropic

from .base_agent import BaseAgent, DEFAULT_MODEL


class OrchestratorAgent(BaseAgent):
    """Orchestrates a team of specialized agents.

    The orchestrator receives a high-level task, breaks it down into subtasks,
    delegates each subtask to the most appropriate sub-agent, and synthesizes
    the results into a final answer.

    It uses a `delegate_task` tool to invoke sub-agents dynamically.
    """

    def __init__(
        self,
        sub_agents: list[BaseAgent],
        client: anthropic.Anthropic,
        model: str = DEFAULT_MODEL,
    ):
        self.sub_agents: dict[str, BaseAgent] = {agent.name: agent for agent in sub_agents}

        agent_descriptions = "\n".join(
            f"- {agent.name} ({agent.role})" for agent in sub_agents
        )

        tools = [
            {
                "name": "delegate_task",
                "description": (
                    "Delegate a subtask to one of the specialized sub-agents in the team. "
                    "The agent will execute the task and return its result. "
                    "You can call this multiple times to coordinate multiple agents.\n\n"
                    f"Available agents:\n{agent_descriptions}"
                ),
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "agent_name": {
                            "type": "string",
                            "description": (
                                "Name of the agent to delegate to. "
                                f"Must be one of: {', '.join(self.sub_agents.keys())}"
                            ),
                        },
                        "task": {
                            "type": "string",
                            "description": "Clear description of the subtask for the agent.",
                        },
                        "context": {
                            "type": "string",
                            "description": (
                                "Optional context from previous steps to share with the agent."
                            ),
                        },
                    },
                    "required": ["agent_name", "task"],
                },
            }
        ]

        instructions = (
            "You are the orchestrator of a multi-agent team. Your job is to:\n"
            "1. Analyze the user's request and break it into clear subtasks\n"
            "2. Delegate each subtask to the most appropriate agent using delegate_task\n"
            "3. Pass relevant context between agents so they can build on each other's work\n"
            "4. Synthesize all results into a coherent final response\n\n"
            "Available agents and their specialties:\n"
            f"{agent_descriptions}\n\n"
            "Guidelines:\n"
            "- Think step-by-step before delegating\n"
            "- Use multiple agents when the task benefits from different perspectives\n"
            "- Pass output from one agent as context to the next when relevant\n"
            "- Synthesize results clearly and concisely in your final response"
        )

        super().__init__(
            name="OrchestratorAgent",
            role="Team Orchestrator",
            instructions=instructions,
            client=client,
            tools=tools,
            model=model,
        )

    def execute_tool(self, tool_name: str, tool_input: dict) -> Any:
        if tool_name == "delegate_task":
            return self._delegate_task(
                agent_name=tool_input["agent_name"],
                task=tool_input["task"],
                context=tool_input.get("context", ""),
            )
        return super().execute_tool(tool_name, tool_input)

    def _delegate_task(self, agent_name: str, task: str, context: str = "") -> str:
        """Delegate a task to a sub-agent and return the result."""
        agent = self.sub_agents.get(agent_name)
        if agent is None:
            available = ", ".join(self.sub_agents.keys())
            return f"Error: Agent '{agent_name}' not found. Available agents: {available}"

        print(f"  -> Delegating to {agent_name}: {task[:80]}{'...' if len(task) > 80 else ''}")

        result = agent.run(task=task, context=context)
        return f"[Result from {agent_name}]\n{result}"
