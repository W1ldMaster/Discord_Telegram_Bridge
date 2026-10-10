# Discord ↔ Telegram Bridge

Бот-мост для пересылки сообщений между Discord и Telegram.

## ✨ Возможности

- 📨 Пересылка текстовых сообщений в обе стороны
- 📎 Поддержка вложений (фото, видео, гифки)
- 🎭 Пересылка эмодзи и форматирования
- 🔄 Автоматическая пересылка без задержек

## ⚙️ Требования

- [Docker Desktop](https://www.docker.com/products/docker-desktop/) (Windows, macOS, Linux)
- Токен Discord-бота
- Токен, Хэш и Айди Telegram-бота
- ID канала Discord и ID чата Telegram

## 📥 Установка

### 1. Склонируйте репозиторий

```bash
git clone https://github.com/W1ldMaster/Discord_Telegram_Bridge.git
cd Discord_Telegram_Bridge
```

### 2. Получите токены и ID

**Discord:**
- Токен бота: [Discord Developer Portal](https://discord.com/developers/applications) → Ваше приложение → Bot → Token
- ID канала и сервера: включите режим разработчика в Discord → правой кнопкой по каналу/серверу → «Копировать ID»

**Telegram:**
- Токен бота: [@BotFather](https://t.me/BotFather) → `/newbot`
- API_ID и API_HASH: [my.telegram.org](https://my.telegram.org) → API Development Tools
- ID чата: добавьте бота [@getmyid_bot](https://t.me/getmyid_bot) в группу

### 3. Измение файл `.envexample`

Переименуйте `.envexample` в `.env` и заполните своими данными:

```env
DISCORD_TOKEN=ваш_токен_дискорд_бота
TELEGRAM_TOKEN=ваш_токен_телеграм_бота
TELEGRAM_CHAT=ID_чата_телеграм
DISCORD_CHANNEL=ID_канала_дискорд
DISCORD_GUILD=ID_сервера_дискорд
API_ID=ваш_api_id
API_HASH=ваш_api_hash
```

### 4. Соберите Docker-образ

```bash
docker build -t discord-telegram-bot .
```

### 5. Запустите контейнер

**Windows (PowerShell):**
```powershell
docker run -v ${PWD}/.env:/Project/.env discord-telegram-bot
```

**Linux / macOS:**
```bash
docker run -v ${pwd}/.env:/Project/.env discord-telegram-bot
```

## 📋 Управление

```bash
# Посмотреть логи
docker logs -f

# Остановить бота
docker stop

# Запустить снова
docker start

# Перезапустить
docker restart

# Удалить контейнер
docker rm
```

## 🔄 Автозапуск при перезагрузке

Чтобы бот автоматически запускался после перезагрузки компьютера, добавьте флаг `--restart unless-stopped`:

```bash
docker run --restart unless-stopped -v ${PWD}/.env:/Project/.env discord-telegram-bot
```

## 🛠️ Устранение неполадок

| Проблема | Решение |
|----------|---------|
| `Cannot connect to Docker daemon` | Запустите Docker Desktop |
| `Improper token has been passed` | Проверьте токены в `.env` |
| Бот не отвечает | Проверьте логи: `docker logs my-bot` |
| Сообщения не пересылаются | Проверьте ID каналов и чатов |

## 📁 Структура проекта

```
discord-telegram-bridge/
├── Dockerfile
├── .dockerignore
├── requirements.txt
├── .env
├── .gitignore
├── README.md
└── Project/
    ├── main.py
    ├── discord_bot.py
    ├── tg.py
    ├── qprocessor.py
    └── main_bridge.py
```
