"""Base agent class for all agents in the team."""

from typing import Any
import anthropic


DEFAULT_MODEL = "claude-opus-4-6"


class BaseAgent:
    """Base class for all agents.

    Each agent has a name, a role description, and a system prompt (instructions).
    Agents communicate with Claude via the Anthropic API and can optionally use tools.
    """

    def __init__(
        self,
        name: str,
        role: str,
        instructions: str,
        client: anthropic.Anthropic,
        tools: list[dict] | None = None,
        model: str = DEFAULT_MODEL,
        max_tokens: int = 4096,
    ):
        self.name = name
        self.role = role
        self.instructions = instructions
        self.client = client
        self.tools = tools or []
        self.model = model
        self.max_tokens = max_tokens

    def run(self, task: str, context: str = "") -> str:
        """Run the agent on a task and return the result.

        Args:
            task: The task description for the agent.
            context: Optional additional context from previous steps.

        Returns:
            The agent's response as a string.
        """
        user_content = task
        if context:
            user_content = f"Context from previous steps:\n{context}\n\nYour task:\n{task}"

        messages: list[dict[str, Any]] = [{"role": "user", "content": user_content}]

        while True:
            kwargs: dict[str, Any] = {
                "model": self.model,
                "max_tokens": self.max_tokens,
                "system": self.instructions,
                "messages": messages,
            }
            if self.tools:
                kwargs["tools"] = self.tools

            response = self.client.messages.create(**kwargs)

            if response.stop_reason == "end_turn":
                return self._extract_text(response)

            if response.stop_reason == "tool_use":
                tool_results = self._handle_tool_use(response)
                messages.append({"role": "assistant", "content": response.content})
                messages.append({"role": "user", "content": tool_results})
            else:
                return self._extract_text(response)

    def _extract_text(self, response: anthropic.types.Message) -> str:
        """Extract text content from a response."""
        parts = []
        for block in response.content:
            if hasattr(block, "text"):
                parts.append(block.text)
        return "\n".join(parts)

    def _handle_tool_use(self, response: anthropic.types.Message) -> list[dict]:
        """Handle tool use blocks in a response.

        Subclasses should override this method to implement custom tool handling.
        Returns a list of tool result content blocks.
        """
        results = []
        for block in response.content:
            if block.type == "tool_use":
                result = self.execute_tool(block.name, block.input)
                results.append({
                    "type": "tool_result",
                    "tool_use_id": block.id,
                    "content": str(result),
                })
        return results

    def execute_tool(self, tool_name: str, tool_input: dict) -> Any:
        """Execute a tool by name. Override in subclasses to add tools."""
        raise NotImplementedError(f"Tool '{tool_name}' not implemented in {self.name}")

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(name={self.name!r}, role={self.role!r})"
