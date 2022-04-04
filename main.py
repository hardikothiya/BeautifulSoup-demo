from bs4 import BeautifulSoup
import requests
import json

responses = requests.get("https://www.empireonline.com/movies/features/best-movies-2/")
webpage = responses.text

soup = BeautifulSoup(webpage, "html.parser")
movie_name = soup.find_all(name="h3", class_="jsx-4245974604")
data = json.loads(soup.select_one("#__NEXT_DATA__").contents[0])

movies_names = []
def find_articles(data):
    if isinstance(data, dict):
        for k, v in data.items():
            if k.startswith("ImageMeta:"):
                yield v["titleText"]
            else:
                yield from find_articles(v)
    elif isinstance(data, list):
        for i in data:
            yield from find_articles(i)

for a in find_articles(data):
    movies_names.append(a)

final_list = movies_names[::-1]

print(final_list)

with open('movies.txt', mode='w') as file:
    for a in final_list:
        file.write(f"{a}\n")

