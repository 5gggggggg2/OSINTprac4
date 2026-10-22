import requests

# эндпоинт, который мы нашли в Network
api_url = "https://quotes.toscrape.com/api/quotes?page=1"

print("Запрашиваем данные напрямую (без браузера)...")
resp = requests.get(api_url)

print(f"Статус ответа: {resp.status_code}")

if resp.status_code == 200:
    data = resp.json()
    quotes = data.get("quotes", [])
    print(f"Успешно получено {len(quotes)} цитат напрямую!")
    print(f"Пример первой цитаты: {quotes[0]['text'][:50]}... (автор: {quotes[0]['author']['name']})")
else:
    print("Не удалось получить данные.")