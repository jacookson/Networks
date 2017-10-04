import requests
import base64
import json
import argparse

def main():

    parser = argparse.ArgumentParser(description='Search Modifiers')
    parser.add_argument('q', help='The Search Keyword')
    parser.add_argument('--geocode', help='Specifies an Area to Search Within')
    args = parser.parse_args()

    consumer_key = '9TZu9cQBvl10InNuUSdj3Pqbm'
    consumer_secret = '9ovztS5t1BtC3cA09SeLKot0F2JllBfOQJhYH8UrHKEiAmpvPJ'
    credentials = base64.b64encode(consumer_key + ':' + consumer_secret)

    payload = { 'grant_type': 'client_credentials' }
    headers = { 'Authorization': 'Basic ' + credentials,
            'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8' }

    r = requests.post("https://api.twitter.com/oauth2/token",
                  headers=headers, data=payload)

    j = json.loads(r.content)


    headers = {'Authorization': 'Bearer ' + j['access_token']}
    parameters = {'q': args.q,'geocode':args.geocode}

    r = requests.get('https://api.twitter.com/1.1/search/tweets.json',
                     headers=headers, params=parameters)

    j = json.loads(r.content)

    for tweet in j['statuses']:
        print 'Tweeted on: ' + tweet['created_at']
        print 'Tweeted by: ' + tweet['user']['name']
        print tweet['text']
        print ''

main()
