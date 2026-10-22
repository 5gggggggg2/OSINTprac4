from playwright.sync_api import sync_playwright
import pandas as pd
import time


def run():
    t0 = time.perf_counter();
    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=True)
        page = browser.new_page()

        print("Открываем страницу...")
        page.goto("https://quotes.toscrape.com/scroll", wait_until="domcontentloaded")

        # Явное ожидание первой загрузки
        page.wait_for_selector("div.quote", state="visible", timeout=10000)

        previous_count = 0
        stable_rounds = 0
        max_rounds = 20

        for round_num in range(max_rounds):
            # Прокрутка
            page.mouse.wheel(0, 5000)

            try:
                # Ждем прироста элементов
                page.wait_for_function(
                    "prev => document.querySelectorAll('div.quote').length > prev",
                    arg=previous_count,
                    timeout=3000
                )
            except Exception:
                pass

            current_count = page.eval_on_selector_all("div.quote", "els => els.length")
            print(f"Круг {round_num + 1}: элементов на странице {current_count}")

            if current_count == previous_count:
                stable_rounds += 1
                if stable_rounds >= 3:
                    print("Подгрузка завершена (количество элементов стабилизировалось).")
                    break
            else:
                stable_rounds = 0

            previous_count = current_count

            # используем встроенный таймаут Playwright вместо time.sleep
            page.wait_for_timeout(500)

            # Извлечение данных
        print("Извлекаем данные...")
        all_quotes = []
        cards = page.query_selector_all("div.quote")
        for card in cards:
            text = card.query_selector("span.text").inner_text().strip()
            author = card.query_selector("small.author").inner_text().strip()
            all_quotes.append({"text": text, "author": author})

        browser.close()

        df = pd.DataFrame(all_quotes)
        df = df.drop_duplicates().reset_index(drop=True)
        df.to_csv("dynamic_page_dataset.csv", index=False, encoding="utf-8-sig")
        print(f"\nСохранено {len(df)} уникальных записей.")
        elapsed = time.perf_counter() - t0
        print(f"Время выполнения: {elapsed:.2f} секунд.")


if __name__ == "__main__":
    run()