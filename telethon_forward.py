# telethon_forward.py
import os, asyncio
from telethon import TelegramClient, events

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
SESSION_NAME = "my_session"

# الأشخاص اللي عايز تراقبهم
WATCH_PEERS = ["@Conutflav", "@Maryamabosaif"]  # usernames أو IDs
# المكان اللي الرسائل تتبعت له
TARGET_CHAT = "me"  # أو "@username" أو chat_id رقمي

client = TelegramClient(SESSION_NAME, API_ID, API_HASH)

@client.on(events.NewMessage(incoming=True))
async def handler(event):
    sender = await event.get_sender()
    sender_username = getattr(sender, 'username', None)
    sender_id = sender.id if sender else None

    # تحقق إذا المرسل ضمن المراقبة
    if not any(str(w) in [str(sender_username), str(sender_id)] for w in WATCH_PEERS):
        return

    msg_text = event.message.text or "<media>"
    print(f"📩 Message from {sender_username or sender_id}: {msg_text[:40]}...")

    try:
        await client.copy_message(TARGET_CHAT, event.message.chat_id, event.message.id)
        print("✅ Copied to target")
    except Exception as e:
        print("❌ Copy failed:", e)
        try:
            await client.forward_messages(TARGET_CHAT, event.message)
            print("✅ Forwarded as fallback")
        except Exception as e2:
            print("❌ Forward failed:", e2)

async def main():
    print("🚀 Starting Telethon client...")
    await client.start()
    me = await client.get_me()
    print(f"✅ Logged in as {me.first_name} ({me.username or me.id})")
    await client.run_until_disconnected()

if __name__ == "__main__":
    asyncio.run(main())
