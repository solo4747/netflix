from flask import Flask, request, render_template
import pymysql
from flask import Flask
import pymysql.cursors  
import pickle
import model
from flask import jsonify


# Connectez- vous à la base de données.
connection = pymysql.connect(host='62.171.158.215',
                             user='netflix',
                             password='WildCodeSchool',                             
                             db='recommender',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

with connection.cursor() as cursor:
    sql = f"SELECT * FROM movies WHERE title LIKE '% toy%'"
    query = cursor.execute(sql)
    data = cursor.fetchall()
    from flask import jsonify
    results = [data[i]['title'] for i in range(len(data))]
    print(results.dtype)