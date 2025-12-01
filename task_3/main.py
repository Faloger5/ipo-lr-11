import requests  # Импортируем библиотеку requests для выполнения HTTP-запросов
from bs4 import BeautifulSoup  # Импортируем BeautifulSoup для парсинга HTML-страниц
import json  # Импортируем json для сохранения данных в файл
from urllib.parse import urljoin  # Импортируем urljoin для правильного объединения URL-адресов

def get_quotes_from_page(url):  # Объявляем функцию для сбора цитат с страницы, принимает URL
    all_quotes = []  # Создаем список для хранения всех цитат
    quote_number = 1  # Инициализируем счетчик цитат для нумерации

    while url:  # Пока есть URL (пока есть страница для обработки)
        headers = {  # Определяем заголовки для HTTP-запроса
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                          "AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/58.0.3029.110 Safari/537.3"  # Имитация браузера
        }
        response = requests.get(url, headers=headers)  # Отправляем GET-запрос по текущему URL с заголовками
        if response.status_code != 200:  # Если ответ не 200 OK
            print("Ошибка загрузки страницы")  # Выводим сообщение об ошибке
            break  # Выходим из цикла, прерывая обработку
        soup = BeautifulSoup(response.text, 'html.parser')  # Создаем объект BeautifulSoup для парсинга HTML
        quote_blocks = soup.find_all("div", class_="quote")  # Находим все блоки цитат на странице

        for block in quote_blocks:  # Проходим по каждому блоку цитаты
            text = block.find("span", class_="text").get_text(strip=True)  # Извлекаем текст цитаты, очищая лишние пробелы
            all_quotes.append({"number": quote_number, "quote": text})  # Добавляем цитату с ее номером в список
            quote_number += 1  # Увеличиваем счетчик цитат

        next_btn = soup.find('li', class_='next')  # Ищем кнопку "следующая" страница
        if next_btn and next_btn.a:  # Если кнопка есть и есть ссылка внутри
            url = urljoin(url, next_btn.a['href'])  # Обновляем URL на следующую страницу
        else:  # Если кнопки или ссылки нет, значит это последняя страница
            url = None  # Устанавливаем url в None, чтобы завершить цикл

    return all_quotes  # Возвращаем список собранных цитат

def save_quotes(quotes, filename="data.json"):  # Объявляем функцию для сохранения цитат в файл
    with open(filename, 'w', encoding='utf-8') as f:  # Открываем файл для записи с указанной кодировкой
        json.dump(quotes, f, ensure_ascii=False, indent=2)  # Записываем список цитат в JSON файл с отступами

if __name__ == '__main__':  # Проверка, что скрипт запущен напрямую, а не импортирован
    start_url = 'https://quotes.toscrape.com/'  # Начальный URL для парсинга
    quotes = get_quotes_from_page(start_url)  # Вызываем функцию сбора цитат
    save_quotes(quotes, filename='data.json')  # Сохраняем в JSON файл
