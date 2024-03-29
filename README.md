# tparse
Web telegram client with API interface. Python + FastAPI + Telethon.

## Описание работы клиента
1. Логин клиента по QR-коду (двухфакторная на данный момент не поддерживается)
2. Возможность чтения последних 50 сообщений с запрашиваемым пользователем
3. Возможность отправки текстовых сообщений

## Описание работы бота
1. Бот принимает запросы на сбор данных с маркетплэйсов в формате "wild: любой товар", где "wild" - название маркетплейса, а "любой товар" - запрос для поиска. На данный момент поддерживается только Wildberries

## Инстукция по установке
1. Клонируйте репозиторий
2. Перейдите в директорию ```infra```
```
git clone https://github.com/firepanda70/tparse
cd tparse/infra
```
3. Создайте файл .env и заполните его данными. Пример запроления в файле .env.example
4. Запустите сборку контейнеров
```
docker compose up -d --build
```
5. Изнутри контейнера ```web``` запустите миграции в бд
```
alembic upgrade head
```

Документация Swagger будет доступна на [localhocs/docs](http://localhost/docs#/)

### Технологии
- Python 3.12
- FastAPI
- SQLAlchemy
- Telethon
