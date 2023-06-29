from typing import Union
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse

app = FastAPI()


@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    html_content =  """
        <html>
            <head>
                <title>T.P. Final</title>
            </head>
            <body>
                <h1>Bienvenido a nuestra  página web</h1>
                <p>Esta es una página web creada con FastAPI.</p>
                <form action="/name" method="post">
                    <label for="name">Ingrese su nombre:</label><br>
                    <input type="text" id="name" name="name"><br><br>
                    <input type="submit" value="Enviar">
                </form>
             </body>
        </html>
 """
    return HTMLResponse(content=html_content, status_code=200)

@app.post("/name", response_class=HTMLResponse)
async def read_item(request: Request):
    form_data = await request.form()
    name = form_data["name"]
    html_content = f"""
        <html>
            <head>
                <title>T.P. Final</title>
            </head>
            <body>
                <h2>Bienvenido {name} a nuestra  página web</h2>
            </body>
        </html>
    """
    return HTMLResponse(content=html_content, status_code=200)
