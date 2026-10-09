# Local Agent Runtime

A local AI agent runtime built around Ollama.

The project explores the engineering behind agentic systems:

- Tool calling
- Agent state
- Conversation persistence
- Context management
- Task orchestration
- Multi-agent execution
- Persistent workspace
- Long-running tasks

## Current Status

Single-agent runtime with:

- Ollama model integration
- Custom tool registration
- Automatic tool schema generation
- Tool execution
- Persistent JSON sessions
- Context management

## Architecture

User
  ↓
Agent
  ↓
Ollama
  ↓
Tool calls
  ↓
Tool execution
  ↓
Persistent session

## Roadmap

- Basic agent
- Tool calling
- Tool schema generation
- Session persistence
- Context management
- Multiple agents
- Task planner
- Agent orchestration
- Workspace / artifacts
- Critic / evaluator
- Long-term memory
