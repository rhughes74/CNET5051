# Your Turn!
import logging
import time
import random
import csv
import requests
from bs4 import BeautifulSoup
import pickle
from tqdm import tqdm
import time

logger = logging.getLogger(__name__)
logging.basicConfig(filename = 'kardashian_problems.log', encoding = 'utf-8',
                    level = logging.DEBUG)

with open(
        'data/kardashian_jenner_urls_jan_1_2024_to_july_31_2024_mediacloud.csv',
        'r', errors = 'ignore') as f:
    reader = csv.reader(f, delimiter = ',')
    urls = [line[-1] for line in reader][1:]


def get_people_in_article(url):
    """
    Given a URL (string) of a TMZ article,
    return a list of the names of the people (as strings) whose TMZ pages are linked in the article.
    You can handle invalid URLs within this function or in the for loop below,
    but make sure you're handling them!
    """
    people_in_article = []
    try:
        #Get the text off the URL
        txt = requests.get(url).text
        soup = BeautifulSoup(txt)
        for text_line in soup.find_all('p'):
            a_tags = text_line.find_all('a')
            for tag in a_tags:
                href = tag.get('href')
                if 'https://www.tmz.com/people/' in href:
                    people_in_article.append(href.split('/')[-2])
    except requests.ConnectionError as e:
        print('connection error')
        print(e)
        logging.debug('connection error')
    except Exception as e:
        print('other error')
        print(e)
        logging.debug('other error')
    return people_in_article
    


lists_of_people = []
for url in tqdm(random.sample(urls, 30)):
    lists_of_people.append(get_people_in_article(url))
    time.sleep(7)
#Saving our pickle
pickle.dump(lists_of_people, open('lists_of_people.pkl', 'wb'))
#Loading back in our pickle
lists_of_people= pickle.load(open('lists_of_people.pkl', 'rb'))