import os
from pyrogram import Client, filters
from pyrogram.types import Message
import ffmpeg
import dotenv

dotenv.load_dotenv()

API_ID = os.getenv("API_ID")
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")

app = Client(
    "video_to_h265_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

def convert_to_h265(input_file: str, output_file: str) -> bool:
    try:
        (
            ffmpeg
            .input(input_file)
            .output(
                output_file,
                vcodec='libx265',
                crf=28,  
                preset='medium',  
                acodec='copy'  
            )
            .overwrite_output()
            .run(quiet=True)
        )
        return True
    except ffmpeg.Error as e:
        print(f"[-] Error al convertir el video: {e.stderr.decode()}")
        return False
    except Exception as e:
        print(f"[-] Error inesperado: {str(e)}")
        return False

@app.on_message(filters.video | filters.document)
async def handle_video(client: Client, message: Message):
    user_id = message.from_user.id
    
    if message.document and not message.document.mime_type.startswith('video/'):
        await message.reply("Por favor envía un archivo de video.")
        return
        
    status_msg = await message.reply("📥 Descargando tu video...")
    
    try:    
        video_path = await message.download()
        
        base_name = os.path.splitext(video_path)[0]
        output_path = f"{base_name}_h265.mp4"
        
        await status_msg.edit("🔄 Convirtiendo a H.265...")
        success = convert_to_h265(video_path, output_path)
        
        if not success:
            await status_msg.edit("❌ Error al convertir el video.")
            return
                
        await status_msg.edit("📤 Subiendo video convertido...")
        
        file_size = os.path.getsize(output_path)
        if file_size > 1024 * 1024 * 1024:  
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
        
        if 'video_path' in locals() and os.path.exists(video_path):
            os.remove(video_path)
        if 'output_path' in locals() and os.path.exists(output_path):
            os.remove(output_path)

@app.on_message(filters.command("start"))
async def start(client: Client, message: Message):
    await message.reply(
        "👋 Hola! Soy un bot que convierte videos a H.265 (HEVC).\n\n"
        "Simplemente envíame un video y lo convertiré al códec más eficiente."
    )

if __name__ == "__main__":
    print("[+] Iniciando el bot...")
    app.run()