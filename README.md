# Claude-Code Agent Team

A Python framework for building multi-agent systems powered by Claude.

## Architecture

```
User Task
   │
   ▼
OrchestratorAgent          ← Breaks down task, coordinates agents
   │
   ├─► ResearchAgent        ← Research, analysis, synthesis
   ├─► CoderAgent           ← Code writing & execution
   ├─► ReviewerAgent        ← Quality review & feedback
   └─► WriterAgent          ← Documentation & writing
```

The **OrchestratorAgent** uses Claude's tool-use capability to delegate subtasks to specialized sub-agents via a `delegate_task` tool. It passes context between agents and synthesizes a final response.

## Setup

```bash
pip install -r requirements.txt

cp .env.example .env
# Edit .env and add your ANTHROPIC_API_KEY
```

## Quick Start

```python
from src import AgentTeam

team = AgentTeam.default()
result = team.run("Implement and review a binary search in Python.")
print(result)
```

## Custom Teams

Use a subset of agents:

```python
team = AgentTeam(agents=["researcher", "coder"])
result = team.run("Research and implement a rate limiter.")
```

Add a custom agent:

```python
from src.agents import BaseAgent
import anthropic

class SecurityAgent(BaseAgent):
    def __init__(self, client: anthropic.Anthropic):
        super().__init__(
            name="SecurityAgent",
            role="Security Expert",
            instructions="You are a security expert. Review code for vulnerabilities...",
            client=client,
        )

team = AgentTeam(agents=["coder"])
team.add_agent(SecurityAgent(client=team.client))
result = team.run("Write a login function and check it for security issues.")
```

## Available Agents

| Agent | Role | Capabilities |
|-------|------|-------------|
| `researcher` | Researcher | Analysis, synthesis, best practices |
| `coder` | Software Engineer | Code writing, Python execution |
| `reviewer` | Quality Reviewer | Bug detection, code review, feedback |
| `writer` | Technical Writer | Documentation, explanations |

## Project Structure

```
Claude-Code/
├── src/
│   ├── team.py                    # AgentTeam - main entry point
│   └── agents/
│       ├── base_agent.py          # BaseAgent class
│       ├── specialized_agents.py  # Built-in agents
│       └── orchestrator.py        # OrchestratorAgent
├── examples/
│   └── example.py                 # Usage examples
├── requirements.txt
└── .env.example
```

## Running Examples

```bash
python examples/example.py
```
