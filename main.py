import json
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
import uuid

app = FastAPI()
PATH = "recipes.json"
def update_recipe(updated_recipe: dict):
    with open(PATH, "r") as f:
        recipes = json.load(f)
    for i, recipe in enumerate(recipes):
        if recipe["name"].lower() == updated_recipe["name"].lower():
            recipes[i] = updated_recipe
            break
    with open(PATH, "w") as f:
        json.dump(recipes, f)

def search_recipe(recipe_name: str):
    with open(PATH, "r") as f:
        recipes = json.load(f)
        for recipe in recipes:
            if recipe["name"].lower() == recipe_name.lower():
                return recipe
    return None

def add_recipe(recipe: dict):
    with open(PATH, "r") as f:
        recipes = json.load(f)
    recipes.append(recipe)
    with open(PATH, "w") as f:
        json.dump(recipes, f)
        
@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    html_content =  """
        <html>
    <head>
        <title>T.P. Final</title>
        <style>
            body {
                font-family: Arial, Helvetica, sans-serif;
                margin: 0;
                padding: 0;
            }
            .container {
                max-width: 800px;
                margin: 0 auto;
                padding: 40px 0;
            }
            h1 {
                text-align: center;
                margin-bottom: 40px;
            }
            p {
                text-align: center;
                font-size: 18px;
                margin-bottom: 40px;
            }
            form {
                display: flex;
                flex-direction: column;
                align-items: center;
            }
            label {
                font-size: 18px;
                margin-bottom: 10px;
            }
            input[type="text"] {
                font-size: 18px;
                padding: 10px 15px;
                margin-bottom: 20px;
            }
            input[type="submit"] {
                font-size: 18px;
                padding: 10px 20px;
                cursor: pointer;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Bienvenido a nuestra página web de recetas</h1>
            <p>Esta es una página web creada con FastAPI.</p>
            <form action="/recipes" method="post">
                <label for="name">Ingrese el nombre de la receta:</label><br>
                <input type="text" id="name" name="name"><br><br>
                <input type="submit" value="Enviar">
            </form>
        </div>
     </body>
</html>

 """
    return HTMLResponse(content=html_content, status_code=200)

@app.post("/recipes", response_class=HTMLResponse)
async def read_item(request: Request):
    form_data = await request.form()
    name = form_data["name"]
    recipe = search_recipe(name)
    if recipe:
        ingredients_list = "".join([f"<li>{ingredient}</li>" for ingredient in recipe["ingredients"]])
        html_content = f'''
            <html>
                <head>
                    <title>T.P. Final</title>
                </head>
                <body>
                    <h2>Receta encontrada: {recipe["name"]}</h2>
                    <img src={recipe["image"]} width="500" height="600">
                    <p>Autor: {recipe["author"]}</p>
                    <p>Descripcion: {recipe["description"]}</p>
                    <p>Porciones: {recipe["serves"]}</p>
                    <p>Dificultad: {recipe["difficult"]}</p>
                    <p>Ingredientes: </p>
                    <ul>{ingredients_list}</ul>
                    <p>Instrucciones: {recipe["steps"]}</p>
                    <p>Tiempos:</p>
                    <ul>
                        <li>Preparación: {recipe["times"]["Preparation"]}</li>
                        <li>Cocción: {recipe["times"]["Cooking"]}</li>
                    </ul>
                    <form action="/change/{recipe["name"]}" method="post">  
                            <button>Modificar Receta</button>  
                    </form>
                </body>
            </html>
        '''
    else:
        html_content = f'''
            <html>
                <head>
                    <title>T.P. Final</title>
                </head>
                <body>
                    <h2>Lo siento, no se encontró la receta para {name}</h2>
                </body>
            </html>
        '''
    return HTMLResponse(content=html_content, status_code=200)

@app.get("/add_recipe", response_class=HTMLResponse)
async def create_recipe_from(request: Request):
    html_content = '''
        <html>
            <head>
                <title>Agregar Receta</title>
            </head>
            <body>
                <h1>Agregar Receta</h1>
                    <form action="/add_recipe" method="post">
            URL:<br><input type="text" name="url"><br><br>
            Imagen:<br><input type="text" name="image"><br><br>
            Nombre:<br><input type="text" name="name"><br><br>
            Descripción:<br><input type="text" name="description"><br><br>
            Autor:<br><input type="text" name="author"><br><br>
            Rattings:<br><input type="number" name="rattings"><br><br>
            Ingredientes (separados por comas):<br><input type="text" name="ingredients"><br><br>
            Pasos (separados por comas):<br><input type="text" name="steps"><br><br>
            Nutrientes (kcal, fat, saturates, carbs, sugars, fibre, protein, salt):<br><input type="text" name="nutrients"><br><br>
            Tiempos (Preparación, Cocción):<br><input type="text" name="times"><br><br>
            Porciones:<br><input type="number" name="serves"><br><br>
            Dificultad:<br><input type="text" name="difficult"><br><br>
            Vote count:<br><input type="number" name="vote_count"><br><br>
            Subcategoría:<br><input type="text" name="subcategory"><br><br>
            Tipo de plato:<br><input type="text" name="dish_type"><br><br>
            Categoría principal:<br><input type="text" name="maincategory"><br><br>
            <input type="submit" value="Enviar">
                    </form>
            </body>
        </html>
        '''
    return HTMLResponse(content=html_content, status_code=200)

