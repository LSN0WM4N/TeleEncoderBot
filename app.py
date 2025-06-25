import os
import time
import asyncio
from pyrogram import filters
from pyrogram.client import Client
from pyrogram.types import Message
import dotenv
from pathlib import Path

from modules import *
from texts import *
from web import *

dotenv.load_dotenv()

API_ID = os.getenv("API_ID", '') 
API_HASH = os.getenv("API_HASH", '') 
BOT_TOKEN = os.getenv("BOT_TOKEN", '') 

app = Client(
    "video_to_h265_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

t = es # Change between es and en

@app.on_message(filters.video | filters.document)
async def handle_video(client: Client, message: Message):    
    if message.document and not message.document.mime_type.startswith('video/'):
        await message.reply(t.bot_error_wrong_file_type)
        return
        
    status_msg = await message.reply(t.bot_downloading)

    try:    
        video_path = await safe_download(message, status_msg)

        original_name = Path(video_path).stem
        output_path = get_unique_filename(
            "downloads",
            f"{original_name}_h265",
            "mp4"
        )
        
        await status_msg.edit(t.bot_converting)
        success = convert_to_h265(video_path, output_path)
        
        if not success:
            await status_msg.edit(t.bot_error_while_converting)
            return
                
        await status_msg.edit(t.bot_uploading_converted_video)
        
        file_size = os.path.getsize(output_path)
        if file_size > 2 * GB:  
            await status_msg.edit(t.bot_error_file_to_big)
        else:
            await message.reply_video(
                video=output_path,
                caption="✅ Video convertido a H.265 (HEVC)"
            )
            await status_msg.delete()
        
    except Exception as e:
        print(f"[-] Error en handle_video: {str(e)}")
        await status_msg.edit(t.bot_error_while_processing)
    finally:
        
        if 'video_path' in locals() and os.path.exists(video_path): # type: ignore
            os.remove(video_path) # type: ignore
        if 'output_path' in locals() and os.path.exists(output_path): # type: ignore
            os.remove(output_path) # type: ignore

@app.on_message(filters.command("start"))
async def start(client: Client, message: Message):
    await message.reply(t.bot_command_start)

@app.on_message(filters.command("help"))
async def help(client: Client, message: Message):
    await message.reply(t.bot_command_help)

async def main():
    await asyncio.gather(
        app.start(),
        web_server()
    )

if __name__ == "__main__":
    print("[+] Iniciando el bot...")
    
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(main())
        loop.run_forever()
    except KeyboardInterrupt:
        print("Deteniendo el bot...")
    finally:
        loop.run_until_complete(app.stop())
        loop.close()
        print("Bot detenido correctamente")