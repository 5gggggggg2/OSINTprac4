import requests
import time
import pandas as pd

t0 = time.perf_counter()

all_quotes = []
# Собираем все 10 страниц через API
for page in range(1, 11):
    resp = requests.get(f"https://quotes.toscrape.com/api/quotes?page={page}")
    if resp.status_code == 200:
        data = resp.json()
        for q in data.get("quotes", []):
            all_quotes.append({
                "text": q["text"],
                "author": q["author"]["name"]
            })

# Сохраняем
df = pd.DataFrame(all_quotes)
df.to_csv("api_dataset.csv", index=False, encoding="utf-8-sig")

elapsed = time.perf_counter() - t0
print(f"Собрано через API: {len(df)} записей.")
print(f"Время выполнения через API: {elapsed:.2f} секунд.")