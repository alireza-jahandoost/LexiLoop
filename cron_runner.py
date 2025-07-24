import asyncio
import os
from datetime import datetime
import subprocess
from dotenv import load_dotenv

load_dotenv()

# Load job hours from .env
JOB_HOURS = {
    "maintain": int(os.getenv("MAINTAIN_HOUR", -1)),
    "check": int(os.getenv("CHECK_HOUR", -1)),
    "publish_vocab": int(os.getenv("PUBLISH_VOCAB_HOUR", -1)),
    "publish_false_friend": int(os.getenv("PUBLISH_FALSE_HOUR", -1)),
    "publish_grammar": int(os.getenv("PUBLISH_GRAMMAR_HOUR", -1)),
}

COMMANDS = {
    "maintain": "python main.py maintain",
    "check": "python main.py check",
    "publish_vocab": "python main.py publish --type vocab",
    "publish_false_friend": "python main.py publish --type false_friend",
    "publish_grammar": "python main.py publish --type grammar",
}

async def run_command(command: str):
    print(f"🕒 Running: {command}")
    process = await asyncio.create_subprocess_shell(command)
    await process.communicate()

async def main():
    current_hour = datetime.utcnow().hour
    print(f"🔎 Current UTC hour: {current_hour}")

    for job, hour in JOB_HOURS.items():
        if hour == current_hour:
            command = COMMANDS[job]
            await run_command(command)

if __name__ == "__main__":
    asyncio.run(main())
