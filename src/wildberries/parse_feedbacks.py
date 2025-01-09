import os
import requests
import json

def fetch_feedbacks(card_id='102721538'):
    url = f"https://feedbacks2.wb.ru/feedbacks/v2/{card_id}"
    headers = {
        "sec-ch-ua": "\"Microsoft Edge\";v=\"131\", \"Chromium\";v=\"131\", \"Not_A Brand\";v=\"24\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
        "Referer": "https://www.wildberries.ru/catalog/155333353/detail.aspx"
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()

def save_data(data, file_path):
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def process_feedbacks(feedbacks):
    result = []
    for feedback in feedbacks:
        text_parts = []
        for key in ['pros', 'cons', 'text']:
            if feedback.get(key):
                text_parts.append(feedback[key])
        if feedback.get('babels'):
            text_parts.append('. '.join(feedback['babels']))
        text = '. '.join(text_parts)
        rating = feedback.get('productValuation')
        result.append({'text': text, 'rating': rating})
    return result

def print_feedback_statistics(feedbacks):
    stats = {}
    for feedback in feedbacks:
        rating = feedback.get('rating')
        if rating is not None:
            stats[rating] = stats.get(rating, 0) + 1
    for rating in sorted(stats.keys(), reverse=True):
        print(f"{rating}: {stats[rating]}")

if __name__ == "__main__":
    # all_products = []
    # data = fetch_feedbacks('102721538')

    # file_path = os.path.join(os.path.dirname(__file__), 'data', 'feedback.json')
    # save_data(data, file_path)
    # print(len(data))

    # Чтение списка товаров из cards.json
    cards_file_path = os.path.join(os.path.dirname(__file__), 'data', 'products.json')
    with open(cards_file_path, 'r', encoding='utf-8') as f:
        cards_data = json.load(f)

    product_ids = [str(product['root']) for product in cards_data]

    all_feedbacks = []
    for product_id in product_ids:
        feedback_data = fetch_feedbacks(product_id)
        # print(feedback_data)
        if feedback_data and 'feedbacks' in feedback_data and feedback_data['feedbacks']:
            processed_feedbacks = process_feedbacks(feedback_data['feedbacks'])
            all_feedbacks.extend(processed_feedbacks)
        else:
            print(f"No feedbacks found for product ID {product_id}")

    # Сохранение обработанных отзывов
    output_file_path = os.path.join(os.path.dirname(__file__), 'data', 'feedback_processed.json')
    save_data(all_feedbacks, output_file_path)
    
    # Вывод статистики по оценкам
    print_feedback_statistics(all_feedbacks)