from flask import Flask
import pandas as pd
import matplotlib.pyplot as plt
import requests
from flask import send_file

#cria a aplicação flask
app = Flask(__name__)


#Criação dos dataframes
df_filmes = pd.read_csv("./data/movies.csv", sep=",", names=['filmeId', 'titulo', 'generos'], skiprows=1)
df_avaliacao = pd.read_csv("./data/ratings.csv", sep=",", names=['usuarioId', 'filmeId', 'avaliacao', 'momento'], skiprows=1)

#Serapando o genero em um novo dataframe, contudo poderaiamos trabalhar diretamente no dataframe de oriegm
df_generos = df_filmes['generos'].str.get_dummies("|")

#Calculado a media dos votos por filmes
df_media = df_avaliacao.groupby("filmeId")['avaliacao'].mean()
df_filmes_media = df_filmes.join(df_media, on='filmeId')


#Rotas e funcoes da API
@app.route("/")
def index():
    return "API Funcionado"

@app.route("/filmes/head")
def pandas_head():
    return df_filmes.head().to_html()

@app.route("/avaliacoes/head")
def pandas_avaliacao_hed():
    return df_avaliacao.head().to_html()

@app.route("/filmes/describe")
def pandas_filmes_describe():
    return df_filmes.describe().to_html()

@app.route("/avaliacoes/describe")
def pandas_avaliacoes_describe():
    return df_avaliacao.describe().to_html()

@app.route("/avaliacoes/boxplot")
def pandas_avaliacoes_boxplot():
    fig = df_avaliacao.boxplot(column="avaliacao")
    plt.savefig('boxplot.png')
    plt.switch_backend('agg')
    return send_file('../boxplot.png', mimetype='image/gif')

@app.route("/filmes/<id>")
def pandas_filmes_id(id):
    try:
        result = df_filmes.query("filmeId == " + id)
        return result.to_html()
    except:
        return "Filme não encontrado"

@app.route("/avaliacoes/<id>")
def pandas_avaliacoes_id(id):
    try:
        result = df_avaliacao.query("filmeId == " + id)
        return result.to_html()
    except:
        return "Avalições não encontradas"

@app.route("/avaliacoes/hist")
def pandas_avaliacoes_hist():
    fig = df_avaliacao.hist(column=["avaliacao", "filmeId"])
    plt.savefig("hist_avaliacao.png")
    plt.switch_backend('agg')
    return send_file("../hist_avaliacao.png", mimetype="image/gif")

@app.route("/avaliacoes/hist/<id>")
def pandas_avaliacao_hist_id(id):
    try:
        df_avaliacao.query("filmeId == " + id).hist("avaliacao")
        titulo = df_filmes.query("filmeId == " + id)
        plt.title("Avaliações: " + titulo.titulo.values[0])
        plt.savefig("hist_avaliacao_id.png")
        plt.switch_backend('agg')
        return send_file("../hist_avaliacao_id.png", mimetype="image/gif")
    except:
        return "Avaliações não encontradas"

@app.route("/generos/head")
def pandas_genero_head():
    return df_generos.head().to_html()

@app.route("/generos/pie")
def pandas_generos_pie():
    df_generos.sum().plot(
            kind ='pie',
            title ='Categorias Presentes nos Filmes',
            figsize=(8,8)
        )
    plt.savefig("pie_cat_filme")
    plt.switch_backend('agg')
    return send_file("../pie_cat_filme.png", mimetype="image/gif")

@app.route("/generos/bar")
def pandas_genero_bar():
    df_generos.sum().sort_values(ascending=False).plot(
        kind="bar",
        title="Categorias Presentes nos Filmes",
        figsize=(8,8)
    )
    plt.savefig("bar_cat_filme")
    plt.switch_backend('agg')
    return send_file("../bar_cat_filme.png", mimetype="image/gif")

#informa os parametros para enderço sob o qual a api vai rodar
app.run(host='localhost', port=3000)
