import asyncio
import os
import random
from dotenv import load_dotenv
from telethon import TelegramClient, errors
from telethon.tl.functions.channels import JoinChannelRequest

# Load environment variables
if os.path.exists("kol.env"):
    load_dotenv("kol.env")
else:
    load_dotenv()

API_ID = int(os.getenv("API_ID", 0))
API_HASH = os.getenv("API_HASH", "")

CHATS_FILE = "found_chats.txt"
TEMPLATES_FILE = "templates.txt"

DEFAULT_TEMPLATES = [
    "🚀 **Welcome to our project!**\n\nCheck out the latest updates and announcements in our main channel 👇\nhttps://t.me/your_channel_here",
    "💡 **Looking for new opportunities?**\n\nJoin our growing community today! Details in our channel 👇\nhttps://t.me/your_channel_here",
]


def load_chats():
    """Reads target chats from found_chats.txt"""
    if os.path.exists(CHATS_FILE):
        with open(CHATS_FILE, "r", encoding="utf-8") as f:
            chats = [line.strip().replace("@", "") for line in f if line.strip()]
            if chats:
                return chats
    return []


def load_templates():
    """Loads post templates from templates.txt separated by '---'"""
    if os.path.exists(TEMPLATES_FILE):
        with open(TEMPLATES_FILE, "r", encoding="utf-8") as f:
            content = f.read()
            templates = [
                t.strip() for t in content.split("---") if t.strip()
            ]
            if templates:
                return templates
    return DEFAULT_TEMPLATES


def remove_chat_from_file(chat_to_remove):
    """Removes restricted or invalid chat from found_chats.txt"""
    chats = load_chats()
    updated_chats = [c for c in chats if c.lower() != chat_to_remove.lower()]
    with open(CHATS_FILE, "w", encoding="utf-8") as f:
        for c in updated_chats:
            f.write(f"@{c}\n")


client = TelegramClient("poster_session", API_ID, API_HASH)


async def main():
    if not API_ID or not API_HASH:
        print("❌ Error: API_ID and API_HASH must be configured in .env file!")
        return

    await client.start()
    print("🟢 AutoPromoter poster module active.")

    while True:
        target_chats = load_chats()
        templates = load_templates()

        if not target_chats:
            print("❌ Target chat list is empty. Exiting...")
            break

        random.shuffle(target_chats)
        total_chats = len(target_chats)

        print(f"\n🚀 Starting broadcast round across {total_chats} chats...")

        for index, chat in enumerate(target_chats, start=1):
            try:
                # Attempt auto-join
                try:
                    await client(JoinChannelRequest(chat))
                    await asyncio.sleep(2)
                except Exception:
                    pass

                text = random.choice(templates)
                await client.send_message(
                    chat, text, parse_mode="md", link_preview=False
                )
                print(f"[{index}/{total_chats}] ✅ Message delivered to: @{chat}")

                # Random delay between posts (35–60 seconds)
                delay = random.randint(35, 60)
                await asyncio.sleep(delay)

            except errors.ChatWriteForbiddenError:
                print(f"⛔️ Posting forbidden in @{chat}. Removing from target list...")
                remove_chat_from_file(chat)

            except errors.FloodWaitError as e:
                print(f"⚠️ Telegram FloodWait restriction! Sleeping for {e.seconds} seconds.")
                await asyncio.sleep(e.seconds + 5)

            except errors.PeerFloodError:
                print("❌ PeerFlood detected! Entering 2-hour sleep mode.")
                await asyncio.sleep(7200)

            except Exception as e:
                print(f"❌ Delivery failed for @{chat}: {e}")
                if "You can't write in this chat" in str(e):
                    print(f"🗑 Removing restricted chat @{chat}...")
                    remove_chat_from_file(chat)
                await asyncio.sleep(5)

        # Round delay (15–20 minutes)
        round_delay = random.randint(900, 1200)
        print(f"\n🏁 Round complete. Next round starting in {round_delay // 60} minutes...\n")
        await asyncio.sleep(round_delay)


with client:
    client.loop.run_until_complete(main())