# <h1 align=center> **PROYECTO INDIVIDUAL Nº1** </h1>

# <h1 align=center>**Machine Learning Operations (MLOps)**</h1>

Esta API te permite obtener información sobre series y películas de diversas plataformas (en concreto Amazon Prime, Disney Plus, Hulu y Netflix), así como también te permite utilizar un modelo de machine learning para obtener recomendaciones personalizadas.

Requisitos

    Python3
    Libreria FastApi (se puede instalar con pip install fastapi)
    Libreria Pandas (se puede instalar con pip install pandas)
    Libreria Scikit-Learn (se puede instalar con pip install scikit-learn)
    Cuenta de Render
    
## **ETL Realizado**

Estos fueron los cambios realizados a partir de lo pedido en el trabajo:

    Generé un id: Cada id se compone de la primera letra del nombre de la plataforma, seguido del show_id ya presente en los datasets (ejemplo para títulos de Amazon = as123).

    Los valores nulos del campo rating se reemplazaron por el string “G” (corresponde al maturity rating: “general for all audiences”).

    La fecha de subida a la plataforma se puso en formato AAAA-mm-dd.

    Los campos de texto están en minúsculas, sin excepciones.

    El campo duration lo convertí en dos campos: duration_int y duration_type. El primero esun integer y el segundo un string indicando la unidad de medición de duración: min (minutos) o season (temporadas).

También unifique los datasets de las plataformas en un único archivo csv para un acceso mas facil a la información y limpié la columna de géneros, que es la utilizada para el modelo de recomendación hecho mas adelante.


## **Funciones disponibles**

## 1. get_max_duration(anio, plataforma, duration_type)

Película (sólo película, no serie, ni documentales, etc) con mayor duración según año, plataforma y tipo de duración. La función devuelve sólo el string del nombre de la película.

Ejemplo:

`/get_max_duration/2012/amazon/min`

```
    {
    "pelicula": "jab tak hai jaan"
    }
```

## 2. get_score_count(plataforma, scored, anio)

Cantidad de películas (sólo películas, no series, ni documentales, etc) según plataforma, con un puntaje mayor a XX en determinado año. La función devuelve un int, con el total de películas que cumplen lo solicitado.

Ejemplo:

`/get_score_count/amazon/3.5/2012`

```
    {
    "plataforma": "amazon",
    "cantidad": 146,
    "anio": 2012,
    "score": 3.5
    }
```

## 3. get_count_platform(plataforma)

Cantidad de películas (sólo películas, no series, ni documentales, etc) según plataforma. La función devuelve un int, con el número total de películas de esa plataforma. Las plataformas deben llamarse amazon, netflix, hulu, disney.

Ejemplo:

`/get_count_platform/amazon`

```
    {
    "plataforma": "amazon",
    "peliculas": 7814
    }
```

## 4. get_actor(plataforma, anio)

Actor que más se repite según plataforma y año. La función devuelve sólo el string con el nombre del actor que más se repite según la plataforma y el año dado.

Ejemplo:

`/get_actor/amazon/2012`

```
    {
    "plataforma": "amazon",
    "anio": 2012,
    "actor": "danny trejo",
    "apariciones": 3
    }
```

## 5. prod_per_county(tipo, pais, anio)

La cantidad de productos disponibles en streaming que se publicaron por país y año. La función devuelve el tipo de contenido (pelicula,serie) por pais y año en un diccionario con las variables llamadas 'pais' (nombre del pais), 'anio' (año) y 'pelicula' (tipo de contenido).

Ejemplo:

`/prod_per_county/movie/india/2012`

```
    {
    "pais": "india",
    "anio": 2012,
    "peliculas": 40
    }
```

## 6. get_contents(rating)

La cantidad total de contenidos disponibles en streaming según el rating de audiencia dado (para que publico fue clasificada la pelicula). La función devuelve el numero total de contenido con ese rating de audiencias.

Ejemplo:

`/get_contents/g`

```
    {
      "rating": "g",
      "contenido": 1311
    }
```

## 7. get_recommendation(titulo)

Esta función utiliza un modelo de machine learning para obtener cinco recomendaciones personalizadas a partir del título de una serie o película. titulo es un string con el título de la serie o película que deseas utilizar como base para las recomendaciones. La función devuelve una lista con los títulos de las cinco recomendaciones.

Ejemplo:

`/get_recommendation/zodiac`

```
    [
      "only god forgives",
      "the machinist",
      "the beguiled",
      "the clovehitch killer",
      "croupier"
    ]
```

## **Ejecución**

La API está montada utilizando la página **`Render.com`**, mas concretamente en **`https://proyecto-plataformas-deploy.onrender.com/`**.
