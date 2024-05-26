import requests
import datetime
import uuid
import json
from config import OPENWEATHER_API_KEY, BING_API_KEY, TRANSLATOR_API_KEY, TRANSLATOR_LOCATION, CRICAPI_KEY

def get_weather_data(city):
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&appid={OPENWEATHER_API_KEY}'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        data['wind']['speed'] = str(data['wind']['speed']) + " km/h"
        data['dt'] = str(datetime.datetime.fromtimestamp(data['dt']).strftime('%Y-%m-%d %H:%M:%S')) + ' GMT 0'
        data['sys']['sunrise'] = str(datetime.datetime.fromtimestamp(data['sys']['sunrise']).strftime('%Y-%m-%d %H:%M:%S')) + ' GMT 0'
        data['sys']['sunset'] = str(datetime.datetime.fromtimestamp(data['sys']['sunset']).strftime('%Y-%m-%d %H:%M:%S')) + ' GMT 0'
        return data
    else:
        print(f"Failed to fetch weather data. Status code: {response.status_code}")
        return None

def search_bing(query):
    try:
        endpoint = "https://api.bing.microsoft.com/v7.0/search"
        headers = {'Ocp-Apim-Subscription-Key': BING_API_KEY}
        params = {'q': query}
        response = requests.get(endpoint, headers=headers, params=params)
        response.raise_for_status()
        result = response.json()
        if result["webPages"]["value"]:
            markdown_results = ""
            for item in result["webPages"]["value"]:
                markdown_results += f"#### [{item['name']}]({item['url']}) \n {item['snippet']} \n\n"
            return markdown_results
        else:
            return "No results found"
    except Exception as e:
        return f"An unexpected error occurred: {e}"

def translate_text(text, to_lang):
    from_lang = 'en'
    endpoint = "https://api.cognitive.microsofttranslator.com"
    path = '/translate'
    constructed_url = endpoint + path

    params = {
        'api-version': '3.0',
        'from': from_lang,
        'to': [to_lang]
    }

    headers = {
        'Ocp-Apim-Subscription-Key': TRANSLATOR_API_KEY,
        'Ocp-Apim-Subscription-Region': TRANSLATOR_LOCATION,
        'Content-type': 'application/json',
        'X-ClientTraceId': str(uuid.uuid4())
    }

    body = [{'text': text}]
    request = requests.post(constructed_url, params=params, headers=headers, json=body)
    response = request.json()
    return response[0]["translations"][0]["text"]