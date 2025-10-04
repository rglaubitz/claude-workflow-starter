#!/usr/bin/env python3
"""
Specialist Agent Invoker
Directly invoke specialist agents via Anthropic API when Task tool doesn't support them
"""

import anthropic
import argparse
import json
import sys
from pathlib import Path
from datetime import datetime
import os

CLAUDE_HOME = Path.home() / ".claude"
AGENTS_DIR = CLAUDE_HOME / "agents"
LOGS_DIR = CLAUDE_HOME / "logs" / "agent-invocations"
LOGS_DIR.mkdir(parents=True, exist_ok=True)

def load_agent_definition(agent_name: str) -> dict:
    """Load agent definition from markdown file"""
    agent_file = AGENTS_DIR / f"{agent_name}.md"

    if not agent_file.exists():
        raise FileNotFoundError(f"Agent not found: {agent_name}")

    content = agent_file.read_text()

    # Parse YAML frontmatter
    if content.startswith('---'):
        parts = content.split('---', 2)
        if len(parts) >= 3:
            frontmatter_text = parts[1]
            agent_instructions = parts[2].strip()

            # Parse YAML manually (simple approach)
            metadata = {}
            for line in frontmatter_text.strip().split('\n'):
                if ':' in line:
                    key, value = line.split(':', 1)
                    metadata[key.strip()] = value.strip().strip('"')

            return {
                'name': metadata.get('name', agent_name),
                'description': metadata.get('description', ''),
                'tools': metadata.get('tools', ''),
                'model': metadata.get('model', 'claude-sonnet-4'),
                'instructions': agent_instructions
            }

    raise ValueError(f"Agent file {agent_name}.md missing YAML frontmatter")

def invoke_agent(agent_name: str, task: str, api_key: str = None) -> dict:
    """Invoke a specialist agent with a task"""

    # Get API key
    if not api_key:
        api_key = os.environ.get('ANTHROPIC_API_KEY')

    if not api_key:
        raise ValueError(
            "ANTHROPIC_API_KEY not set. Either:\n"
            "  1. Export: export ANTHROPIC_API_KEY='sk-ant-...'\n"
            "  2. Pass: --api-key sk-ant-...\n"
            "  3. Use password manager: ANTHROPIC_API_KEY=$(pass show anthropic/api-key)"
        )

    # Load agent definition
    print(f"📋 Loading agent: {agent_name}")
    agent = load_agent_definition(agent_name)
    print(f"   Description: {agent['description']}")
    print(f"   Model: {agent['model']}")

    # Create client
    client = anthropic.Anthropic(api_key=api_key)

    # Build system prompt from agent instructions
    system_prompt = agent['instructions']

    # Invoke agent
    print(f"\n🚀 Invoking {agent['name']}...")
    print(f"   Task: {task[:100]}{'...' if len(task) > 100 else ''}\n")

    start_time = datetime.now()

    try:
        message = client.messages.create(
            model=agent['model'],
            max_tokens=4096,
            system=system_prompt,
            messages=[
                {"role": "user", "content": task}
            ]
        )

        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()

        result = {
            'agent': agent_name,
            'task': task,
            'response': message.content[0].text if message.content else '',
            'model': message.model,
            'usage': {
                'input_tokens': message.usage.input_tokens,
                'output_tokens': message.usage.output_tokens
            },
            'duration_seconds': duration,
            'timestamp': datetime.now().isoformat()
        }

        # Log the invocation
        log_file = LOGS_DIR / f"{agent_name}-{datetime.now().strftime('%Y%m%d-%H%M%S')}.json"
        log_file.write_text(json.dumps(result, indent=2))

        print(f"✅ Agent completed in {duration:.2f}s")
        print(f"   Input tokens: {result['usage']['input_tokens']}")
        print(f"   Output tokens: {result['usage']['output_tokens']}")
        print(f"   Log: {log_file}")
        print(f"\n{'='*80}")
        print(f"RESPONSE:\n{result['response']}")
        print(f"{'='*80}\n")

        return result

    except Exception as e:
        error_result = {
            'agent': agent_name,
            'task': task,
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }

        log_file = LOGS_DIR / f"{agent_name}-ERROR-{datetime.now().strftime('%Y%m%d-%H%M%S')}.json"
        log_file.write_text(json.dumps(error_result, indent=2))

        print(f"❌ Agent invocation failed: {e}")
        print(f"   Error log: {log_file}")

        return error_result

def list_agents():
    """List all available specialist agents"""
    print("📋 Available Specialist Agents:\n")

    categories = {
        'Orchestration': ['task-manager', 'project-task-planner', 'prd-expert', 'agent-architecture-designer'],
        'Development': ['database-architect', 'graph-database-specialist', 'ai-ml-engineer',
                       'frontend-developer', 'backend-developer', 'devops-engineer'],
        'Quality': ['security-auditor', 'performance-engineer', 'accessibility-specialist', 'qa-engineer'],
        'Review': ['code-review-expert', 'database-reviewer', 'frontend-reviewer', 'backend-reviewer'],
        'Support': ['api-architect', 'ui-ux-designer', 'data-pipeline-engineer',
                   'knowledge-graph-engineer', 'sql-specialist', 'integration-specialist', 'mcp-bridge-engineer'],
        'Research': ['research-manager', 'documentation-expert', 'agent-testing-engineer', 'memory-system-engineer'],
        'C-Suite': ['CIO', 'CTO', 'COO']
    }

    for category, agents in categories.items():
        print(f"{category}:")
        for agent in agents:
            agent_file = AGENTS_DIR / f"{agent}.md"
            exists = "✅" if agent_file.exists() else "❌"
            print(f"  {exists} {agent}")
        print()

def main():
    parser = argparse.ArgumentParser(description='Invoke Claude specialist agents')
    parser.add_argument('command', choices=['list', 'invoke'], help='Command to execute')
    parser.add_argument('--agent', help='Agent name to invoke')
    parser.add_argument('--task', help='Task for the agent')
    parser.add_argument('--api-key', help='Anthropic API key (or use ANTHROPIC_API_KEY env var)')

    args = parser.parse_args()

    if args.command == 'list':
        list_agents()

    elif args.command == 'invoke':
        if not args.agent:
            print("❌ Error: --agent required for invoke command")
            sys.exit(1)

        if not args.task:
            print("❌ Error: --task required for invoke command")
            sys.exit(1)

        result = invoke_agent(args.agent, args.task, args.api_key)

        if 'error' in result:
            sys.exit(1)

if __name__ == '__main__':
    main()
