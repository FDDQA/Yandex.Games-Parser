from selenium import webdriver
from selenium.webdriver.common.by import By

#собираем значения из популярных
driver = webdriver.Chrome()
driver.get("https://yandex.ru/games/category/editors_choice")
res_pop = driver.find_elements(By.CSS_SELECTOR, ".game-card__title")
print("Популярные игры:")
for element in res_pop:
        print(element.text)
#собираем значения из новых
driver.get("https://yandex.ru/games/category/new")
res_pop = driver.find_elements(By.CSS_SELECTOR, ".game-card__title")
print("\nНовые игры:")
for element in res_pop:
        print(element.text)