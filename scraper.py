import requests
from bs4 import BeautifulSoup
import json

# Определяем список ключевых слов:
KEYWORDS = ['дизайн', 'фото', 'web', 'python']

headers = {
"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

# Отправляем запрос и получаем HTML
response = requests.get("https://habr.com/ru/articles/",  headers=headers, timeout=5)
print(response.status_code)

# Парсим HTML
soup = BeautifulSoup(response.text, 'html.parser')

# Находим все статьи с помощью CSS-селектора
articles = soup.select('article.tm-articles-list__item')

# Список для хранения найденных статей
found_articles = []

for article in articles:
    # Извлекаем заголовок и ссылку
    title_element = article.select_one('h2.tm-title a.tm-title__link')
    if not title_element:
        continue

    title = title_element.text.strip()
    link = title_element.get('href')

    # Добавляем базовый URL если ссылка относительная
    if link and not link.startswith('http'):
        link = 'https://habr.com' + link

    # Извлекаем дату публикации
    time_element = article.select_one('time')
    date = time_element.get('title') if time_element else 'Неизвестно'

    # Извлекаем preview-информацию
    preview_element = article.select_one('div.tm-article-body, div.article-formatted-body')
    preview_text = preview_element.text.strip().lower() if preview_element else ''

    # Проверяем наличие ключевых слов в заголовке
    title_lower = title.lower()

    # Находим какие именно ключевые слова найдены
    found_keywords = [keyword for keyword in KEYWORDS
                      if keyword.lower() in title_lower or keyword.lower() in preview_text]

    # Если найдено хотя бы одно ключевое слово - добавляем в список
    if found_keywords:
        article_data = {
            'date': date,
            'title': title,
            'link': link,
            'preview': preview_text,
            'found_keywords': found_keywords
        }
        found_articles.append(article_data)

        # Выводим в консоль
        print(f'{date} – {title} – {link}')

# Сохраняем в JSON файл
with open('habr_articles.json', 'w', encoding='utf-8') as f:
    json.dump(found_articles, f, ensure_ascii=False, indent=2)

print(f"\nНайдено статей: {len(found_articles)}")
print("Результаты сохранены в файл: habr_articles.json")