import os
from urllib.parse import urlparse
import argparse
import requests
from dotenv import load_dotenv



def is_bitlink(token, url):
    divided_url = urlparse(url)
    header = {
        'Authorization': token
    }
    full_url = f'https://api-ssl.bitly.com/v4/bitlinks/' \
               f'{divided_url.netloc}{divided_url.path}'
    response = requests.get(full_url, headers=header)
    return response.ok


def shorten_link(token, url):
    header = {
        'Authorization': token
    }
    long_url = {
        "long_url": url
    }
    response = requests.post(
        "https://api-ssl.bitly.com/v4/shorten",
        headers=header,
        json=long_url)
    response.raise_for_status()
    bitlink = response.json()["link"]
    return bitlink


def count_clicks(token, url):
    divided_url = urlparse(url)
    full_url = f'https://api-ssl.bitly.com/v4/bitlinks/' \
               f'{divided_url.netloc}{divided_url.path}/clicks'
    header = {
        'Authorization': token
    }
    params = {
        'unit': 'day',
        'units': '-1'
    }
    response = requests.get(full_url, headers=header, params=params)
    response.raise_for_status()
    clicks = response.json()['link_clicks'][0]['clicks']
    return clicks


def main():
    load_dotenv()
    token = os.environ['BITLY_TOKEN']
    parser = argparse.ArgumentParser()
    parser.add_argument("url", help='Ссылка')
    args = parser.parse_args()
    url = args.url
    if is_bitlink(token, url):
        print('Количество кликов:', count_clicks(token, url))
    else:
        print('Ваш битлинк:', shorten_link(token, url))


if __name__ == '__main__':
    main()
