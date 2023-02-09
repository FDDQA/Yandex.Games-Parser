from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions
import pymysql # для работы с базой
from config import host, user, password, db_name
from datetime import datetime # получаем текущую дату
from tqdm import tqdm # прогресс-бар
import time
import concurrent.futures

import chromedriver_autoinstaller
chromedriver_autoinstaller.install()

# подключение к базе
try:
    connection = pymysql.connect(
        host=host,
        port=3306,
        user=user,
        password=password,
        database=db_name,
        cursorclass=pymysql.cursors.DictCursor
    )
    print("Succesfully connected :)")
    print("_" * 40)
except Exception as ex:
    print("Connect refused :(")
    print(ex)

# очистка таблицы перед работой
cursor = connection.cursor()
try:
    # cursor.execute("DROP TABLE nameandcat")
    # cursor.execute("DROP TABLE dateandplayers")
    print("Удалил таблицы nameandcat и dateandplayers")
except Exception as ex:
    print("Ошибка удаления!Таблицы отсутствуют")
    print(ex)

# отключаем GUI, загрузку картинок
options = Options()
options.add_argument("--headless=new")
options.add_argument("--blink-settings=imagesEnabled=false")

# объявляем драйвер Хрома, грузим страницу с играми, объявляем неявное ожидание загрузки драйвера 2 сек
driver = webdriver.Chrome(options=options)
driver.get("https://yandex.ru/games/category/new")

# скролим страницу до самого низа
match = False
lastCount, lenOfPage = 0, 0
print("Проматываю страницу за вас. Подождите...")
while(match == False):
    lastCount = lenOfPage
    time.sleep(2)
    lenOfPage = driver.execute_script("window.scrollTo(0, document.body.scrollHeight);"
                                      "var lenOfPage=document.body.scrollHeight;"
                                      "return lenOfPage;")
    if lastCount == lenOfPage: #Если доскролили до конца
        match = True

# закрываем рекламу, которая блокирует элементы
close_ads = driver.find_element(By.CSS_SELECTOR,'.close-button_type_popup-inner')
close_ads.click()

# собираем все ссылки на игры
page_new_games = driver.find_elements(By.CSS_SELECTOR, ".game-card__game-info")

# создаем список game_cats_list для записи методом find.elements
# т.к. он возвращает список и списки для последующей передачи в таблицы
game_cats_list = []
args_namecat_db = []
args_countplayers_db = []

today = datetime.today().strftime("%d.%m.%Y")

for element in tqdm(page_new_games, desc='Parsing', colour='#00ff00'):
    element.click()
    WebDriverWait(driver=driver, timeout=10).until(expected_conditions.presence_of_element_located((By.CSS_SELECTOR,".game-play-button_size_page_icon_desktop.Button2")))
    game_name = driver.find_element(By.CSS_SELECTOR, '.game-page__title').text
    game_cats = driver.find_elements(By.CSS_SELECTOR, '.category__link.games-link')

    # преобразование WebElements в текст и запись в массив game_cats_list
    for cat in game_cats:
         game_cats_list.append(cat.text)

    # убираем мусорную категорию, которая нам не нужна и есть в каждой игре из новых
    game_cats_list.remove('Новые')

    # берём количество игроков и стрипаем
    game_players = driver.find_element(By.CSS_SELECTOR, '.game-number__number-text').text.strip('+ игроков').strip('+ пользователей')

    # берём ID игры и стрипаем
    game_id = driver.current_url.strip('https://yandex.ru/games/category/new#app=')

    # собираем массив для первой таблицы из ID, названия и категорий игры
    args_namecat_db.append(tuple((game_id, game_name, ', '.join(game_cats_list))))

    # собираем массив для второй таблицы из количества игроков, даты сбора и ID
    args_countplayers_db.append(tuple((game_id, today, game_players)))
    game_cats_list.clear()
    driver.back()
# создаем две таблицы
try:
    cursor.execute("create table nameandcat (ID int NOT NULL AUTO_INCREMENT, APP_ID int(10), NAME char(255), CATEGORY VARCHAR(255),  PRIMARY KEY (ID), UNIQUE(APP_ID))")
    cursor.execute("create table dateandplayers (ID int NOT NULL AUTO_INCREMENT, APP_ID int(10), DATE VARCHAR(10), COUNTPLAYERS VARCHAR (255), PRIMARY KEY(ID))")
except:
    print("Базы уже созданы")
# заливаем все данные в таблицы
cursor.executemany("INSERT IGNORE INTO nameandcat (app_id, name, category) VALUE (%s,%s,%s)", args_namecat_db)
cursor.executemany("INSERT INTO dateandplayers (app_id, date, countplayers) VALUE (%s,%s,%s)", args_countplayers_db)

# вывод нашей таблицы через Pandas
# print(pandas.read_sql("SELECT * FROM nameandcat", connection), pandas.read_sql("SELECT * FROM dateandplayers", connection))

# сохранение и закрытие соединения
connection.commit()
connection.close()

