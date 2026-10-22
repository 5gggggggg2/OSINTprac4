import requests

url = "https://quotes.toscrape.com/scroll"
resp = requests.get(url)

print(f"Статус: {resp.status_code}")
print(f"Длина ответа: {len(resp.text)} символов")

# Проверяем наличие конкретной цитаты
if "Albert Einstein" in resp.text:
    print("Данные есть в HTML. Headless не нужен.")
else:
    print("Данные НЕ найдены в HTML. Это динамическая страница (JS), нужен Playwright.")
