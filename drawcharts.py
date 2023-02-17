import pymysql
from config import host, user, password, db_name
from datetime import datetime, timedelta
import gpcharts


class GameItem:
    def __init__(self, name, category, date):
        self.name = name
        self.category = category
        self.date = date


def generate_dates(date):
    xVals = []
    i = 0
    while i < 14:
        x = (date - timedelta(days=i)).strftime("%Y-%m-%d")
        xVals.append(x)
        i += 1
    xVals.reverse()
    return xVals


# коннектимся к базе
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

cursor = connection.cursor()

# собираем все данные с первой таблицы
cursor.execute("SELECT app_id, name, category  FROM nameandcat")
nameandcat_db = cursor.fetchall()

# собираем все данные со второй таблицы
cursor.execute("SELECT date, countplayers, app_id  FROM dateandplayers")
dates_players_db = cursor.fetchall()

connection.commit()
connection.close()
# дальше уже не трогаем базу

game_list = []
for elem in nameandcat_db:
    game = GameItem(elem['name'], elem['category'], {})
    # перебор элементов массива (вторая таблица)
    for dateandcountplayers in dates_players_db:
        if elem['app_id'] == dateandcountplayers['app_id']:
            game.date[(dateandcountplayers['date'])] = int(dateandcountplayers['countplayers'])
    if sum(game.date.values()) < 10000:
        continue
    game_list.append(game)

# создаем массив под запись количества игроков на 14 дней
count_players = []
while 14 != len(count_players):
    count_players.append([])

massiv = generate_dates(datetime.today())
names = []  # массив только имён
for game in game_list:  # берём одну игру из массива с играми
    names.append(game.name)  # запихиваем все имена в массив имён names

i = 13
while i > -1:
    for game in game_list:  # берём одну игру из массива с играми
        if game.date.get((massiv[i])) is None:
            count_players[i].append(0)
        elif game.date.get((massiv[i])) > 10000:
            count_players[i].append((game.date.get(massiv[i])))
        else:
            count_players[i].append(0)
    i -= 1

massiv.insert(0, 'Dates')  # вставляем xlabel
fig = gpcharts.figure(title='Parsing', width=1200, height=600)
yVals = [names, *count_players]
print(yVals)

# рисуем
fig.plot(massiv, yVals)
