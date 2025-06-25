import ffmpeg

def convert_to_h265(input_file: str, output_file: str) -> bool:
    print(f'[Debug] >> Converting {input_file} to {output_file}')
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