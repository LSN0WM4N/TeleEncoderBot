from aiohttp import web
import os

WEB_PORT = int(os.getenv("WEB_PORT", 8080)) 

async def web_server():
    app = web.Application()
    app.router.add_get("/", handle_help)
    app.router.add_get("/help", handle_help)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", WEB_PORT)
    await site.start()
    print(f"Servidor web iniciado")

async def handle_help(request):
    help_html = """
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Bot de Conversión a H.265 - Ayuda</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                line-height: 1.6;
                max-width: 800px;
                margin: 0 auto;
                padding: 20px;
                color: #333;
            }
            h1 {
                color: #2c3e50;
                text-align: center;
            }
            .container {
                background-color: #f9f9f9;
                border-radius: 8px;
                padding: 20px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            }
            .command {
                background-color: #e8f4f8;
                padding: 8px 12px;
                border-radius: 4px;
                font-family: monospace;
            }
            .footer {
                margin-top: 30px;
                text-align: center;
                font-size: 0.9em;
                color: #7f8c8d;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🤖 Bot de Conversión a H.265</h1>
            
            <h2>📌 ¿Qué hace este bot?</h2>
            <p>Este bot convierte videos al códec H.265 (HEVC), que ofrece mejor compresión manteniendo alta calidad.</p>
            
            <h2>🛠 Cómo usarlo</h2>
            <ol>
                <li>Envía cualquier video al bot</li>
                <li>Espera a que procese el archivo</li>
                <li>Recibe el video convertido</li>
            </ol>
            
            <h2>⚙️ Comandos disponibles</h2>
            <p><span class="command">/start</span> - Muestra el mensaje de bienvenida</p>
            <p><span class="command">/help</span> - Muestra esta información de ayuda</p>
            
            <h2>ℹ️ Información técnica</h2>
            <ul>
                <li><strong>Formato de salida:</strong> MP4 con códec H.265</li>
                <li><strong>Calidad:</strong> CRF 28 (ajustable)</li>
                <li><strong>Audio:</strong> Copiado sin recompresión</li>
                <li><strong>Tamaño máximo:</strong> 2 GB</li>
            </ul>
            
            <div class="footer">
                <p>Bot desarrollado con Pyrogram y FFmpeg</p>
            </div>
        </div>
    </body>
    </html>
    """
    return web.Response(text=help_html, content_type="text/html")
