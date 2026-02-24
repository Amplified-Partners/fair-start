#!/usr/bin/env python3
"""
Family AI Setup Script
Creates OpenClaw agent directories and bootstrap files for each family member.
Run once per person, or run for all with: python3 setup.py --all

Usage:
  python3 setup.py --all                    # Set up all six agents
  python3 setup.py --agent demario          # Set up one agent
  python3 setup.py --list                   # Show current status
"""
import json
import os
import sys
import argparse
from pathlib import Path

HOME = Path.home()
OPENCLAW_DIR = HOME / ".openclaw"

AGENTS = {
    "demario": {
        "display": "Demario",
        "emoji": "✨",
        "age": 14,
        "vibe": "curious, creative, reflective",
    },
    "freya": {
        "display": "Freya",
        "emoji": "🎨",
        "age": 17,
        "vibe": "creative, driven, building something",
    },
    "tyrone": {
        "display": "Tyrone",
        "emoji": "⚡",
        "age": 26,
        "vibe": "analytical, ambitious, learning fast",
    },
    "tom": {
        "display": "Tom",
        "emoji": "🏗️",
        "age": 18,
        "vibe": "precise, practical, building things",
    },
    "ava": {
        "display": "Ava",
        "emoji": "🌟",
        "age": 18,
        "vibe": "exploring, finding direction",
    },
    "james": {
        "display": "James",
        "emoji": "🧠",
        "age": 22,
        "vibe": "perceptive, analytical, pattern-finding",
    },
}


def soul_md(agent: dict) -> str:
    return f"""# Soul

You are {agent['display']}'s personal AI. You have one job: help them achieve whatever they tell you they're working toward.

## How you work

- Ask what they think before you answer. Guide their reasoning before giving yours.
- When they're about to do something that will hurt them: say so clearly, show the consequences, then let them choose.
- Their data is theirs. You don't report to anyone. Not to Ewan, not to anyone else.
- No agenda. No curriculum. Follow their lead.
- If something genuinely worries you: raise it with them directly, not with anyone else.

## What you're not

- Not a teacher. Not a filter. Not a monitor.
- Not neutral — you have opinions, share them when asked.
- Not an oracle — ask questions, think together.

## The one rule

Win-win only. Radical honesty. Their choice always.
""".strip()


def identity_md(agent: dict) -> str:
    return f"""# Identity

Name: {agent['display']}
Emoji: {agent['emoji']}
Vibe: {agent['vibe']}
""".strip()


def user_md(agent: dict) -> str:
    return f"""# User Profile

Name: {agent['display']}
Age: {agent['age']}

## What they're working on
[To be filled in after first conversation]

## Their stated goal
[To be filled in after first conversation]

## What they're into
[To be filled in after onboarding interview]

## Preferences
[To be filled in over time]
""".strip()


def agents_md(agent: dict) -> str:
    return f"""# Operating Instructions

You are {agent['display']}'s personal AI.

## Your job
Help them make progress toward whatever goal they've stated. If they haven't stated one yet, ask.

## Each conversation
1. Pick up where you left off
2. Help them move forward
3. Ask before solving
4. Note what happened for next time

## Memory
Use your conversation history. Reference what they've told you before.
If they change their goal: update immediately, no resistance.

## First conversation
If this is the first time: ask their name (confirm), ask what they're working on right now, ask what a good outcome looks like. Then start helping.
""".strip()


def create_agent(agent_id: str) -> None:
    agent = AGENTS[agent_id]
    workspace = OPENCLAW_DIR / f"workspace-{agent_id}"
    agent_dir = OPENCLAW_DIR / "agents" / agent_id / "agent"

    workspace.mkdir(parents=True, exist_ok=True)
    agent_dir.mkdir(parents=True, exist_ok=True)

    (workspace / "SOUL.md").write_text(soul_md(agent))
    (workspace / "IDENTITY.md").write_text(identity_md(agent))
    (workspace / "USER.md").write_text(user_md(agent))
    (workspace / "AGENTS.md").write_text(agents_md(agent))

    print(f"✅ {agent['display']} ({agent_id}) — directories and bootstrap files created")
    print(f"   Workspace: {workspace}")
    print(f"   Agent dir: {agent_dir}")
    print(f"   Next: add Telegram bot token to openclaw.json")
    print()


def show_config_snippet(agent_ids: list) -> None:
    print("\n" + "="*60)
    print("Add this to your openclaw.json agents.list:")
    print("="*60)
    for agent_id in agent_ids:
        agent = AGENTS[agent_id]
        snippet = {
            "id": agent_id,
            "workspace": f"~/.openclaw/workspace-{agent_id}",
            "agentDir": f"~/.openclaw/agents/{agent_id}/agent",
            "agent": {
                "model": {
                    "primary": "anthropic/claude-haiku-4-5-20251001",
                    "fallbacks": ["anthropic/claude-sonnet-4-6"]
                }
            }
        }
        print(json.dumps(snippet, indent=2))
        print()

    print("="*60)
    print("Add bindings (one per person, after you have their bot token):")
    print("="*60)
    for agent_id in agent_ids:
        print(f"""{{
  "agentId": "{agent_id}",
  "match": {{ "telegram": {{ "chatId": "REPLACE_WITH_{agent_id.upper()}_CHAT_ID" }} }}
}},""")

    print("\n⚠️  You need one Telegram bot per person.")
    print("Create them via @BotFather on Telegram — /newbot for each one.")
    print("Then add each bot token to the telegram channel config in openclaw.json")


def list_status() -> None:
    print("\nFamily AI Agent Status:")
    print("-" * 40)
    for agent_id, agent in AGENTS.items():
        workspace = OPENCLAW_DIR / f"workspace-{agent_id}"
        exists = workspace.exists()
        status = "✅ Created" if exists else "⬜ Not set up"
        print(f"  {agent['emoji']} {agent['display']:10} {status}")
    print()


def main():
    parser = argparse.ArgumentParser(description="Family AI setup")
    parser.add_argument("--all", action="store_true", help="Set up all agents")
    parser.add_argument("--agent", help="Set up a specific agent")
    parser.add_argument("--list", action="store_true", help="Show status")
    parser.add_argument("--config", action="store_true", help="Show config snippet only")
    args = parser.parse_args()

    if args.list:
        list_status()
    elif args.config:
        show_config_snippet(list(AGENTS.keys()))
    elif args.all:
        print("Setting up all Family AI agents...\n")
        for agent_id in AGENTS:
            create_agent(agent_id)
        show_config_snippet(list(AGENTS.keys()))
    elif args.agent:
        if args.agent not in AGENTS:
            print(f"Unknown agent: {args.agent}. Choose from: {', '.join(AGENTS.keys())}")
            sys.exit(1)
        create_agent(args.agent)
        show_config_snippet([args.agent])
    else:
        parser.print_help()
        print()
        list_status()


if __name__ == "__main__":
    main()
