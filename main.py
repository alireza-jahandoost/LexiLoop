import argparse
import asyncio
from commands.generate import run_generate
from commands.publish import run_publish

def main():
    parser = argparse.ArgumentParser(description="LexiLoop CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # generate command (sync)
    gen_parser = subparsers.add_parser("generate", help="Generate a new post")
    gen_parser.add_argument("--type", "-t", type=str, default="vocab", help="Type of post to generate")
    gen_parser.add_argument("--count", "-c", type=int, default=1, help="Number of posts to generate")
    gen_parser.set_defaults(func=run_generate)

    # publish command (async)
    pub_parser = subparsers.add_parser("publish", help="Publish an unpublished post to Telegram")
    pub_parser.add_argument("--type", "-t", type=str, default="vocab", help="Type of post to publish")
    pub_parser.set_defaults(func=run_publish)

    args = parser.parse_args()

    # Handle async vs sync
    if asyncio.iscoroutinefunction(args.func):
        asyncio.run(args.func(args))
    else:
        args.func(args)

if __name__ == "__main__":
    main()