from playwright.sync_api import sync_playwright

with sync_playwright() as pw:
    # Запускаем браузер в headless-режиме
    browser = pw.chromium.launch(headless=True)
    
    # Создаем контекст (эмуляция обычного браузера)
    context = browser.new_context(
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36",
        viewport={"width": 1366, "height": 900}
    )
    page = context.new_page()
    
    print("Открываем страницу...")
    page.goto("https://quotes.toscrape.com/scroll", wait_until="domcontentloaded")
    
    # Ждем, пока на странице появятся первые цитаты
    page.wait_for_selector("div.quote", state="visible", timeout=10000)
    
    print(f"Заголовок: {page.title()}")
    print("Первые элементы загружены успешно!")
    
    browser.close()
