import requests
import re
import json

api_url_base = "https://the-one-api.dev/v2/quote"
api_token = '7BZav5YGxUZHxdhGFDg3'
headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer {0}'.format(api_token)
}




def jprint(obj):
    text = json.dumps(obj, sort_keys=True, indent=4)
    print(text)




def get_book():
    api_url_base = "https://the-one-api.dev/v2/book"
    response = requests.get(api_url_base, headers=headers)
    if response.status_code == 200: 
        books = response.json()['docs']
        bookDict = {}
        for d in books:
          name = d['name']
          id = d['_id']
          bookDict[id] = name    
        return bookDict


      
      
def get_book_id(string_number):
    api_url_base = "https://the-one-api.dev/v2/book/"  + string_number
    response = requests.get(api_url_base, headers=headers)
    if response.status_code == 200:
        books = response.json()['docs']
        for d in books:
          name = d['name']
        return name

def get_book_chapter(string_number):
    api_url_base = "https://the-one-api.dev/v2/book/" + string_number + "/chapter"
    response = requests.get(api_url_base, headers=headers)
    if response.status_code == 200:
        books = response.json()['docs']
        bookDict = []
        for d in books:
          name = d['chapterName']
          bookDict.append(name) 
        return bookDict



      
def get_movies():
    api_url_base = "https://the-one-api.dev/v2/movie"
    response = requests.get(api_url_base, headers=headers)
    if response.status_code == 200: 
        movies = response.json()['docs']
        movieDict = {}
        for d in movies:
          name = d['name']
          id = d['_id']
          movieDict[id] = name    
        return movieDict

def get_movie_id(string_number):
    api_url_base = "https://the-one-api.dev/v2/movie/"+ string_number
    response = requests.get(api_url_base, headers=headers)
    if response.status_code == 200:
        movie = response.json()['docs']
        for d in movie:
          name = d['name']
        return name

def get_movie_quote(string_number):
    api_url_base = "https://the-one-api.dev/v2/movie/"  + string_number + "/quote"
    response = requests.get(api_url_base, headers=headers)
    if response.status_code == 200:
        movies = response.json()['docs']
        movieDict = {}
        for d in movies:
          name = d['dialog']
          id = get_character_id(d['character'])
          movieDict[id] = name
        return movieDict




  
def get_character():
    api_url_base = "https://the-one-api.dev/v2/character"
    response = requests.get(api_url_base, headers=headers)
    if response.status_code == 200: 
        char = response.json()['docs']
        charDict = {}
        for d in char:
          name = d['name']
          id = d['_id']
          charDict[id] = name    
        return charDict

def get_character_id(string_number):
    api_url_base = "https://the-one-api.dev/v2/character/"  + string_number
    response = requests.get(api_url_base, headers=headers)
    if response.status_code == 200:
        chars = response.json()['docs']
        for d in chars:
          name = d['name']
        return name





def get_quote():
    api_url_base = "https://the-one-api.dev/v2/quote"
    response = requests.get(api_url_base, headers=headers)
    if response.status_code == 200: 
        quotes = response.json()['docs']
        quoteDict = {}
        for d in quotes:
          id = d['_id']
          dialog = d['dialog']
          quoteDict[id] = dialog  
        return quoteDict



def get_chapter():
    api_url_base = "https://the-one-api.dev/v2/chapter"
    response = requests.get(api_url_base, headers=headers)
    if response.status_code == 200: 
        chapters = response.json()['docs']
        jprint(chapters)
        chaptersDict = {}
        for d in chapters:
          name = d['chapterName']
          id = d['_id']
          chaptersDict[id] = name    
        return chaptersDict