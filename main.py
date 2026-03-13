import yt_dlp
from pyrogram import Client, filters
from pytgcalls import PyTgCalls
from pytgcalls.types.input_stream import AudioPiped
from pytgcalls.types.input_stream.quality import HighQualityAudio

# CONFIG
API_ID = 123456
API_HASH = "YOUR_API_HASH"
STRING_SESSION = "YOUR_STRING_SESSION"

# START CLIENT
app = Client(
    "userbot",
    api_id=API_ID,
    api_hash=API_HASH,
    session_string=STRING_SESSION
)

call = PyTgCalls(app)


# JOIN VC
@app.on_message(filters.command("join", ".") & filters.me)
async def join_vc(client, message):
    chat_id = message.chat.id
    try:
        await call.join_group_call(
            chat_id,
            AudioPiped("https://files.catbox.moe/3x8k1p.mp3")
        )
        await message.reply("✅ Joined Voice Chat")
    except Exception as e:
        await message.reply(str(e))


# PLAY MUSIC
@app.on_message(filters.command("play", ".") & filters.me)
async def play_music(client, message):

    if len(message.command) < 2:
        return await message.reply("Usage: `.play song name`")

    query = message.text.split(None, 1)[1]

    ydl_opts = {
        "format": "bestaudio",
        "noplaylist": True
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(f"ytsearch:{query}", download=False)["entries"][0]
        url = info["url"]

    await call.join_group_call(
        message.chat.id,
        AudioPiped(
            url,
            HighQualityAudio(),
        ),
    )

    await message.reply(f"🎵 Playing: {info['title']}")


# STOP VC
@app.on_message(filters.command("stop", ".") & filters.me)
async def stop_vc(client, message):
    try:
        await call.leave_group_call(message.chat.id)
        await message.reply("⏹ VC Stopped")
    except:
        await message.reply("❌ No active VC")


# LEAVE VC
@app.on_message(filters.command("leave", ".") & filters.me)
async def leave_vc(client, message):
    try:
        await call.leave_group_call(message.chat.id)
        await message.reply("👋 Left VC")
    except:
        await message.reply("❌ Not in VC")


# START BOT
app.start()
call.start()

print("Userbot VC Started")

import asyncio
asyncio.get_event_loop().run_forever()
