import requests
import datetime
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient

key_vault_url = f"https://one-leiaws-kv.vault.azure.net"
secret_name = "BING-SEARCH-API-KEY"

credential = DefaultAzureCredential()
client = SecretClient(vault_url=key_vault_url, credential=credential)
retrieved_secret = client.get_secret(secret_name)
api_key = retrieved_secret.value

def get_news_by_bing_search(topic,mkt='en-US' ,count=10, offset=0):
    url = "https://api.bing.microsoft.com/v7.0/news/search"
    query = topic
    params = {
        'q': query,
        'safeSearch': 'moderate',
        'textformat': 'raw',
        'offset': offset,
        'sortBy': 'date',
        'count': count,
        'freshness': 'Week',
        'mkt': mkt
    }
    headers = {
        'Ocp-Apim-Subscription-Key': api_key
    }

    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        response.raise_for_status()

def format_news(response):
    news_list = []
    for article in response.get('value', []):
        if 'msn.com' in article.get('url'):
            continue
        news_item = {
            'name': article.get('name'),
            'description': article.get('description'),
            'url': article.get('url'),
            'datePublished': article.get('datePublished'),
        }
        news_list.append(news_item)
    return news_list

def generate_news_feed(topic, mkt,count, offset):
    response = get_news_by_bing_search(topic, mkt,count, offset)
    formatted_news = format_news(response)
    return formatted_news