@app.post("/add_recipe", response_class=HTMLResponse)
async def create_recipe(request: Request):
    form_data = await request.form()
    recipe = {
        "id":  str(uuid.uuid4()),
        "url": form_data["url"],
        "image": form_data["image"],
        "name": form_data["name"],
        "description": form_data["description"],
        "author": form_data["author"],
        "rattings": int(form_data["rattings"]),
        "ingredients": [x.strip() for x in form_data["ingredients"].split(",")],
        "steps": [x.strip() for x in form_data["steps"].split(",")],
        "nutrients": dict(zip(["kcal", "fat", "saturates", "carbs", "sugars", "fibre", "protein", "salt"], [x.strip() for x in form_data["nutrients"].split(",")])),
        "times": dict(zip(["Preparation", "Cooking"], [x.strip() for x in form_data["times"].split(",")])),
        "serves": int(form_data["serves"]),
        "difficult": form_data["difficult"],
        "vote_count": int(form_data["vote_count"]),
        "subcategory": form_data["subcategory"],
        "dish_type": form_data["dish_type"],
        "maincategory": form_data["maincategory"]
    }
    add_recipe(recipe)
    return HTMLResponse(content="<h1>Receta agregada con éxito</h1>", status_code=200)

 #####  Experimental
@app.post("/change/{name}")
async def read_item(name):
    recipe = search_recipe(name)
    if recipe:
        ingredients_list = "".join([f"<li>{ingredient}</li>" for ingredient in recipe["ingredients"]])
        html_content = f'''
            <html>
                <head>
                    <title>T.P. Final</title>
                </head>
                <body>
                    <form action="/change_recipe/" method="post">
                        <input type="hidden" name="id" value={recipe["id"]}>
                        <p>{recipe["url"]}</p>
                        URL Nueva:<br><input type="text" name="url"><br><br>
                        <p>{recipe["image"]}</p>
                        Imagen:<br><input type="text" name="image"><br><br>
                        <p>{recipe["name"]}</p>
                        Nombre:<br><input type="text" name="name"><br><br>
                        <p>{recipe["description"]}</p>
                        Descripción:<br><input type="text" name="description"><br><br>
                        <p>{recipe["author"]}</p>
                        Autor:<br><input type="text" name="author"><br><br>
                        <p>{recipe["rattings"]}</p>
                        Rattings:<br><input type="number" name="rattings"><br><br>
                        <p>{ingredients_list}</p>
                        Ingredientes (separados por comas):<br><input type="text" name="ingredients"><br><br>
                        <p>{recipe["steps"]}</p>
                        Pasos (separados por comas):<br><input type="text" name="steps"><br><br>
                        <p>{recipe["nutrients"]}</p>
                        Nutrientes (kcal, fat, saturates, carbs, sugars, fibre, protein, salt):<br><input type="text" name="nutrients"><br><br>
                        <p>{recipe["times"]}</p>
                        Tiempos (Preparación, Cocción):<br><input type="text" name="times"><br><br>
                        <p>{recipe["serves"]}</p>
                        Porciones:<br><input type="number" name="serves"><br><br>
                        <p>{recipe["difficult"]}</p>
                        Dificultad:<br><input type="text" name="difficult"><br><br>
                        <p>{recipe["vote_count"]}</p>
                        Vote count:<br><input type="number" name="vote_count"><br><br>
                        <p>{recipe["subcategory"]}</p>
                        Subcategoría:<br><input type="text" name="subcategory"><br><br>
                        <p>{recipe["dish_type"]}</p>
                        Tipo de plato:<br><input type="text" name="dish_type"><br><br>
                        <p>{recipe["maincategory"]}</p>
                        Categoría principal:<br><input type="text" name="maincategory"><br><br>
                        <input type="submit" value="Modificar">
                    </form>     
            </html>
        '''
        return HTMLResponse(content=html_content, status_code=200)
    else:
        html_content = f'''
            <html>
                <head>
                    <title>T.P. Final</title>
                </head>
                <body>
                    <h2>Lo siento, no se encontró la receta para {name}</h2>
                </body>
            </html>
        '''
    return HTMLResponse(content=html_content, status_code=200)

@app.post("/change_recipe/", response_class=HTMLResponse)
async def change_recipe(request: Request):
    form_data = await request.form()
    recipe = {
        "id": form_data["id"],
        "url": form_data["url"],
        "image": form_data["image"],
        "name": form_data["name"],
        "description": form_data["description"],
        "author": form_data["author"],
        "rattings": int(form_data["rattings"]),
        "ingredients": [x.strip() for x in form_data["ingredients"].split(",")],
        "steps": [x.strip() for x in form_data["steps"].split(",")],
        "nutrients": dict(zip(["kcal", "fat", "saturates", "carbs", "sugars", "fibre", "protein", "salt"], [x.strip() for x in form_data["nutrients"].split(",")])),
        "times": dict(zip(["Preparation", "Cooking"], [x.strip() for x in form_data["times"].split(",")])),
        "serves": int(form_data["serves"]),
        "difficult": form_data["difficult"],
        "vote_count": int(form_data["vote_count"]),
        "subcategory": form_data["subcategory"],
        "dish_type": form_data["dish_type"],
        "maincategory": form_data["maincategory"]
    }
    update_recipe(recipe)
    return HTMLResponse(content="<h1>Receta modificada con éxito</h1>", status_code=200)

