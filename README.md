# TechZone

---

## Настройка проекта

1. Клонировать проект:

```bash
git clone git@github.com:BrokenError/DiplomaProject.git
```

2. Создать `.env` файл (вы можете скопировать `.env.example` и ввести свои данные):

```bash
cp .env.example .env
```

---

## Запуск проекта

### Локально с помощью docker-compose

#### Выполните эти команды в терминале:

1. Закомментировать строки, которые нужны для https
   1. Перейдите в нужный файл
   ```bash
   nano src/main.py
   ```
   2. Закомментируйте строки 100 и 101

2. Выполнить следующие команды
```bash
docker network create "techzone"
docker-compose build
docker-compose up -d
```

#### На сервере с помощью docker-compose:
```bash
docker network create "techzone"
docker-compose build
docker-compose up -d
docker exec nginx_techzone certbot --nginx --agree-tos  \
--email "ваша почта" -d "ваш домен"
docker exec nginx_techzone certbot install --cert-name "ваше название сертификата"
```

