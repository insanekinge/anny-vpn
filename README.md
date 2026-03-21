diff --git a/C:\Users\sokka\OneDrive\Документы\Playground\anny-vpn\README.md b/C:\Users\sokka\OneDrive\Документы\Playground\anny-vpn\README.md
new file mode 100644
--- /dev/null
+++ b/C:\Users\sokka\OneDrive\Документы\Playground\anny-vpn\README.md
@@ -0,0 +1,273 @@
+# AllyVPN
+
+Сейчас AllyVPN состоит из двух слоёв, которые развиваются параллельно:
+
+- существующий Python backend и Telegram-бот в `app/`
+- frontend-monorepo для публичного сайта и Telegram Mini App
+
+Репозиторий организован так, чтобы фронтенд можно было развивать быстро и независимо, не ломая текущий backend с интеграцией через Marzban.
+
+## Стек
+
+- Python 3.12
+- aiogram 3.26.0
+- FastAPI 0.118.0
+- SQLAlchemy 2.0.48
+- React для сайта и Mini App
+- npm workspaces для управления monorepo
+- общие design tokens и web UI-пакеты в `packages/`
+
+## Общее дизайн-направление
+
+- Палитра: `#ffffff`, `#7c4acc`, `#b699e6`, `#0f0d12`, `#2a1c40`
+- Типографика:
+  - Display: `Sora`
+  - Body/UI: `Manrope`
+- Темы:
+  - dark
+  - light
+
+## Структура репозитория
+
+```text
+app/
+  api/
+  bot/
+  core/
+  db/
+  integrations/
+  services/
+apps/
+  website/
+  miniapp/
+packages/
+  design-system/
+  ui-web/
+```
+
+## Переменные окружения backend
+
+Обязательные переменные для бота:
+
+- `BOT_TOKEN`
+- `MARZBAN_BASE_URL`
+- `MARZBAN_USERNAME`
+- `MARZBAN_PASSWORD`
+
+Дополнительные переменные:
+
+- `APP_ENV=production`
+- `BOT_USERNAME=@AllyVPNsbot`
+- `DATABASE_URL=sqlite+aiosqlite:///./allyvpn.db`
+- `MINIAPP_URL=https://your-public-miniapp-url`
+- `SUPPORT_USERNAME=`
+- `ADMIN_TELEGRAM_IDS=123456789,987654321`
+- `LOG_LEVEL=INFO`
+
+## Локальная подготовка
+
+Установка backend:
+
+```powershell
+python -m venv .venv
+.venv\Scripts\Activate.ps1
+python -m pip install -r requirements.txt
+```
+
+Заполни `.env` реальными backend-данными:
+
+```env
+BOT_TOKEN=your_real_token_here
+MARZBAN_BASE_URL=https://your-marzban-host
+MARZBAN_USERNAME=admin_username
+MARZBAN_PASSWORD=admin_password
+MINIAPP_URL=https://your-public-miniapp-url
+ADMIN_TELEGRAM_IDS=your_telegram_id
+```
+
+Токен Telegram нужен только для стороны бота:
+
+- `BOT_TOKEN` нужен, чтобы запускать бота и обновлять кнопку Mini App в Telegram
+- сам frontend Mini App не должен хранить токен бота и не должен его получать
+
+Установка frontend-workspaces:
+
+```powershell
+npm install
+```
+
+## Команды запуска
+
+Запуск Telegram-бота:
+
+```powershell
+python -m app.bot.main
+```
+
+Обновление Telegram-команд и кнопки Mini App без полного запуска backend:
+
+```powershell
+python -m app.bot.sync_telegram_ui
+```
+
+Запуск API:
+
+```powershell
+uvicorn app.api.main:app --reload
+```
+
+Запуск сайта:
+
+```powershell
+npm run dev:website
+```
+
+Стабильный статический preview сайта:
+
+```powershell
+powershell -ExecutionPolicy Bypass -File .\scripts\start-website-static.ps1
+```
+
+Запуск Mini App локально:
+
+```powershell
+npm run dev:miniapp
+```
+
+Стабильный статический preview Mini App:
+
+```powershell
+powershell -ExecutionPolicy Bypass -File .\scripts\start-miniapp-static.ps1
+```
+
+Стабильный статический preview с временным публичным URL:
+
+```powershell
+powershell -ExecutionPolicy Bypass -File .\scripts\start-miniapp-static.ps1 -Public
+```
+
+Проверка и сборка web-части:
+
+```powershell
+npm run check:web
+```
+
+## Текущий scope фронтенда
+
+Сейчас реализовано:
+
+- `apps/website`: каркас premium landing page
+- `apps/miniapp`: Telegram-ориентированный личный кабинет
+- `packages/design-system`: tokens, themes, подключение шрифтов
+- `packages/ui-web`: общие web-компоненты
+
+Пока не реализовано:
+
+- реальная backend-валидация Telegram WebApp auth
+- платежные сценарии
+- полноценные продовые контентные страницы и billing-backend
+
+## Локальное визуальное тестирование
+
+Сайт:
+
+- запусти `npm run dev:website`
+- открой локальный URL в браузере
+- проверь desktop и mobile responsive-режимы
+- если dev-сервер рендерит пустую страницу, используй static preview на `http://127.0.0.1:4300`
+
+Mini App:
+
+- запусти `npm run dev:miniapp`
+- пробрось локальный порт наружу через `cloudflared` или `ngrok`
+- вставь полученный `https` URL в `MINIAPP_URL` в `.env`
+- перезапусти Python-бота; он автоматически обновит кнопку Mini App в Telegram
+- открой бота в Telegram и запусти Mini App внутри него
+- Mini App dev-сервер работает на `http://localhost:3001`
+- если Telegram Desktop или локальный браузер на Windows показывает пустую страницу, используй static preview вместо Vite dev mode
+
+Вспомогательная команда для Windows:
+
+```powershell
+powershell -ExecutionPolicy Bypass -File .\scripts\start-miniapp-public.ps1
+```
+
+Этот helper:
+
+- запускает dev-сервер Mini App
+- автоматически определяет фактический локальный порт
+- поднимает публичный `cloudflared` tunnel
+- записывает публичный `MINIAPP_URL` обратно в `.env`
+- выводит следующую команду для синхронизации кнопки Telegram
+
+Пример с `cloudflared`:
+
+```powershell
+npm run dev:miniapp
+cloudflared tunnel --url http://localhost:3001
+```
+
+После этого вставь сгенерированный `https://...trycloudflare.com` URL в `MINIAPP_URL` и перезапусти:
+
+```powershell
+python -m app.bot.main
+```
+
+Если нужно только обновить кнопку Mini App после смены URL, запусти:
+
+```powershell
+python -m app.bot.sync_telegram_ui
+```
+
+## Зачем нужен Mini App, если бот уже работает
+
+Бот по-прежнему полезен для команд, уведомлений и fallback-сценариев.
+
+Mini App нужен для:
+
+- более удобного UX личного кабинета
+- отображения тарифов и billing
+- профиля и пользовательских настроек
+- точек входа в поддержку
+- onboarding-сценариев без длинных чат-флоу
+
+## Как делиться Mini App с другом
+
+Твой друг сможет открыть тот же Mini App, если соблюдены все условия:
+
+- `MINIAPP_URL` указывает на публичный `https` адрес
+- dev-сервер Mini App всё ещё работает на твоей машине
+- публичный tunnel всё ещё жив
+- кнопка меню бота синхронизирована через `python -m app.bot.sync_telegram_ui`
+
+Для коротких тестов `cloudflared` достаточно.
+
+Для нормального стабильного использования лучше задеплоить `apps/miniapp` на статический хостинг, например:
+
+- Cloudflare Pages
+- Vercel
+- Netlify
+
+После этого нужно поставить постоянный домен в `MINIAPP_URL` вместо временного `trycloudflare` URL.
+
+## Что дальше
+
+- подключить Mini App к backend API и Telegram WebApp auth validation
+- превратить текущий каркас сайта в полноценный публичный продуктовый сайт
+
+## Стабильный URL для Mini App
+
+Временные туннели вроде `trycloudflare`, `localhost.run` или `loca.lt` подходят только для быстрых локальных превью.
+Для нормального использования Telegram Mini App они недостаточно стабильны и могут перестать работать в любой момент, если изменится локальный процесс, tunnel или endpoint провайдера.
+
+В репозиторий уже добавлен workflow для GitHub Pages, который публикует совместимую с Telegram статическую версию Mini App из:
+
+`apps/miniapp/compat`
+
+Ожидаемый долгоживущий URL после включения GitHub Pages для репозитория:
+
+`https://insanekinge.github.io/anny-vpn/`
+
+После успешного выполнения workflow используй этот URL как `MINIAPP_URL` и укажи этот же адрес в:
+
+`@BotFather -> Bot Settings -> Menu Button`
