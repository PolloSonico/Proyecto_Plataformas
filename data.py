import pandas as pd

productos = pd.read_csv("data/productos.csv")

ratings1 = pd.read_csv("data/ratings/1.csv")
ratings2 = pd.read_csv("data/ratings/2.csv")
ratings3 = pd.read_csv("data/ratings/3.csv")
ratings4 = pd.read_csv("data/ratings/4.csv")
ratings5 = pd.read_csv("data/ratings/5.csv")
ratings6 = pd.read_csv("data/ratings/6.csv")
ratings7 = pd.read_csv("data/ratings/7.csv")
ratings8 = pd.read_csv("data/ratings/8.csv")

ratings = pd.concat([ratings1, ratings2, ratings3, ratings4, ratings5, ratings6, ratings7, ratings8], axis=0)