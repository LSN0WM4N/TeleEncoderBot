import ffmpeg
from .logs import setup_logging

personal_logger = setup_logging()

def convert_to_h265(input_file: str, output_file: str) -> bool:
    personal_logger.debug(f'[Debug] >> Converting {input_file} to {output_file}')
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
        personal_logger.error(f"[-] Error al convertir el video: {e.stderr.decode()}")
        return False
    except Exception as e:
        personal_logger.error(f"[-] Error inesperado: {str(e)}")
        return False