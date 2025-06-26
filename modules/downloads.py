import os
import re
import time
import shutil
from urllib.parse import unquote
from pathlib import Path
from pyrogram.types import Message

from .progress import progress_callback
from .logs import setup_logging

personal_logger = setup_logging()

def sanitize_filename(filename: str) -> str:
    clean_name = unquote(filename)
    clean_name = clean_name.replace(" ", "_")
    clean_name = re.sub(r'[\\/*?:"<>|]', "", clean_name)
    clean_name = clean_name[:200]
    
    return clean_name

def get_unique_filename(directory: str, base_name: str, extension: str) -> str:

    os.makedirs(directory, exist_ok=True)
    
    counter = 1
    while True:
        if counter == 1:
            filename = f"{base_name}.{extension}"
        else:
            filename = f"{base_name}_{counter}.{extension}"
        
        full_path = os.path.join(directory, filename)
        if not os.path.exists(full_path):
            return full_path
        counter += 1

async def safe_download(message: Message, status_msg: Message) -> str:
    try:
        temp_dir = "downloads"
        os.makedirs(temp_dir, exist_ok=True)

        if message.video:
            original_name = message.video.file_name or "video"
        elif message.document:
            original_name = message.document.file_name or "file"
        else:
            original_name = "file"
        
        clean_base = sanitize_filename(Path(original_name).stem)
        extension = Path(original_name).suffix[1:] or "mp4"
        
        dest_path = get_unique_filename(temp_dir, clean_base, extension)
        
        personal_logger.debug(f'[Debug] >> dest+path: {dest_path}')

        download_path = await message.download(
            file_name=dest_path,
            progress=progress_callback,
            progress_args=(message, status_msg, time.time())
        )
        
        return download_path
        
    except Exception as e:
        personal_logger.error(f"Error en safe_download: {str(e)}")
        raise

