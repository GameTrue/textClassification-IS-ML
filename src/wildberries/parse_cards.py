import requests
import json
import os

def fetch_data(page):
    query_params = {
        "ab_visual_prediction_space": "ab_ps_prod",
        "appType": 1,
        "curr": "rub",
        "dest": "-1181031",
        "hide_dtype": 10,
        "lang": "ru",
        "page": page,
        "query": "60840048",
        "resultset": "catalog",
        "spp": 30,
        "suppressSpellcheck": False,
        "uclusters": 2,
        "uiv": 1,
        "uv": "sOGq5Kvpq10g3jAJMfAulSpbrSssFCQesK8iD66pLpaih67PKGkpXa8iGZwo0iQeKKiuKqy9prIY-isGmeqnWrOEp4gxoLCwqI-tsqo9pskwqi_0J8GpJqE-Kn4qNimgMASssqgULluxDCy2q0yPKSwOMg8lNzBnLNOkQqsxKtuqeCCPrRsokarmsEU0wyqMsBIrN6ENFuOwfjEALsGkVy3BLGOoqjGRrBAk4JxOqfcx8SYXLAOvKaJ-LMcxqB-IpsksuxJOpYixMBTNI8Msca00q6GnHKLZGi2pXKtEj8qoQqtqq30oUCaaGCcuJKpdrHcyGKwUKOavoLDRp2uhtw"
    }
    url = "https://recom.wb.ru/personal/ru/male/v5/search"
    headers = {
        "accept": "*/*",
        "accept-language": "ru,en;q=0.9,en-GB;q=0.8,en-US;q=0.7",
        "authorization": "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJpYXQiOjE3MzM3ODYwMzYsInZlcnNpb24iOjIsInVzZXIiOiI2MDg0MDA0OCIsInNoYXJkX2tleSI6IjEyIiwiY2xpZW50X2lkIjoid2IiLCJzZXNzaW9uX2lkIjoiZjU2YTdiYTg1NGZhNDczN2I1OGViZjk0MmM2YjQxN2MiLCJ1c2VyX3JlZ2lzdHJhdGlvbl9kdCI6MTY3NTY3MDY1MywidmFsaWRhdGlvbl9rZXkiOiIzMTg3MWViZjg4ZTk2ODE1MWE2NTMxYjJhZDk4Zjg2NjZhZmFjZmNiZDNhMjU5YWZkYmQ0ZGExYTcyY2Q3MTdhIiwicGhvbmUiOiJvUkdVUERtRlgyQU1KUjZSWWorbWpnPT0ifQ.CbwqpKtYeZmZAXK9Vd3Fi6b6dkUxTUkfjHw3CzZ7zDEQkCf2wMYhFr1XzwRiLilD7YaAwtxA5Iu0dUAHe1x9peMON2Z_fjHRz4QT02Fl6-xN11kLYK2r63QEFb2ImWZR4qHt7y7CNt0YdQ2NR3SnVf6CELrVBbffsYt1oU7hDzIj1bKncLY6NuAG2wxEL_tnKlqV8NseKHS7RafP_bkDWSqEymygTqIwNb6vVUwAsr0P3Q1Gt3lPOJFzM9_dn4KD_pM2-9ZXZNINjvINmi3FC3y4giStK_knPWdwJ_ENfRvo5tGusx-vSJ8SLiby-C2U47PuJzkOSMPYLd_yrhZvBw",
        "basket": "196486696=1733706485;171630341=1733353955;241114389=1732790479;267555627=1732405363;77483151=1710002028;139696728=1710001407",
        "clicks": "207322849=1733953157;292395010=1733953156;270451681=1733953156;172618610=1733953155;270037545=1733953155;196486696=1733953140;213120432=1733953114;224031990=1733953112;191987936=1733953112;270451683=1733953111;207323400=1733953111;292388540=1733953085;195558250=1733953083;195558249=1733953082;276432237=1733953081;195906722=1733953081;195558248=1733953064;238059844=1733953063;195557745=1733953063;220715939=1733952760",
        "priority": "u=1, i",
        "sec-ch-ua": "\"Microsoft Edge\";v=\"131\", \"Chromium\";v=\"131\", \"Not_A Brand\";v=\"24\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "cross-site",
        "x-userid": "60840048"
    }
    response = requests.get(url, headers=headers, params=query_params)
    return response.json()

def save_data(data, file_path):
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    all_products = []
    for page in range(1, 101):
        data = fetch_data(page)
        if not data:
            print(page, data)
            break
        all_products.extend(data['data'].get('products', []))
    file_path = os.path.join(os.path.dirname(__file__), 'data', 'products.json')
    save_data(all_products, file_path)
    print(len(all_products))