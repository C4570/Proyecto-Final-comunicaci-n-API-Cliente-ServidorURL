
@app.get("/change/{recipe_name}", response_class=HTMLResponse)
async def edit_recipe_form(request: Request, recipe_name: str):
    recipe = search_recipe(recipe_name)
    if recipe:
        ingredients = ", ".join(recipe["ingredients"])
        steps = ", ".join(recipe["steps"])
        nutrients = ", ".join(str(value) for value in recipe["nutrients"].values())
        times = ", ".join(str(value) for value in recipe["times"].values())
        html_content = f'''
            <html>
                <head>
                    <title>Modificar Receta</title>
                </head>
                <body>
                    <h1>Modificar Receta</h1>
                    <form action="/change/{recipe_name}" method="post">
                        <input type="hidden" name="id" value="{recipe["id"]}">
                        URL:<br><input type="text" name="url" value="{recipe["url"]}"><br><br>
                        Imagen:<br><input type="text" name="image" value="{recipe["image"]}"><br><br>
                        Nombre:<br><input type="text" name="name" value="{recipe["name"]}"><br><br>
                        Descripción:<br><input type="text" name="description" value="{recipe["description"]}"><br><br>
                        Autor:<br><input type="text" name="author" value="{recipe["author"]}"><br><br>
                        Rattings:<br><input type="number" name="rattings" value="{recipe["rattings"]}"><br><br>
                        Ingredientes (separados por comas):<br><input type="text" name="ingredients" value="{ingredients}"><br><br>
                        Pasos (separados por comas):<br><input type="text" name="steps" value="{steps}"><br><br>
                        Nutrientes (kcal, fat, saturates, carbs, sugars, fibre, protein, salt):<br><input type="text" name="nutrients" value="{nutrients}"><br><br>
                        Tiempos (Preparación, Cocción):<br><input type="text" name="times" value="{times}"><br><br>
                        Porciones:<br><input type="number" name="serves" value="{recipe["serves"]}"><br><br>
                        Dificultad:<br><input type="text" name="difficult" value="{recipe["difficult"]}"><br><br>
                        Vote count:<br><input type="number" name="vote_count" value="{recipe["vote_count"]}"><br><br>
                        Subcategoría:<br><input type="text" name="subcategory" value="{recipe["subcategory"]}"><br><br>
                        Tipo de plato:<br><input type="text" name="dish_type" value="{recipe["dish_type"]}"><br><br>
                        Categoría principal:<br><input type="text" name="maincategory" value="{recipe["maincategory"]}"><br><br>
                        <input type="submit" value="Guardar Cambios">
                    </form>
                </body>
            </html>
        '''
    else:
        html_content = f'''
            <html>
                <head>
                    <title>Modificar Receta</title>
                </head>
                <body>
                    <h2>No se encontró una receta con el nombre '{recipe_name}'</h2>
                </body>
            </html>
        '''
    return HTMLResponse(content=html_content, status_code=200)

@app.post("/change/{recipe_name}", response_class=HTMLResponse)
async def update_recipe_handler(request: Request, recipe_name: str):
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