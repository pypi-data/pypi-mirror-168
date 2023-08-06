# download_jokes.py

import yaml
import urllib.request
from utils import scrap_reddit

with open("auth.yaml", 'r') as stream:
    infos = yaml.safe_load(stream)

banned_words = [] 
banned_words_url = "http://www.bannedwordlist.com/lists/swearWords.txt"
file = urllib.request.urlopen(banned_words_url)
for line in file:
    word = line.decode("utf-8").strip().lstrip()
    banned_words.append(word)

url = "https://www.reddit.com/r/Jokes/top/?t=day"

instance = scrap_reddit(starting_url = url,
                        banned_words = banned_words,
                        client_name = infos["client_name"],
                        db_name = infos["db_name"],
                        collection_name = infos["collection_name"])

instance.get_jokes()

