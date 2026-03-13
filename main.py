import asyncio
import yt_dlp

from pyrogram import Client, filters
from pytgcalls import PyTgCalls
from pytgcalls.types.input_stream import AudioPiped
from pytgcalls.types.input_stream.quality import HighQualityAudio


# CONFIG
API_ID = 33603336
API_HASH = "c9683a8ec3b886c18219f650fc8ed429"
STRING_SESSION = "BQIAvwgAtGpTYJxvUNp8rbi2VNdfNGw-foSWWvDtrWSVnLbKeor1FcHdS2DO3WAwKRUHYT9NyJGuBAIjd9cYSh0JGW7SZjxsMTs0xEWFeU7dxKhHatLzbjhIA8kUOxWj2chH_ags_7fIToe7_LFolcHFbdJhCKAuStVEV4bUXvn43vmALgKi87JQHAId5p9xB7atUNHxMebmAOq6JqABdoBCdtUJC7tEov8GBF0a1C4r8WE8wKoSp5vDjcu7mRIJrUcQ17LMHYY6ACErur_iH3zN2Ny7Nd3VYyIu7Fk7VfeErEZlw-EoNvB89m_e_KYWE3E6ITu-vAtHeTAMG_cDo771-c7GAwAAAAIAgPwVAA"


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
async def join_vc(_, message):

    chat_id = message.chat.id

    try:
        await call.join_group_call(chat_id, AudioPiped("silence.mp3"))
        await message.reply("✅ Joined Voice Chat")

    except:
        await message.reply("⚠ Already in Voice Chat")


# PLAY MUSIC
@app.on_message(filters.command("play", ".") & filters.me)
async def play_music(_, message):

    chat_id = message.chat.id

    # REPLY AUDIO
    if message.reply_to_message:

        audio = message.reply_to_message.audio or message.reply_to_message.voice

        if not audio:
            return await message.reply("❌ Reply to an audio file")

        file = await message.reply_to_message.download()

        try:
            await call.change_stream(
                chat_id,
                AudioPiped(file, HighQualityAudio())
            )
        except:
            await call.join_group_call(
                chat_id,
                AudioPiped(file, HighQualityAudio())
            )

        return await message.reply("🎵 Playing replied audio")


    # YOUTUBE / SEARCH
    if len(message.command) < 2:
        return await message.reply("Usage: `.play song name or url`")

    query = message.text.split(None, 1)[1]

    ydl_opts = {
        "format": "bestaudio",
        "quiet": True
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(f"ytsearch:{query}", download=False)["entries"][0]

    url = info["url"]
    title = info["title"]

    try:
        await call.change_stream(
            chat_id,
            AudioPiped(url, HighQualityAudio())
        )

    except:
        await call.join_group_call(
            chat_id,
            AudioPiped(url, HighQualityAudio())
        )

    await message.reply(f"🎵 Playing: {title}")


# STOP MUSIC
@app.on_message(filters.command("stop", ".") & filters.me)
async def stop_music(_, message):

    try:
        await call.change_stream(
            message.chat.id,
            AudioPiped("silence.mp3")
        )

        await message.reply("⏹ Music Stopped")

    except:
        await message.reply("❌ Nothing Playing")


# LEAVE VC
@app.on_message(filters.command("leave", ".") & filters.me)
async def leave_vc(_, message):

    try:
        await call.leave_group_call(message.chat.id)
        await message.reply("👋 Left Voice Chat")

    except:
        await message.reply("❌ Not in VC")


# START BOT
app.start()
call.start()

print("VC USERBOT STARTED")

asyncio.get_event_loop().run_forever()
