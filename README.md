## Бот для отображения скриншота веб-страницы по ее адресу

Сервис для отображения страницы по ее URL-адресу.
Команды:
- `/start` (Получение информации о боте и его командах)

Пример ссылки: `http://wikipedia.org`
## Используемые технологии

- **Python 3.9** 
- **aiogram** (Асинхронный фреймворк для создания телеграм-бота)
- **pyppeteer** (Асинхронный порт puppeteer для работы с chromedriver)
- **Docker and Docker Compose** (Контейнеризация);
- **PostgreSQL** (СУБД);
- **Redis** (Хранение состояния бота и кэшированных данных);
- **SQLAlchemy** (ОРМ для Python);
- **Alembic** (Создание миграций для БД);

## Процесс загрузки проекта

1. Склонируйте репозиторий: `git clone https://github.com/Roman-AlexeevP/ScreenshotBot.git`
2. Перейдите в рабочую директорию: `cd ScreenshotBot`
3. Заполнение .env по примеру **.env.example**
4. Создайте каталоги redis_data и redis_config, в последнем создайте свой конфиг redis.conf по примеру **redis.conf.example**
5. Создайте каталог /pg/data
6. Запускайте с помощью команды `docker-compose up -d`