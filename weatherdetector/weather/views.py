import re
import sys
from django.shortcuts import render
import json
import urllib.request
from requests import request
# Create your views here.


def index(request):
    if request.method == 'POST':
        city = request.POST['city']
        res = urllib.request.urlopen(
            'http://api.openweathermap.org/data/2.5/weather?q=' + city+'&appid=85a98231b4123f64952e7a6a91ecaefb')
        jsondata = json.load(res)
        data = {
            'country_code': str(jsondata['sys']['country']),
            'coordinate': str(jsondata['coord']['lon']) + ' ' +
            str(jsondata['coord']['lat']),
            'temp': str(jsondata['main']['temp']) + 'k',
            'pressure': str(jsondata['main']['pressure']),
            'humidity': str(jsondata['main']['humidity'])
        }
    else:
        city = ''
        data = {}
    return render(request, 'index.html', {'city': city, 'data': data})
