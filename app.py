from fastapi import FastAPI, HTTPException, Body, Path, Query
from typing import Annotated
from pydantic import BaseModel, Field

app = FastAPI()

VideojuegoId = Annotated[int, Path(gt=0)]
GeneroBusqueda = Annotated[str, Query(min_length=3)]



class VideoJuegos(BaseModel):
    id: Annotated [int, Field (gt=0, description = "ID del videojuego")]    
    nombre: Annotated [str, Field (min_length=1, description = "Nombre del Videojuego")]
    genero: Annotated [str, Field (min_length=1, description = "Genero del videojuego")]
    precio: Annotated [int, Field (ge=0, description = "Precio del videojuego")]
    


videojuegos = [
    {
        "id": 1,
        "nombre": "Minecraft",
        "genero": "Sandbox",
        "precio": 20
    },
    {
        "id": 2,
        "nombre": "FIFA 25",
        "genero": "Deportes",
        "precio": 60
    },
    {
        "id": 3,
        "nombre": "GTA V",
        "genero": "Accion",
        "precio": 35
    },
    {
        "id": 4,
        "nombre": "Fortnite",
        "genero": "Disparos",
        "precio": 0
    }
]




@app.get("/")
def home():
    return {"mensaje": "API funcionando"}


# GET - Obtener todos los videojuegos
@app.get("/videojuegos", response_model=list[VideoJuegos])
def obtener_videojuegos():
    return videojuegos


# GET - Obtener videojuego por ID
@app.get("/videojuegos/{id}", response_model= VideoJuegos, responses ={404: {"description" : "Videojuego no encontrado"}
})
def obtener_videojuego_por_id(id: VideojuegoId):

    for videojuego in videojuegos:
        if videojuego["id"] == id:
            return videojuego

    raise HTTPException(status_code=404, detail="Videojuego no encontrado")



# GET - Buscar por género usando Query
@app.get("/buscar",response_model=list[VideoJuegos]) 
def buscar_videojuego(genero: GeneroBusqueda):
    resultado = []
    for videojuego in videojuegos:
        if videojuego["genero"].lower() == genero.lower():
            resultado.append(videojuego)
        
    return resultado



# POST - Agregar videojuego
@app.post("/videojuegos",response_model= VideoJuegos)
def agregar_videojuego(
    videojuego: dict = Body(...)
):
    videojuegos.append(videojuego)

    return videojuego


# PUT - Actualizar videojuego
@app.put("/videojuegos/{id}",response_model= VideoJuegos, responses ={404: {"description" : "Videojuego no encontrado"}
})
def actualizar_videojuego(
    id: VideojuegoId,
    videojuego_actualizado: dict = Body(...)
):
    for videojuego in videojuegos:
        if videojuego["id"] == id:
            videojuego.update(videojuego_actualizado)

            return {
                "mensaje": "Videojuego actualizado",
                "videojuego": videojuego
            }

    raise HTTPException(status_code=404, detail="Videojuego no encontrado")



# DELETE - Eliminar videojuego
@app.delete("/videojuegos/{id}",response_model= VideoJuegos,responses ={404: {"description" : "Videojuego no encontrado"}
})
def eliminar_videojuego(
        id: VideojuegoId,
):
    for videojuego in videojuegos:
        if videojuego["id"] == id:
            videojuegos.remove(videojuego)

            return {
                "mensaje": "Videojuego eliminado"
            }

    raise HTTPException(status_code=404, detail="Videojuego no encontrado")
