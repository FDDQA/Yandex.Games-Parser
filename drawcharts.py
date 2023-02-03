import pymysql
from config import host, user, password, db_name
from datetime import datetime, timedelta
from gpcharts import figure

class Game_item:
    def __init__(self,name,category,date):
        self.name = name
        self.category = category
        self.date = date

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
cursor.execute( "SELECT date, countplayers, app_id  FROM dateandplayers")
dateandplayers_db = cursor.fetchall()

connection.commit()
connection.close()

game_list=[]
arr2=[]
# перебор элементов массива (первая таблица)
# for elem in nameandcat_db:
#     arr1.append(elem['name'])
#     arr1.append(elem['category'])
#     arr2.clear()
#     # перебор элементов массива (вторая таблица)
#     for dateandcountplayers in dateandplayers_db:
#         if elem['app_id'] == dateandcountplayers['app_id']:
#             arr2.append((dateandcountplayers['date'], dateandcountplayers['countplayers']))
#     arr1.append(arr2)

for elem in nameandcat_db:
    game = Game_item(elem['name'],elem['category'],[])
    dates = []
    # перебор элементов массива (вторая таблица)
    for dateandcountplayers in dateandplayers_db:
        if elem['app_id'] == dateandcountplayers['app_id']:
            game.date.append((dateandcountplayers['date'], dateandcountplayers['countplayers']))

    #print(game.name,game.category,game.date)
    game_list.append(game)
names=[]
number_players=[]
count_players1=[]
for elem in game_list:
    names.append(elem.name)
    count_players = []
    for elem1 in elem.date:
        count_players.append(elem1[1])
    number_players.append(count_players)
i=0
for counter in number_players[0]:
    count_players1.append([])
    for elem in number_players:
        count_players1[i].append(int(elem[i].replace(' ','')))
    if i<14:
        i+=1

xVals=[]

i=0
while i < len(count_players1):
    x = (datetime.today() - timedelta(days=i)).strftime("%Y-%m-%d")
    xVals.append(x)
    i+=1
xVals.reverse()
xVals.insert(0,'Dates')


print("Игр в базе:",len(names))
fig = figure(title='TEST',height=1080, width=1920)
yVals=[names,*count_players1]
fig.plot(xVals,yVals)