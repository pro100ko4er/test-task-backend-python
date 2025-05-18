import requests
from bs4 import BeautifulSoup
import csv
import time
from collections import defaultdict
import unittest
from unittest.mock import patch


BASE_URL = 'https://ru.wikipedia.org'
START_URL = f'{BASE_URL}/wiki/Категория:Животные_по_алфавиту'

def get_animals_by_letter():
    url = START_URL
    counts = defaultdict(int)

    while url:
        print(f'Обрабатываем: {url}')
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        # Получаем список животных на странице
        for li in soup.select('#mw-pages .mw-category li'):
            title = li.get_text().strip()
            if title:
                first_letter = title[0].upper()
                counts[first_letter] += 1

        # Переход на следующую страницу (если есть)
        next_link = soup.select_one('a:contains("Следующая страница")')
        if not next_link:
            next_link = soup.select_one('a:contains("След.")')

        if next_link:
            url = BASE_URL + next_link['href']
            time.sleep(0.5)  # пауза между запросами, чтобы не нагружать сервер
        else:
            url = None

    return counts

def save_counts_to_csv(counts, filename='beasts.csv'):
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        for letter in sorted(counts):
            writer.writerow([letter, counts[letter]])

if __name__ == '__main__':
    counts = get_animals_by_letter()
    save_counts_to_csv(counts)
    print(f'Готово! Сохранено в beasts.csv')


FAKE_HTML_PAGE_1 = '''
<div id="mw-pages">
  <div class="mw-category">
    <ul>
      <li><a href="/wiki/Аист">Аист</a></li>
      <li><a href="/wiki/Бобр">Бобр</a></li>
      <li><a href="/wiki/Бегемот">Бегемот</a></li>
    </ul>
  </div>
</div>
<a href="/wiki/Категория:Животные_по_алфавиту?page=2">Следующая страница</a>
'''

FAKE_HTML_PAGE_2 = '''
<div id="mw-pages">
  <div class="mw-category">
    <ul>
      <li><a href="/wiki/Волк">Волк</a></li>
      <li><a href="/wiki/Верблюд">Верблюд</a></li>
    </ul>
  </div>
</div>
'''

class TestBeastCounter(unittest.TestCase):

    @patch('beast_counter.requests.get')
    def test_get_animals_by_letter(self, mock_get):
        # Подмена responses от requests.get
        mock_get.side_effect = [
            # Первый вызов — первая страница
            type('Response', (object,), {'text': FAKE_HTML_PAGE_1}),
            # Второй вызов — вторая страница
            type('Response', (object,), {'text': FAKE_HTML_PAGE_2}),
        ]

        result = get_animals_by_letter()

        expected = {
            'А': 1,
            'Б': 2,
            'В': 2
        }

        self.assertEqual(result, expected)

if __name__ == '__main__':
    unittest.main()