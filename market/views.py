from django.shortcuts import render
import json
import requests

def isbn(request, isbn):
    r = requests.get('https://www.googleapis.com/books/v1/volumes', params={'q': isbn})
    j = json.loads(r.text)
    info = j['items'][0]['volumeInfo']
    
    context = {
        'isbn': info['industryIdentifiers'][1]['identifier'],
        'title': info['title'],
        'authors': info['authors'][0],
    }
    
    return render(request, 'isbn.html', context=context)