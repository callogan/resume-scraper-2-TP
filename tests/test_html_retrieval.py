import logging
from selenium import webdriver
from selenium.common.exceptions import WebDriverException

# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

BASE_URL = "https://robota.ua/candidates/all/ukraine"  # Замените на нужный URL


def test_html_content():
    logging.info("Запуск теста на извлечение HTML-кода.")
    try:
        with webdriver.Chrome() as driver:
            logging.info(f"Переход по URL: {BASE_URL}")
            driver.get(BASE_URL)

            # Ждем, чтобы страница полностью загрузилась (можно настроить время)
            driver.implicitly_wait(10)

            content = driver.page_source  # Извлечение HTML-кода страницы


            if content:
                # Write HTML-code to the file
                filename = f"resumes.html"
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(content)
                # Логируем успешную загрузку страницы
                logging.info("HTML-код страницы успешно извлечён.")
                print("HTML-код загружен успешно!")

                # Вывод первых 500 символов для проверки
                print("Первый фрагмент HTML-кода:\n", content[:500])
            else:
                print("Не удалось загрузить контент!")

    except WebDriverException as e:
        # Логирование ошибок веб-драйвера
        logging.error(f"Ошибка при работе с веб-драйвером: {e}", exc_info=True)
    except Exception as e:
        # Логирование любых других ошибок
        logging.error(f"Произошла ошибка: {e}", exc_info=True)


if __name__ == "__main__":
    test_html_content()