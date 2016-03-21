''' download info from amazon '''
from bs4 import BeautifulSoup
import os
from py2neo import authenticate, Graph, Node
import re
import requests
import sys

def load_book(url):
    ''' scrape from librarything '''
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')

    isbn = soup.find('meta', {'property': 'books:isbn'})['content']
    title = soup.find('meta', {'property': 'og:title'})['content']
    try:
        datestring = soup.find(class_='date').text
        year = re.sub(r'.*(\d{4}).*', r'\1', datestring)
    except Exception:
        year = ''
    uid = title.lower()
    uid = re.sub(' ', '-', uid)

    node = Node('edition', isbn=isbn, identifier=title, year=year, uid=uid)
    graph.create(node)


if __name__ == '__main__':
    user = os.environ['NEO4J_USER']
    password = os.environ['NEO4J_PASS']
    authenticate('localhost:7474', user, password)
    graph = Graph()

    load_book(sys.argv[1])
