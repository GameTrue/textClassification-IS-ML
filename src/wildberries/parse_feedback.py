import os
import requests
import json

def fetch_feedbacks(card_id='102721538'):
    url = f"https://feedbacks2.wb.ru/feedbacks/v2/{card_id}"
    headers = {
        "sec-ch-ua": "\"Microsoft Edge\";v=\"131\", \"Chromium\";v=\"131\", \"Not_A Brand\";v=\"24\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
        "Referer": "https://www.wildberries.ru/catalog/186639803/detail.aspx"
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()

def save_data(data, file_path):
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

    
if __name__ == "__main__":
    all_products = []
    data = fetch_feedbacks('186639803')

    file_path = os.path.join(os.path.dirname(__file__), 'data', 'feedback.json')
    save_data(data, file_path)
    print(len(data))