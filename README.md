# history-quiz-bot

A quiz bot that helps recruit interns to the historical museum.

### How to prepare

- Get files with questions and answers
- Sign up at [Redis](https://redislabs.com) and create a database
- Create Telegram bot through [BotFather](https://telegram.me/BotFather)
- Create VK club, enable messages and bot features in it

### How to install

Python3 should be already installed.

Download the repository:
```commandline
git clone https://github.com/Katsutami7moto/history-quiz-bot.git
cd history-quiz-bot
```

Then use `pip` (or `pip3`, if there is a conflict with Python2) to install dependencies:
```commandline
pip install -r requirements.txt
```

Then, configure environment variables:

1. Go to the project directory and create a file with the name `.env` (yes, it has only the extension). This file will contain environment variables that usually store data unique to each user, thus you will need to create your own.
2. Copy and paste this to `.env` file:
```dotenv
TELEGRAM_BOT_TOKEN='{telegram_token}'
VK_CLUB_TOKEN='{vk_club_token}'
QUESTIONS_DIR='{questions_dir}'
DB_ADDRESS='{redis_db_address}'
DB_PORT={redis_db_port}
DB_USERNAME='{redis_db_username}'
DB_PASSWORD='{redis_db_password}'
```
3. Replace `{telegram_token}` with API token for the Telegram bot you have created with the help of [BotFather](https://telegram.me/BotFather). This token will look something like this: `958423683:AAEAtJ5Lde5YYfkjergber`.
4. Replace `{vk_club_token}` with token of VK club you have created; token is created here: https://vk.com/club{club_id}?act=tokens  Token should have permissions to manage the club and use messages.
5. Replace `{questions_dir}` with path to directory with txt files (in `KOI8-R` encoding) of questions and answers. There is `test-questions` directory in this repository as an example (and for Heroku-deployed bots examples).
6. Replace `redis_db_` parts with credentials from settings of Redis database you have created. `{redis_db_address}` and `{redis_db_port}` are divided by `:`.

### How to use

For Telegram, start chat with the bot you have created. Then run the script with this command:
```commandline
python3 tg_bot.py
```

For VK bot, execute this command:
```commandline
python3 vk_bot.py
```

### How to deploy

1. Fork this repository.
2. Sign up at [Heroku](https://id.heroku.com/login).
3. Create [an app](https://dashboard.heroku.com/new-app) at Heroku; choose `Europe` region.
4. [Connect](https://dashboard.heroku.com/apps/{your-heroku-app-name}/deploy/github) forked GitHub repository.
5. Go to [Settings](https://dashboard.heroku.com/apps/{your-heroku-app-name}/settings) and set `Config Vars` from previously described environment variables, putting each name to `KEY` and value to `VALUE`, e.g. `TELEGRAM_BOT_TOKEN` to `KEY` and `{telegram_token}` (here it should be without `' '` quotation marks) to `VALUE`.
6. Go to [Deploy](https://dashboard.heroku.com/apps/{your-heroku-app-name}/deploy/github) section, scroll to bottom, to `Manual Deploy`, be sure to choose `main` branch and click `Deploy Branch` button.
7. Bot should start working, but just in case check the [logs](https://dashboard.heroku.com/apps/{your-heroku-app-name}/logs) of the app. At the end it should look something like this:
```
2022-07-25T12:52:42.000000+00:00 app[api]: Build succeeded
2022-07-25T12:52:42.153483+00:00 heroku[bot.1]: Stopping all processes with SIGTERM
2022-07-25T12:52:42.338522+00:00 heroku[bot.1]: Process exited with status 143
2022-07-25T12:52:42.793206+00:00 heroku[bot.1]: Starting process with command `python3 main.py`
2022-07-25T12:52:43.389877+00:00 heroku[bot.1]: State changed from starting to up
```

### Working examples

- [Telegram](https://t.me/dvmn87_quiz_bot)
- [VK](https://vk.com/im?sel=-215777705)

### Project Goals

The code is written for educational purposes on online-course for web-developers [dvmn.org](https://dvmn.org/).
