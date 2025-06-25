import os
import time
import asyncio
from pyrogram import filters
from pyrogram.client import Client
from pyrogram.types import Message
import dotenv
from pathlib import Path


from modules import *
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

@app.on_message(filters.video | filters.document)
async def handle_video(client: Client, message: Message):    
    if message.document and not message.document.mime_type.startswith('video/'):
        await message.reply("Por favor envía un archivo de video.")
        return
        
    status_msg = await message.reply("📥 Descargando tu video...")

    try:    
        video_path = await safe_download(message, status_msg)

        original_name = Path(video_path).stem
        output_path = get_unique_filename(
            "temp_converted",
            f"{original_name}_h265",
            "mp4"
        )
        
        await status_msg.edit("🔄 Convirtiendo a H.265...")
        success = convert_to_h265(video_path, output_path)
        
        if not success:
            await status_msg.edit("❌ Error al convertir el video.")
            return
                
        await status_msg.edit("📤 Subiendo video convertido...")
        
        file_size = os.path.getsize(output_path)
        if file_size > 2048 * 1024 * 1024:  
            await status_msg.edit("⚠️ El video convertido es demasiado grande para enviar por Telegram.")
        else:
            await message.reply_video(
                video=output_path,
                caption="✅ Video convertido a H.265 (HEVC)"
            )
            await status_msg.delete()
        
    except Exception as e:
        print(f"[-] Error en handle_video: {str(e)}")
        await status_msg.edit("❌ Ocurrió un error al procesar tu video.")
    finally:
        
        if 'video_path' in locals() and os.path.exists(video_path): # type: ignore
            os.remove(video_path) # type: ignore
        if 'output_path' in locals() and os.path.exists(output_path): # type: ignore
            os.remove(output_path) # type: ignore

@app.on_message(filters.command("start"))
async def start(client: Client, message: Message):
    await message.reply(
        "👋 Hola! Soy un bot que convierte videos a H.265 (HEVC).\n\n"
        "Simplemente envíame un video y lo convertiré al códec más eficiente."
    )

@app.on_message(filters.command("help"))
async def help(client: Client, message: Message):
    await message.reply("""
    🤖 *Bot de Conversión a H.265*

    📌 *¿Qué hace este bot?*
    Convierte videos al códec H.265 (HEVC) para reducir su tamaño manteniendo buena calidad.

    🛠 *Cómo usarlo:*
    1. Envíame cualquier video
    2. Espera a que lo procese
    3. Recibe el video convertido

    ⚙️ *Comandos disponibles:*
    /start - Mensaje de bienvenida
    /help - Muestra este mensaje

    ℹ️ *Más información:*
    Visita la página de ayuda en [este enlace](https://teleencoderbot.onrender.com) o consulta la web del bot.
    """
    )

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