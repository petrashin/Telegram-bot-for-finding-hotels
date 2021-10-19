## Telegram-бот для анализа сайта Hotels.com и поиска подходящих пользователю отелей

***

### Настройка бота:

1) Для начала работы с ботом необходимо скачать папку проекта к себе на компьютер
2) Открыть терминал, и запустить скрипт main.py с помощью команды python main.py из папки проекта
3) Перейти по [ссылке](https://t.me/find_hotels_my_bot) и запустить бота
4) После прохождения трех предыдущих этапов бот будет настроен и готов к работе

***

### Взаимодействие с ботом:

1) Команда **/lowprice** - узнать топ самых дешёвых отелей в городе
2) Команда **/highprice** - узнать топ самых дорогих отелей в городе
3) Команда **/bestdeal** - узнать топ отелей, наиболее подходящих по цене и расположению от центра
4) Команда **/history** - узнать историю поиска отелей

***

### Описание работы команд:

#### Команда /lowprice
После ввода команды у пользователя запрашивается:
1) Город, где будет проводиться поиск. 
2) Количество отелей, которые необходимо вывести в результате (не больше
заранее определённого максимума). 
3) Необходимость загрузки и вывода фотографий для каждого отеля (“Да/Нет”). 
   * При положительном ответе пользователь также вводит количество необходимых фотографий (не больше заранее определённого максимума)

#### Команда /highprice
После ввода команды у пользователя запрашивается:
1) Город, где будет проводиться поиск.
2) Количество отелей, которые необходимо вывести в результате (не больше
заранее определённого максимума).
3) Необходимость загрузки и вывода фотографий для каждого отеля (“Да/Нет”)
   * При положительном ответе пользователь также вводит количество необходимых фотографий (не больше заранее определённого максимума)

#### Команда /bestdeal
После ввода команды у пользователя запрашивается:
1) Город, где будет проводиться поиск.
2) Диапазон цен.
3) Диапазон расстояния, на котором находится отель от центра.
4) Количество отелей, которые необходимо вывести в результате (не больше
заранее определённого максимума).
5) Необходимость загрузки и вывода фотографий для каждого отеля (“Да/Нет”)
   * При положительном ответе пользователь также вводит количество необходимых фотографий (не больше заранее определённого максимума)

#### Команда /history
После ввода команды пользователю выводится история поиска отелей. Сама история содержит:
1) Команду, которую вводил пользователь.
2) Дату и время ввода команды.
3) Отели, которые были найдены.