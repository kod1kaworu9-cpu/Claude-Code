"""
Multi-agent discussion loop using Claude.

Two agents (Proposer and Critic) alternate in discussing a topic for N rounds,
then a Summarizer produces a final conclusion.

Usage:
    python discussion_loop.py                          # interactive mode
    python discussion_loop.py --topic "テーマ" --rounds 3
"""

import argparse
import os
import sys

import anthropic

# ─── Agent definitions ────────────────────────────────────────────────────────

AGENTS = {
    "proposer": {
        "name": "提案者",
        "system": (
            "あなたは革新的なアイデアを提案するエキスパートです。"
            "与えられたテーマについて具体的かつ建設的な提案を行い、"
            "批判には真摯に向き合って改善案を示してください。"
            "回答は日本語で、200〜300字程度で簡潔にまとめてください。"
        ),
    },
    "critic": {
        "name": "批評家",
        "system": (
            "あなたは鋭い批判的思考を持つ分析専門家です。"
            "相手の提案の弱点・リスク・見落としを的確に指摘し、"
            "より良い方向性を示す建設的な批評を行ってください。"
            "回答は日本語で、200〜300字程度で簡潔にまとめてください。"
        ),
    },
    "summarizer": {
        "name": "まとめ役",
        "system": (
            "あなたは議論の全体像を把握し、要点を整理する専門家です。"
            "これまでの議論を踏まえ、合意点・残課題・最終的な結論を"
            "箇条書きで整理してください。回答は日本語で。"
        ),
    },
}

# ─── Core logic ───────────────────────────────────────────────────────────────


def call_agent(client: anthropic.Anthropic, agent_key: str, messages: list[dict]) -> str:
    """Call a single agent and return its response text."""
    agent = AGENTS[agent_key]
    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1024,
        system=agent["system"],
        messages=messages,
    )
    return response.content[0].text


def run_discussion(topic: str, rounds: int = 3) -> None:
    """
    Run a multi-agent discussion loop.

    Args:
        topic:  The discussion topic.
        rounds: Number of back-and-forth rounds between Proposer and Critic.
    """
    client = anthropic.Anthropic()

    # Shared conversation history (alternating user/assistant turns)
    history: list[dict] = []

    print(f"\n{'='*60}")
    print(f"  議題: {topic}")
    print(f"  ラウンド数: {rounds}")
    print(f"{'='*60}\n")

    # ── Round loop ────────────────────────────────────────────────────────────
    for round_num in range(1, rounds + 1):
        print(f"--- ラウンド {round_num} ---\n")

        for agent_key in ("proposer", "critic"):
            agent_name = AGENTS[agent_key]["name"]

            # Build the prompt for this turn
            if not history:
                # First turn: seed with the topic
                user_content = f"テーマ「{topic}」について、あなたの見解を述べてください。"
            else:
                # Subsequent turns: ask to respond to the previous statement
                prev_name = AGENTS["critic" if agent_key == "proposer" else "proposer"]["name"]
                user_content = f"{prev_name}の発言を踏まえて、あなたの意見を述べてください。"

            history.append({"role": "user", "content": user_content})

            response_text = call_agent(client, agent_key, history)
            history.append({"role": "assistant", "content": response_text})

            print(f"【{agent_name}】")
            print(response_text)
            print()

    # ── Summarization ────────────────────────────────────────────────────────
    print("--- 最終まとめ ---\n")

    summary_prompt = (
        f"テーマ「{topic}」について、"
        f"提案者と批評家が{rounds}ラウンドにわたって議論しました。"
        "以下の議論の流れを踏まえ、合意点・残課題・結論を整理してください。\n\n"
        + "\n".join(
            f"{'提案者' if i % 4 in (1, 2) else '批評家'}: {m['content']}"
            for i, m in enumerate(history)
            if m["role"] == "assistant"
        )
    )

    summary_messages = [{"role": "user", "content": summary_prompt}]
    summary_text = call_agent(client, "summarizer", summary_messages)

    print(f"【{AGENTS['summarizer']['name']}】")
    print(summary_text)
    print(f"\n{'='*60}\n")


# ─── CLI entry point ──────────────────────────────────────────────────────────


def main() -> None:
    parser = argparse.ArgumentParser(description="Multi-agent discussion loop with Claude")
    parser.add_argument("--topic", "-t", type=str, default="", help="議題（省略時は対話入力）")
    parser.add_argument("--rounds", "-r", type=int, default=3, help="ラウンド数（デフォルト: 3）")
    args = parser.parse_args()

    if not os.environ.get("ANTHROPIC_API_KEY"):
        print("エラー: 環境変数 ANTHROPIC_API_KEY が設定されていません。", file=sys.stderr)
        sys.exit(1)

    topic = args.topic.strip()
    if not topic:
        topic = input("議題を入力してください: ").strip()
    if not topic:
        print("議題が入力されませんでした。終了します。")
        sys.exit(0)

    run_discussion(topic=topic, rounds=args.rounds)


if __name__ == "__main__":
    main()
