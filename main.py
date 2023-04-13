from fastapi import FastAPI
from data import productos

app = FastAPI()

@app.get("/")
def index():
    
    return "Holis"


#1) Pelicula de mayor duracion segun año, plataforma y tipo de duración.
@app.get('/get_max_duration/{anio}/{plataforma}/{duration_type}')
def get_max_duration(anio: int, plataforma: str, duration_type: str):

    try:
        sitio = plataforma.lower()[0]
        filtro = productos[ (productos['show_id'].str.startswith(sitio)) 
                            & (productos["type"] == "movie") 
                            & (productos["release_year"] == anio)
                            & (productos["duration_type"] == duration_type.lower())]
    
        max_duracion = filtro.loc[filtro["duration_int"].idxmax()]
        respuesta = max_duracion["title"]
        return {'pelicula': str(respuesta)}

    except ValueError:
        return "No hay datos, pruebe otras opciones"


#2) Cantidad de películas en la plataforma para determinado año y con un puntaje mayor al pedido.
@app.get('/get_score_count/{plataforma}/{scored}/{anio}')
def get_score_count(plataforma: str, scored: float, anio: int):

    sitio = plataforma.lower()[0]
    filtro = productos[(productos['show_id'].str.startswith(sitio)) 
                        & (productos['type'] == "movie") 
                        & (productos["release_year"] == anio) 
                        & (productos["score"] >= scored)]
    
    respuesta = len(filtro)
    return {
        'plataforma': plataforma,
        'cantidad': respuesta,
        'anio': anio,
        'score': scored
    }


#3)Cantidad de peliculas en la plataforma.
@app.get('/get_count_platform/{plataforma}')
def get_count_platform(plataforma: str):

    sitio = plataforma.lower()[0]
    filtro = productos[ (productos['show_id'].str.startswith(sitio)) 
                        & (productos['type'] == "movie") ]
    
    respuesta = len(filtro)
    return {'plataforma': plataforma, 'peliculas': respuesta}


#4) Actor que más se repite según plataforma y año.
@app.get('/get_actor/{plataforma}/{anio}')
def get_actor(plataforma: str, anio: int):

    try:
        sitio = plataforma.lower()[0]
        filtro = productos[ (productos['show_id'].str.startswith(sitio)) 
                            & (productos['release_year'] == anio) ]
    
        actores_lista = filtro['cast'].str.split(', ', expand=True).stack().value_counts()
        actor = actores_lista.index[0]
        actor_cantidad = actores_lista.values[0]

        return {"plataforma": plataforma,
        "anio": anio,
        "actor": actor,
        "apariciones": int(actor_cantidad)}
    
    except IndexError:
        return "No hay datos, pruebe otras opciones"


#5) Cantidad de contenidos publicados por país y año.
@app.get('/prod_per_county/{tipo}/{pais}/{anio}')
def prod_per_county(tipo: str, pais: str, anio: int):

    filtro = productos[ (productos['type'] == tipo) 
                        & (productos['country'] == pais.lower()) 
                        & (productos['release_year'] == anio) ]
    
    respuesta = len(filtro)
    return {'pais': pais, 'anio': anio, 'peliculas': respuesta}


#6) Cantidad de contenidos según el rating de audiencia.
@app.get('/get_contents/{rating}')
def get_contents(rating: str):
    
    filtro = productos[ productos["rating"] == rating.lower() ]

    respuesta = len(filtro)
    return {'rating': rating, 'contenido': respuesta}