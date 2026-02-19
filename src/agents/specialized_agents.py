"""Specialized sub-agents for the agent team."""

import json
import subprocess
import anthropic

from .base_agent import BaseAgent, DEFAULT_MODEL


class ResearchAgent(BaseAgent):
    """Agent specialized in research, analysis, and information synthesis."""

    def __init__(self, client: anthropic.Anthropic, model: str = DEFAULT_MODEL):
        super().__init__(
            name="ResearchAgent",
            role="Researcher",
            instructions=(
                "You are an expert researcher and analyst. Your job is to:\n"
                "- Deeply analyze problems and break them down into key components\n"
                "- Gather and synthesize relevant information\n"
                "- Identify patterns, trade-offs, and best practices\n"
                "- Provide well-structured, evidence-based findings\n"
                "- Be thorough but concise in your responses\n"
                "Always structure your output clearly with sections and bullet points where appropriate."
            ),
            client=client,
            model=model,
        )


class CoderAgent(BaseAgent):
    """Agent specialized in writing, reviewing, and debugging code."""

    TOOLS = [
        {
            "name": "run_python",
            "description": "Execute a Python code snippet and return stdout/stderr. Use this to test or validate code.",
            "input_schema": {
                "type": "object",
                "properties": {
                    "code": {
                        "type": "string",
                        "description": "The Python code to execute.",
                    }
                },
                "required": ["code"],
            },
        }
    ]

    def __init__(self, client: anthropic.Anthropic, model: str = DEFAULT_MODEL):
        super().__init__(
            name="CoderAgent",
            role="Software Engineer",
            instructions=(
                "You are an expert software engineer. Your job is to:\n"
                "- Write clean, efficient, and well-documented code\n"
                "- Follow best practices and design patterns\n"
                "- Handle edge cases and errors gracefully\n"
                "- Use the run_python tool to test your code when appropriate\n"
                "- Explain your implementation decisions clearly\n"
                "Always provide complete, runnable code with clear explanations."
            ),
            client=client,
            tools=self.TOOLS,
            model=model,
        )

    def execute_tool(self, tool_name: str, tool_input: dict) -> str:
        if tool_name == "run_python":
            return self._run_python(tool_input["code"])
        return super().execute_tool(tool_name, tool_input)

    def _run_python(self, code: str) -> str:
        """Execute Python code in a subprocess and return the result."""
        try:
            result = subprocess.run(
                ["python3", "-c", code],
                capture_output=True,
                text=True,
                timeout=30,
            )
            output = ""
            if result.stdout:
                output += f"stdout:\n{result.stdout}"
            if result.stderr:
                output += f"stderr:\n{result.stderr}"
            if not output:
                output = "(no output)"
            return output
        except subprocess.TimeoutExpired:
            return "Error: Code execution timed out (30s limit)"
        except Exception as e:
            return f"Error: {e}"


class ReviewerAgent(BaseAgent):
    """Agent specialized in reviewing, critiquing, and improving work."""

    def __init__(self, client: anthropic.Anthropic, model: str = DEFAULT_MODEL):
        super().__init__(
            name="ReviewerAgent",
            role="Quality Reviewer",
            instructions=(
                "You are a meticulous quality reviewer. Your job is to:\n"
                "- Critically evaluate work for correctness, completeness, and quality\n"
                "- Identify bugs, logical errors, and potential improvements\n"
                "- Check for security issues, edge cases, and maintainability\n"
                "- Provide constructive, actionable feedback\n"
                "- Summarize your findings with a clear verdict (PASS / NEEDS WORK / FAIL)\n"
                "Be thorough and specific. Always include your verdict at the end."
            ),
            client=client,
            model=model,
        )


class WriterAgent(BaseAgent):
    """Agent specialized in writing clear documentation and explanations."""

    def __init__(self, client: anthropic.Anthropic, model: str = DEFAULT_MODEL):
        super().__init__(
            name="WriterAgent",
            role="Technical Writer",
            instructions=(
                "You are an expert technical writer. Your job is to:\n"
                "- Write clear, concise, and engaging documentation\n"
                "- Explain complex concepts in accessible language\n"
                "- Structure content logically with proper headings and examples\n"
                "- Adapt tone and detail level to the target audience\n"
                "- Produce polished, publication-ready text\n"
                "Always aim for clarity and completeness."
            ),
            client=client,
            model=model,
        )


# Registry of available agent types for dynamic instantiation
AGENT_REGISTRY: dict[str, type[BaseAgent]] = {
    "researcher": ResearchAgent,
    "coder": CoderAgent,
    "reviewer": ReviewerAgent,
    "writer": WriterAgent,
}
