from agents.review.post_judge import PostJudgeAgent

if __name__ == "__main__":
    print("🧪 Testing PostJudgeAgent with a malformed vocabulary post...\n")

    # Structured correctly but contains bad grammar and mistakes
    bad_post = {
        "type": "vocab_json",
        "topic": "cibo",
        "content": {
            "topic": "cibo",
            "vocabulary": [
                {
                    "word_it": "pomodori",
                    "meaning_en": "tomatoes",
                    "example_it": "Io mangia pomodori tutti giorni perché loro è salute.",
                    "example_en": "I eat tomatoes every day because they is health.",
                    "emoji": "🍅"
                },
                {
                    "word_it": "pane",
                    "meaning_en": "bread",
                    "example_it": "Il pane è mangiare da molto persone nella mondo.",
                    "example_en": "Bread is eaten by much people in the world.",
                    "emoji": "🍞"
                }
            ]
        },
        "formatted_view": """
cibo

🍅 **pomodori** — tomatoes
🗣️ Io mangia pomodori tutti giorni perché loro è salute.
💬 (I eat tomatoes every day because they is health.)

🍞 **pane** — bread
🗣️ Il pane è mangiare da molto persone nella mondo.
💬 (Bread is eaten by much people in the world.)
""",
        "media": None
    }

    judge = PostJudgeAgent()
    result = judge.judge(bad_post)

    print("🧾 Judgment Result:")
    print(result)

    if result["verdict"] == "reject":
        print("\n❌ Post was rejected as expected.")
        print(f"Reason: {result['reason']}")
    else:
        print("\n⚠️ Unexpected: Post was accepted.")
