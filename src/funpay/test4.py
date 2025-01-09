import requests
from bs4 import BeautifulSoup
import concurrent.futures

# Fetches the page content
def fetch_page(url):
    headers = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "accept-language": "ru,en;q=0.9,en-GB;q=0.8,en-US;q=0.7",
        "sec-ch-ua": "\"Microsoft Edge\";v=\"131\", \"Chromium\";v=\"131\", \"Not_A Brand\";v=\"24\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
        "sec-fetch-dest": "document",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "same-origin",
        "sec-fetch-user": "?1",
        "upgrade-insecure-requests": "1"
    }
    response = requests.get(url, headers=headers)
    return response.text

# Parses user IDs from the page content
def parse_user_ids(html):
    soup = BeautifulSoup(html, 'html.parser')
    user_ids = set()
    for user_span in soup.find_all('div', class_='avatar-photo', attrs={'data-href': True}):
        data_href = user_span['data-href']
        if 'users' in data_href:
            user_id = data_href.split('/')[-2]
            user_ids.add(user_id)
    return user_ids

# Fetches reviews from FunPay
def fetch_reviews(user_id, continue_token, filter_value):
    payload = {
        "user_id": user_id,
        "continue": continue_token,
        "filter": filter_value
    }
    headers = {
        "accept": "text/html, */*; q=0.01",
        "accept-language": "ru,en;q=0.9,en-GB;q=0.8,en-US;q=0.7",
        "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
        "priority": "u=1, i",
        "sec-ch-ua": "\"Microsoft Edge\";v=\"131\", \"Chromium\";v=\"131\", \"Not_A Brand\";v=\"24\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "x-requested-with": "XMLHttpRequest"
    }
    response = requests.post('https://funpay.com/users/reviews', headers=headers, data=payload)
    return response.text

def parse_continue_token(html):
    soup = BeautifulSoup(html, 'html.parser')
    continue_input = soup.find('input', {'name': 'continue'})
    if continue_input:
        return continue_input['value']
    return None

def parse_reviews(html):
    soup = BeautifulSoup(html, 'html.parser')
    reviews = []
    for review_container in soup.find_all('div', class_='review-container'):
        rating_div = review_container.find('div', class_='rating')
        if rating_div:
            rating_class = rating_div.find('div')['class'][0]
            rating = int(rating_class.replace('rating', ''))
        else:
            rating = None
        review_text_div = review_container.find('div', class_='review-item-text')
        review_text = review_text_div.get_text(strip=True) if review_text_div else ''
        reviews.append({'rating': rating, 'text': review_text})
    return reviews

def fetch_user_reviews(user_id):
    continue_token = ""
    all_reviews = []
    iterations = 0
    while True:
        html = fetch_reviews(user_id, continue_token, "")
        reviews = parse_reviews(html)
        all_reviews.extend(reviews)
        continue_token = parse_continue_token(html)
        iterations += 1
        if iterations % 10 == 0:
            print(f"Отзывов для пользователя {user_id}: {len(all_reviews)}")
        if not continue_token:
            break
    return all_reviews

# Example usage
url = "https://funpay.com/lots/1350/"
html = fetch_page(url)

user_ids = parse_user_ids(html)

global_reviews = []
reviewcount = 0
max_reviews = 50000

with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
    future_to_user_id = {executor.submit(fetch_user_reviews, user_id): user_id for user_id in user_ids}
    for future in concurrent.futures.as_completed(future_to_user_id):
        user_id = future_to_user_id[future]
        try:
            user_reviews = future.result()
            global_reviews.extend(user_reviews)
            reviewcount += len(user_reviews)
            print(f"Отзывы для пользователя {user_id}:")
            for review in user_reviews:
                print(f"Rating: {review['rating']}, Review: {review['text']}")
            print(f"Всего отзывов: {len(user_reviews)}\n")
            if reviewcount >= max_reviews:
                break
        except Exception as exc:
            print(f"Пользователь {user_id} вызвал исключение: {exc}")

print("Все отзывы:")
# for review in global_reviews:
#     print(f"Rating: {review['rating']}, Review: {review['text']}")
# print(f"Всего отзывов: {len(global_reviews)}")

# Calculate and print statistics for global reviews
rating_stats = {}
for review in global_reviews:
    rating = review['rating']
    if rating not in rating_stats:
        rating_stats[rating] = 0
    rating_stats[rating] += 1

print("Статистика по отзывам:")
for rating, count in rating_stats.items():
    print(f"Оценка {rating}: {count} отзывов")