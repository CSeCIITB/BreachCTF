import argparse
import datetime
import os
import re
import requests
import sqlite3
import time


# Announcement message can be changed here
# {challenge} and {user} are replaced with the challenge title and username
ANNOUNCEMENT = ":drop_of_blood: First blood for **{challenge}** goes to **{user}**! :drop_of_blood:"


def log(msg: str) -> None:
    now = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
    print(f"{now}\t{msg}")


def setup_database(db_path: str) -> sqlite3.Connection:
    log(f"Connecting to sqlite3 db at '{db_path}'...")
    db = sqlite3.connect(db_path)

    log("Creating table of announced solves if not existing...")
    db.execute("CREATE TABLE IF NOT EXISTS announced_solves (id INTEGER PRIMARY KEY AUTOINCREMENT, challenge_id INTEGER, solver_id INTEGER)")

    return db


def get_announced_solves(db: sqlite3.Connection) -> list[int]:
    rows = db.execute("SELECT challenge_id FROM announced_solves").fetchall()
    return [row[0] for row in rows]


def get_first_blood(session: requests.Session, challenge_id: int) -> str:
    return session.get(
        f"{session.base_url}/api/v1/challenges/{challenge_id}/solves",
        timeout=5
    ).json().get("data", [None])[0]


def get_challenges(session: requests.Session, solved_only: bool=False) -> list[str]:
    challenges = session.get(f"{session.base_url}/api/v1/challenges", timeout=5).json().get("data", [])

    if solved_only:
        challenges = [c for c in challenges if c.get("solves", 0) > 0]

    return challenges


def announce_new_solves(db: sqlite3.Connection, session: requests.Session, webhook: str, announced: list[int]) -> None:
    solved_challenges = get_challenges(session, solved_only=True)
    for challenge in solved_challenges:
        if challenge["id"] in announced:
            continue

        first_blood = get_first_blood(session, challenge["id"])
        if first_blood is None:
            continue

        log(f"Announcing first blood for {challenge['name']} by {first_blood['name']}")
        res = session.post(webhook, json={
            "content": ANNOUNCEMENT.format(challenge=challenge["name"], user=first_blood["name"])
        }, timeout=5)

        if res.status_code in [200, 204]:
            db.execute(
                "INSERT INTO announced_solves (challenge_id, solver_id) VALUES (?, ?)",
                (challenge["id"], first_blood["account_id"])
            )
            db.commit()

            announced.append(challenge["id"])


def parse_args() -> argparse.Namespace:
    # Parse command line args
    parser = argparse.ArgumentParser(
        prog="First Blood Announcer",
        description="Announce CTF first bloods from CTFd on Discord",
        formatter_class=argparse.RawTextHelpFormatter,
        epilog="""Note: First bloods made before running the bot are skipped unless adding --existing.

Webhook, CTFd URL and CTFd access token are all required, either through command line args
or environment variables (WEBHOOK_URL, CTFD_URL, CTFD_ACCESS_TOKEN) - possibly in a .env file.

An existing DB can be specified with --db. If the DB does not exist, a new is created."""
    )
    parser.add_argument("--webhook", help="Discord webhook URL")
    parser.add_argument("--ctfd", help="CTFd URL")
    parser.add_argument("--token", help="CTFd access token")
    parser.add_argument("--existing", action="store_true", help="Announce existing solves")
    parser.add_argument("--interval", type=int, default=5, help="Refresh interval in seconds (default: %(default)s)")
    parser.add_argument("--db", default="solves.db", help="Database path (default: %(default)s)")

    args = parser.parse_args()

    try:
        # Load envvars from .env if possible
        from dotenv import load_dotenv
        load_dotenv()
    except ModuleNotFoundError:
        print("Module 'dotenv' not found, skipping potential .env-file")

    # Cmd line args override environment
    args.webhook = args.webhook or os.getenv("WEBHOOK_URL")
    args.ctfd = args.ctfd or os.getenv("CTFD_URL")
    args.token = args.token or os.getenv("CTFD_ACCESS_TOKEN")

    # Check required args
    if args.webhook is None:
        raise parser.error("--webhook option or WEBHOOK_URL envvar is required")

    if args.ctfd is None:
        raise parser.error("--ctfd option or CTFD_URL envvar is required")

    if args.token is None:
        raise parser.error("--token option or CTFD_ACCESS_TOKEN envvar is required")

    # Validate args
    if not re.match(r"^https?://discord.com/api/webhooks/", args.webhook) or requests.get(args.webhook).status_code != 200:
        raise parser.error("Invalid webhook URL")

    if not re.match(r"^https?://", args.ctfd) or requests.get(args.ctfd).status_code != 200:
        raise parser.error("Invalid CTFd URL")

    with requests.Session() as s:
        s.headers.update({
            "Content-Type": "application/json",
            "Authorization": f"Token {args.token}"
        })

        s.base_url = args.ctfd.strip("/")

        if s.get(f"{s.base_url}/api/v1/challenges", timeout=5).status_code != 200:
            raise parser.error("Unauthorized - invalid CTFd URL or access token")

        args.session = s

    return args


def main():
    args = parse_args()

    log("Starting CTFd Discord First Blood Announcer...")
    db = setup_database(args.db)
    announced = get_announced_solves(db)

    # Skip existing but not yet announced CTFd solves
    if not args.existing:
        log("Skipping existing first bloods...")
        solved = get_challenges(args.session, solved_only=True)
        announced.extend([s["id"] for s in solved])
    else:
        log("Announcing existing first bloods...")

    log("Bot running, waiting for first bloods...")

    while True:
        try:
            log("Fetching new solves...")
            announce_new_solves(db, args.session, args.webhook, announced)
        except requests.exceptions.ConnectionError:
            log("Connection failed, retrying...")
        except requests.exceptions.Timeout:
            log("Request timed out, retrying...")

        time.sleep(args.interval)


if __name__ == "__main__":
    main()
