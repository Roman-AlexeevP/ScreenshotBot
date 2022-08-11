## Бот для отображения скриншота веб-страницы по ее адресу

Сервис для отображения страницы по ее URL-адресу. 

Пример ссылки: `http://wikipedia.org`
## Используемые технологии

- aiogram
- pyppeteer

## Процесс загрузки проекта

1. `git clone https://github.com/Roman-AlexeevP/ScreenshotBot.git`
2. `cd ScreenshotBot`
3. Заполнение .env по примеру **.env.example**
4. Создайте каталоги redis_data и redis_config, в последнем создайте свой конфиг redis.conf по примеру **redis.conf.example**
5. Создайте каталог /pg/data
6. `docker-compose up -d`