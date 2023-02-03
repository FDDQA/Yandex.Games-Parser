from selenium import webdriver
from selenium_stealth import stealth
from selenium.webdriver.common.by import By
import time

driver = webdriver.Chrome()
# stealth(driver,
#         languages=["en-US","en"],
#         vendor="Google Inc.",
#         platform="Win32",
#         webgl_vendor="Intel Inc.",
#         render="Inter Iris OpenGL Engine",
#         fix_hairline=True,
#         )
driver.get("https://yandex.ru/games/category/editors_choice")
res_pop = driver.find_elements(By.CSS_SELECTOR, ".game-card__title")
print("Популярные игры:")
i=0
for element in res_pop:
        res_pop[i].click()
        driver.back()
        i=i+1
        #print(element.text)




driver.get("https://yandex.ru/games/category/new")
res_pop = driver.find_elements(By.CSS_SELECTOR, ".game-card__title")
print("\nНовые игры:")
for element in res_pop:
        print(element.text)