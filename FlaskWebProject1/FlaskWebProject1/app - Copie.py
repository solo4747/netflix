from flask import Flask, request, render_template
import pymysql
from flask import Flask
import pymysql.cursors  



# Connectez- vous à la base de données.
connection = pymysql.connect(host='62.171.158.215',
                             user='netflix',
                             password='WildCodeSchool',                             
                             db='recommender',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

app = Flask(__name__)


@app.route("/search", methods=["GET", "POST"])
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
            
            return render_template("index.html", data=data)

            return redirect(request.url)

    return render_template("choix.html")



# @app.route('/')
# def someName():

#     with connection.cursor() as cursor:
    
#         # SQL 
#         sql = "SELECT * from movies limit 5"
        
#         # Exécutez la requête (Execute Query).
#         cursor.execute(sql)
#         data = cursor.fetchall()

#     return render_template('index.html', data=data)

if __name__ == '__main__':
    app.run()