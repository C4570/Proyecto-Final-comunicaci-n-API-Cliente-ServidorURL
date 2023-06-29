from typing import Union
from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()


@app.get("/", response_class=HTMLResponse)
async def read_root():
    return """
        <html>
            <head>
                <title>T.P. Final</title>
            </head>
            <body>
                <h1>Bienvenido a nuestra  página web</h1>
                <p>Esta es una página web creada con FastAPI.</p>
            </body>
        </html>
    """
