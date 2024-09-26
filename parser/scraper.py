import csv
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

# Настройка логгирования
logging.basicConfig(level=logging.INFO)

# URL сайта с резюме
URL = "https://robota.ua/candidates/all/ukraine"

# Селекторы для извлечения данных
SELECTORS = {
    'desired_position': ".santa-m-0.santa-mb-10.santa-typo-regular-bold",
    'years_of_experience': ".santa-text-black-500.santa-whitespace-nowrap.ng-star-inserted",
    'skills': ".skills-selector",  # Замените на актуальный селектор для навыков
    'location': ".santa-typo-secondary.santa-truncate",
    'desired_salary': ".desired-salary-selector"  # Замените на актуальный селектор для желаемой зарплаты
}

# Функция для извлечения данных из одного резюме
def extract_resume_data(resume_element):
    try:
        desired_position = resume_element.find_element(By.CSS_SELECTOR, SELECTORS['desired_position']).text
        years_of_experience = resume_element.find_element(By.CSS_SELECTOR, SELECTORS['years_of_experience']).text
        skills = resume_element.find_element(By.CSS_SELECTOR, SELECTORS['skills']).text
        location = resume_element.find_element(By.CSS_SELECTOR, SELECTORS['location']).text
        desired_salary = resume_element.find_element(By.CSS_SELECTOR, SELECTORS['desired_salary']).text

        return {
            'Desired Position': desired_position,
            'Years of Experience': years_of_experience,
            'Skills': skills,
            'Location': location,
            'Desired Salary': desired_salary
        }
    except Exception as e:
        logging.warning(f"Ошибка при извлечении данных: {e}")
        return None

# Функция для записи данных в CSV файл
def write_data_to_csv(data):
    try:
        with open('resumes.csv', mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(["Desired Position", "Years of Experience", "Skills", "Location", "Desired Salary"])
            writer.writerows(data)

        # Логирование успешной записи данных
        logging.info("Данные успешно записаны в файл resumes.csv")

    except Exception as e:
        # Логирование ошибки, если запись не удалась
        logging.error(f"Ошибка при записи данных в файл resumes.csv: {e}")

# Настройка веб-драйвера
def setup_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Запуск в фоновом режиме
    service = Service(ChromeDriverManager().install())
    return webdriver.Chrome(service=service, options=options)

# Основная функция парсинга
def main():
    driver = setup_driver()
    driver.get(URL)
    time.sleep(5)  # Ждем загрузки страницы

    logging.info("Извлечение данных с текущей страницы...")

    resume_elements = driver.find_elements(By.CSS_SELECTOR, ".cv-card")  # Замените на актуальный селектор
    print("RESUME_EXTRACTS", resume_elements)
    for resume in resume_elements:
        data = extract_resume_data(resume)
        if data:
            write_data_to_csv(data)

    driver.quit()
    logging.info("Парсинг завершён.")

if __name__ == "__main__":
    main()
