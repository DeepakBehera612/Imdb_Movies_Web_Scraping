from bs4 import BeautifulSoup
import requests
import pandas as pd
import time

url = 'https://imdb.com/chart/top'
res = requests.get(url=url)
soup = BeautifulSoup(res.text, features='html.parser')
all_tr = soup.findChildren('tr')

title_list = []
year_list = []
rating_list = []
movie_data = {}


for movie in all_tr:
    try:
        title_list.append(movie.find(
            'td', {'class': 'titleColumn'}).find('a').contents[0])

        year_list.append(movie.find('td', {'class': 'titleColumn'}).find(
            'span', {'class': 'secondaryInfo'}).contents[0])

        rating_list.append(movie.find(
            'td', {'class': 'ratingColumn imdbRating'}).find('strong').contents[0])
    except:
        continue

movie_data["title"] = title_list
movie_data["year"] = year_list
movie_data["rating"] = rating_list

df = pd.DataFrame(movie_data)


# df.to_csv('top_movies.csv')
# print('csv file generate successfully.')


df.to_excel('top_movies.xlsx')
print('csv file generate successfully.')