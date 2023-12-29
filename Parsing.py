import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

def save_images(url):
    # Запрос к странице
    response = requests.get(url)

    # Проверка успешности запроса
    if response.status_code != 200:
        print("Ошибка при загрузке страницы")
        return

    # Использование BeautifulSoup для парсинга HTML
    soup = BeautifulSoup(response.text, "html.parser")

    # Создание папки "Images" (если она еще не существует)
    os.makedirs("Images", exist_ok=True)

    # Получение всех <img> тегов со страницы
    img_tags = soup.find_all("img")

    # Сохранение изображений в папку "Images"
    for img_tag in img_tags:
        # Получение URL изображения
        img_url = urljoin(url, img_tag["src"])

        # Загрузка изображения
        img_response = requests.get(img_url)

        # Проверка успешности запроса и сохранение изображения
        if img_response.status_code == 200:
            # Получение имени файла из URL
            img_filename = os.path.basename(urlparse(img_url).path)

            # Путь к сохраняемому файлу
            save_path = os.path.join("Images", img_filename)

            # Сохранение изображения
            with open(save_path, "wb") as img_file:
                img_file.write(img_response.content)

            print(f"Изображение сохранено: {img_url}")
        else:
            print(f"Ошибка при загрузке изображения: {img_url}")


# Пример использования
url = input("Введите URL страницы: ")
save_images(url)