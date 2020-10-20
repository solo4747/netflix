import sys
import pandas as pd
import pymysql.cursors 

###############################
#####     Db connexion    #####
###############################
 

connection = pymysql.connect(host='62.171.158.215',
                             user='netflix',
                             password='WildCodeSchool',                             
                             db='recommender',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

with connection.cursor() as cursor:
    sql = f"select * from recommender.movies"
    cursor.execute(sql)
    data = cursor.fetchall()

# convert to dataframe :
df_movies = pd.DataFrame(data)


###############################
##### Pre-processing Data #####
###############################

#create a new Year column from title :

def getYear(title_year):
    year = title_year[-5:-1]
    try:
        year_int = int(year)
    except:
        year_int = 0

    return year_int

df_movies['year'] = df_movies['title'].apply(getYear)
df_movies['decade'] = df_movies['year'].apply(lambda x: (x-1900)//10)


# create dummies - Genres col
df_movies = pd.concat([df_movies, df_movies['genres'].str.get_dummies(sep='|')], axis=1)



df_model = df_movies[['title','decade','Action', 'Adventure', 'Animation', 'Children',
       'Comedy', 'Crime', 'Documentary', 'Drama', 'Fantasy', 'Film-Noir',
       'Horror', 'IMAX', 'Musical', 'Mystery', 'Romance', 'Sci-Fi', 'Thriller',
       'War', 'Western']]

df_model = df_model.set_index('title')

###############################
#####     Predictions     #####
###############################

def getMovies(movie):
    from sklearn.neighbors import NearestNeighbors
    from sklearn.preprocessing import LabelEncoder

    KNN_model = NearestNeighbors(n_neighbors=5).fit(df_model)
    indices = KNN_model.kneighbors(df_model[df_model.index == movie].values, 10, return_distance=False)
    indices = list(indices[0])
    list_predicted_movies = []
    for i in indices:
        list_predicted_movies.append(df_movies.iloc[i].title)
    return list_predicted_movies


output = getMovies('Freddie as F.R.O.7. (1992)')
print(output)


# ###############################
# #####     Pickle          #####
# ###############################
# # import pickle

# # pickle.dump(output, open('model.pkl','wb'))
# # model = pickle.load(open('model.pkl','rb'))
