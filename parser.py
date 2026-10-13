import asyncio
import os
from dotenv import load_dotenv
from telethon import TelegramClient
from telethon.tl.functions.contacts import SearchRequest
from telethon.tl.types import Channel

# Load environment variables
if os.path.exists("kol.env"):
    load_dotenv("kol.env")
else:
    load_dotenv()

API_ID = int(os.getenv("API_ID", 0))
API_HASH = os.getenv("API_HASH", "")

KEYWORDS_FILE = "keywords.txt"
OUTPUT_FILE = "found_chats.txt"
MIN_MEMBERS = 100


def load_keywords():
    """Loads search keywords from file or returns default placeholders."""
    if os.path.exists(KEYWORDS_FILE):
        with open(KEYWORDS_FILE, "r", encoding="utf-8") as f:
            keywords = [line.strip() for line in f if line.strip()]
            if keywords:
                return keywords
    # Default fallback keywords
    return [
        "crypto chat",
        "freelance jobs",
        "marketing discussion",
        "community chat",
    ]


async def search_chats():
    if not API_ID or not API_HASH:
        print("❌ Error: API_ID and API_HASH must be set in .env file!")
        return

    keywords = load_keywords()
    async with TelegramClient("parser_session", API_ID, API_HASH) as client:
        existing_chats = set()

        if os.path.exists(OUTPUT_FILE):
            with open(OUTPUT_FILE, "r", encoding="utf-8") as f:
                existing_chats = {line.strip() for line in f if line.strip()}

        print(f"🔍 Starting search for {len(keywords)} keyword(s)...\n")

        for keyword in keywords:
            print(f"[*] Querying: '{keyword}'")
            try:
                result = await client(SearchRequest(q=keyword, limit=50))

                for chat in result.chats:
                    if isinstance(chat, Channel) and chat.megagroup:
                        username = f"@{chat.username}" if chat.username else None

                        if username and username not in existing_chats:
                            raw_members = getattr(chat, "participants_count", 0)
                            if raw_members is None:
                                try:
                                    full_chat = await client.get_entity(chat)
                                    raw_members = getattr(
                                        full_chat, "participants_count", 0
                                    )
                                except Exception:
                                    raw_members = 0

                            members = raw_members or 0

                            if members >= MIN_MEMBERS:
                                print(
                                    f"  [+] Found group: {username} ({members} members)"
                                )
                                existing_chats.add(username)

                                with open(OUTPUT_FILE, "a", encoding="utf-8") as f:
                                    f.write(f"{username}\n")

            except Exception as e:
                print(f"  [!] Search error for '{keyword}': {e}")

            await asyncio.sleep(4)

        print(
            f"\n✅ Search complete. Total unique chats saved in {OUTPUT_FILE}: {len(existing_chats)}"
        )


if __name__ == "__main__":
    asyncio.run(search_chats())