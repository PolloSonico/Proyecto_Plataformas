from fastapi import FastAPI
import pandas

productos = pandas.read_csv("data/productos.csv")
app = FastAPI()

@app.get("/")
def index():
    
    return "Holis"


#1) Película de mayor duración según año, plataforma y tipo de duración.
@app.get('/get_max_duration/{anio}/{plataforma}/{duration_type}')
def get_max_duration(anio: int, plataforma: str, duration_type: str):

    #Puse un manejo de excepciones para evitar errores cuando la primer letra 
    #de la plataforma no coincide con las utilizadas en el dataset.
    try:
        #Como la información de la plataforma en la que se encuentra el show está en la
        #primer letra del id, extraigo solo el primer caracter del parametro "plataforma".
        sitio = plataforma.lower()[0]

        filtro = productos[ (productos['show_id'].str.startswith(sitio)) 
                            & (productos["type"] == "movie") 
                            & (productos["release_year"] == anio)
                            & (productos["duration_type"] == duration_type.lower()) ]
    
        #Dentro del filtro anterior busco la duración más alta.
        max_duracion = filtro.loc[filtro["duration_int"].idxmax()]
        respuesta = max_duracion["title"]

        return {'pelicula': str(respuesta)}

    except ValueError:
        return "No hay datos, asegurese de que la plataforma este bien escrita, y que coincide con las utilizadas."


#2) Cantidad de películas en la plataforma para determinado año y con un puntaje mayor al pedido.
@app.get('/get_score_count/{plataforma}/{scored}/{anio}')
def get_score_count(plataforma: str, scored: float, anio: int):

    sitio = plataforma.lower()[0]

    filtro = productos[(productos['show_id'].str.startswith(sitio))
                        & (productos['type'] == "movie") 
                        & (productos["release_year"] == anio) 
                        & (productos["score"] > scored)]

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

        #Utilizo la función split() para separar los actores por comas (,), 
        #cuento la cantidad de veces que aparece cada uno y los ordeno de mayor a menor.
        actores_lista = filtro['cast'].str.split(', ', expand=True).stack().value_counts()

        actor = actores_lista.index[0]
        actor_cantidad = actores_lista.values[0]

        return {"plataforma": plataforma,
        "anio": anio,
        "actor": actor,
        "apariciones": int(actor_cantidad)}
    
    except IndexError:
        return "No hay datos, asegurese de que la plataforma este bien escrita, y que coincide con las utilizadas."


#5) Cantidad de contenidos publicados por país y año.
@app.get('/prod_per_county/{tipo}/{pais}/{anio}')
def prod_per_county(tipo: str, pais: str, anio: int):

    filtro = productos[ (productos['type'] == tipo) 
                        & (productos['country'].str.contains(pais.lower())) 
                        & (productos['release_year'] == anio) ]
    
    respuesta = len(filtro)
    return {'pais': pais, 'anio': anio, 'peliculas': respuesta}


#6) Cantidad de contenidos según el rating de audiencia.
@app.get('/get_contents/{rating}')
def get_contents(rating: str):
    
    filtro = productos[ productos["rating"] == rating.lower() ]

    respuesta = len(filtro)
    return {'rating': rating, 'contenido': respuesta}


#7) Recomendador de series y peliculas
@app.get('/get_recommendation/{titulo}')
def get_recommendation(titulo: str):

    try:
        id_show = (productos[productos["title"] == titulo].index)[0]
        
        #Divido el conjunto de géneros y creo nuevas columnas para cada género.
        genres = productos['listed_in'].str.get_dummies(sep=', ')

        #Calculo la similitud coseno entre todas las películas a partir de sus géneros.
        from sklearn.metrics.pairwise import cosine_similarity
        similarities = cosine_similarity(genres)

        #Encuentro las películas más similares a la que tiene el ID 1.
        similar_movies = list(enumerate(similarities[id_show]))
        sorted_similar_movies = sorted(similar_movies, key=lambda x: x[1], reverse=True)[0:10]

        #Imprimo los títulos de las películas recomendadas.
        recommended_movies = [productos.iloc[i[0]]['title'] for i in sorted_similar_movies]

        #Como hay contenidos que se encuentran en mas de una plataforma, elimino los resultados iguales.
        if titulo in recommended_movies:
            recommended_movies.remove(titulo)
            
        return recommended_movies[:5]
    except IndexError:
        return "No hay ninguna pelicula o serie con ese nombre"