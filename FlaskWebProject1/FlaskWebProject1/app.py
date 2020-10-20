from flask import Flask, request, render_template
import pymysql
import pymysql.cursors  
import pickle
import pandas as pd
import model


#Connection à la base de données.
connection = pymysql.connect(host='62.171.158.215',
                             user='netflix',
                             password='WildCodeSchool',                             
                             db='recommender',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def sign_up():

    if request.method == "POST":

        # récupération du nom du film
        movie = request.form["movie"]

        #Requête dans la base de données
        with connection.cursor() as cursor:
 
            sql = f"SELECT * FROM movies WHERE title = '{movie}'"
            
            # Exécutez la requête (Execute Query).
            cursor.execute(sql)
            data = cursor.fetchall()
            # data se présente comme list de dictionnaire -> [0], ensuite sélection de la colonne.
            data = data[0]['title']
            
            # Prédit la suggestion de film à partir du modèle LNN (model.py)
            output = model.getMovies(data)

            # pour ressortir le titre de la prédiction
          
            trailers = []
            titles = []
            resumes = []
            directors = []
            actors = []
            ratings = []
            for i in range(10):
                split_title = output[i].split()
                title_omdb =''
                for i in range(len(split_title)-1):
                    title_omdb = title_omdb + '+'  + split_title[i]
                
                title_omdb = title_omdb[1:].replace(',', '')
                import requests
                import json
                from youtube_search import YoutubeSearch

                response = json.loads(requests.get("http://www.omdbapi.com/?t="+title_omdb+"&apikey=8ab8c578").text)
                if len(resumes) == 5:
                    break
                else : 
                    if  response['Response'] == 'True' :
                        resume = response['Plot']
                        results = YoutubeSearch(str(response['Title'])+'trailer', max_results=10).to_dict()
                        trailer = "http://www.youtube.com"+str(results[0]['link'])
                        trailer = trailer.replace("watch?v=", "embed/")
                        trailers.append(trailer)
                        resumes.append(response['Plot'])
                        titles.append(response['Title'])
                        directors.append(response['Director'])
                        actors.append(response['Actors'])
                        ratings.append(response['imdbRating'])


            return render_template("results.html", prediction=output, trailer = trailers, title = titles, resume=resumes, directors=directors, actors=actors, ratings=ratings)
            return redirect(request.url)

    return render_template("search.html")


@app.route('/autocomplete',methods=['POST', 'GET'])
def ajaxautocomplete():
    with connection.cursor() as cursor:
        sql = f"SELECT * FROM movies WHERE title LIKE '%%'"
        query = cursor.execute(sql)
        data = cursor.fetchall()
        from flask import jsonify
        results = [data[i]['title'] for i in range(len(data))]

    return render_template("search.html", results=results)

if __name__ == '__main__':
    app.run()