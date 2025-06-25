import math
import time

async def progress_callback(current, total, message, status_msg, start_time):
    elapsed_time = time.time() - start_time
    speed = current / elapsed_time if elapsed_time > 0 else 0
    
    percent = current * 100 / total
    
    if speed > 0:
        remaining_time = (total - current) / speed
        remaining_str = f"Tiempo restante: {humanize_time(remaining_time)}"
    else:
        remaining_str = "Calculando..."
    
    downloaded_size = humanize_size(current)
    total_size = humanize_size(total)
    speed_str = humanize_size(speed) + "/s" if speed > 0 else "0 B/s"
    
    progress_bar = create_progress_bar(percent)
    
    text = (
        f"📥 **Descargando...**\n\n"
        f"**Progreso:** {progress_bar} {percent:.1f}%\n"
        f"**Descargado:** {downloaded_size} / {total_size}\n"
        f"**Velocidad:** {speed_str}\n"
        f"**{remaining_str}**"
    )
    
    if current == total or int(percent) % 5 == 0 or elapsed_time % 5 < 0.1:
        try:
            await status_msg.edit(text)
        except Exception as e:
            print(f"Error al actualizar progreso: {str(e)}")

def humanize_size(size_bytes):
    if size_bytes == 0:
        return "0 B"
    size_name = ("B", "KB", "MB", "GB", "TB")
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    return f"{s} {size_name[i]}"

def humanize_time(seconds):
    if seconds < 60:
        return f"{int(seconds)} segundos"
    minutes, seconds = divmod(seconds, 60)
    if minutes < 60:
        return f"{int(minutes)} minutos {int(seconds)} segundos"
    hours, minutes = divmod(minutes, 60)
    return f"{int(hours)} horas {int(minutes)} minutos"

def create_progress_bar(percent, length=20):
    completed = int(length * percent / 100)
    remaining = length - completed
    return "[" + "█" * completed + "░" * remaining + "]"
