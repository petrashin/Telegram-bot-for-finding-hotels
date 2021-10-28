## Telegram bot for site analysis Hotels.com and search for suitable hotels for the user

***

### Setting up the bot:

1) To start working with the bot, you need to download the project folder to your computer
2) Open the terminal and install all the necessary dependencies using the pip install -r command requirements.txt
3) Before running the script, you need to create locally a file .env in which you have to write the token of your telegram bot and the rapidapi key (this can be done by using the env.example file)
4) Next you will need to run main script, using the python main.py command from the project folder
5) After running the script, you need to go to the chat with the bot (BotFather will give you a link to it while creating the bot)
6) After passing all the previous stages, the bot will be configured and ready to work

***

### Interaction with the bot:

1) Command **/lowprice** - find out the top cheapest hotels in the city
2) Command **/high price** - find out the top most expensive hotels in the city
3) Command **/best deal** - find out the top hotels most suitable for price and location from the center
4) Command **/history** - find out the history of hotel search

***

### Description of the work of the commands:

#### Command /lowprice
After entering the command, the user is asked:
1) The city where the search will be conducted.
2) The number of hotels that need to be displayed as a result (no more
than a predetermined maximum).
3) The need to upload and display photos for each hotel ("Yes/No").
  * If the answer is positive, the user also enters the number of required photos (no more than a predetermined maximum)

#### Command /highprice
After entering the command, the user is asked:
1) The city where the search will be conducted.
2) The number of hotels that need to be displayed as a result (no more
than a predetermined maximum).
3) The need to upload and output photos for each hotel ("Yes/No")
  * If the answer is positive, the user also enters the number of necessary photos (no more than a predetermined maximum)

#### Command /bestdeal
After entering the command, the user is asked:
1) The city where the search will be conducted.
2) Price range.
3) The range of the distance at which the hotel is located from the center.
4) The number of hotels that need to be displayed as a result (no more
than a predetermined maximum).
5) The need to upload and output photos for each hotel ("Yes/No")
  * If the answer is positive, the user also enters the number of necessary photos (no more than a predetermined maximum)

#### Command /history
After entering the command, the user is shown the search history of hotels. The story itself contains:
1) The command that the user entered.
2) The date and time when the command was entered.
3) Hotels that were found.
