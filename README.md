# AllyVPN

AllyVPN now consists of two layers that evolve in parallel:

- the existing Python backend and Telegram bot in `app/`
- a frontend monorepo for the public website, Telegram Mini App, and mobile client UI

The repository is organized so frontend work can move fast without breaking the current Marzban-integrated backend.

## Stack

- Python 3.12
- aiogram 3.26.0
- FastAPI 0.118.0
- SQLAlchemy 2.0.48
- React 18 for website and Mini App
- Expo / React Native for the mobile shell
- npm workspaces for monorepo management
- shared design tokens and web UI packages in `packages/`

## Shared Design Direction

- Palette: `#ffffff`, `#7c4acc`, `#b699e6`, `#0f0d12`, `#2a1c40`
- Typography:
  - Display: `Sora`
  - Body/UI: `Manrope`
- Themes:
  - dark
  - light

## Repository Structure

```text
app/
  api/
  bot/
  core/
  db/
  integrations/
  services/
apps/
  website/
  miniapp/
  mobile/
packages/
  design-system/
  ui-web/
```

## Backend Runtime

Required bot env values:

- `BOT_TOKEN`
- `MARZBAN_BASE_URL`
- `MARZBAN_USERNAME`
- `MARZBAN_PASSWORD`

Additional env values:

- `APP_ENV=production`
- `BOT_USERNAME=@AllyVPNsbot`
- `DATABASE_URL=sqlite+aiosqlite:///./allyvpn.db`
- `MINIAPP_URL=https://your-public-miniapp-url`
- `SUPPORT_USERNAME=`
- `ADMIN_TELEGRAM_IDS=123456789,987654321`
- `LOG_LEVEL=INFO`

## Local Setup

Install backend:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

Fill `.env` with real backend credentials:

```env
BOT_TOKEN=your_real_token_here
MARZBAN_BASE_URL=https://your-marzban-host
MARZBAN_USERNAME=admin_username
MARZBAN_PASSWORD=admin_password
MINIAPP_URL=https://your-public-miniapp-url
ADMIN_TELEGRAM_IDS=your_telegram_id
```

The Telegram token is required for the bot side only:

- `BOT_TOKEN` is required to run the bot and push the Mini App button into Telegram
- the Mini App frontend itself does not contain the bot token and should never receive it

Install frontend workspaces:

```powershell
npm install
```

## Run Commands

Run the Telegram bot:

```powershell
python -m app.bot.main
```

Sync Telegram commands and the Mini App button without starting the full backend:

```powershell
python -m app.bot.sync_telegram_ui
```

Run the API:

```powershell
uvicorn app.api.main:app --reload
```

Run the website:

```powershell
npm run dev:website
```

Stable static preview for the website:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\start-website-static.ps1
```

Run the Mini App locally:

```powershell
npm run dev:miniapp
```

Stable static preview for the Mini App:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\start-miniapp-static.ps1
```

Stable static preview with a public temporary URL:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\start-miniapp-static.ps1 -Public
```

Run the mobile UI shell:

```powershell
npm run dev:mobile
```

Build the web apps:

```powershell
npm run check:web
```

## Current Frontend Scope

Implemented now:

- `apps/website`: premium landing-page shell
- `apps/miniapp`: Telegram-oriented account shell
- `apps/mobile`: three-screen mobile UI shell (`Home`, `Access`, `Profile`)
- `packages/design-system`: tokens, themes, font imports
- `packages/ui-web`: shared web primitives

Not implemented yet:

- real Telegram WebApp backend validation flow
- VPN connection engine for the mobile client
- payment flows
- production content pages and billing backend

## Local Visual Testing

Website:

- run `npm run dev:website`
- open the local Vite URL in the browser
- check desktop and mobile responsive views
- if the dev server renders blank, use the static preview script on `http://127.0.0.1:4300`

Mini App:

- run `npm run dev:miniapp`
- expose the local port through `cloudflared` or `ngrok`
- put the generated `https` URL into `MINIAPP_URL` in `.env`
- restart the Python bot; it will set the Telegram menu button automatically
- open the bot in Telegram and launch the Mini App there
- the Mini App dev server runs on `http://localhost:3001`
- if the dev server renders blank in Telegram Desktop or local Windows browsers, use the static preview script instead of Vite dev mode

One-command helper for Windows:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\start-miniapp-public.ps1
```

This helper:

- starts the Mini App dev server
- detects the actual local port automatically
- starts a public `cloudflared` tunnel
- writes the public `MINIAPP_URL` back into `.env`
- prints the next command to sync the Telegram button

Example with `cloudflared`:

```powershell
npm run dev:miniapp
cloudflared tunnel --url http://localhost:3001
```

Then copy the generated `https://...trycloudflare.com` URL into `MINIAPP_URL` and restart:

```powershell
python -m app.bot.main
```

If you only want to refresh the Telegram button after changing the URL, run:

```powershell
python -m app.bot.sync_telegram_ui
```

Mobile app:

- run `npm run dev:mobile`
- Expo starts on port `8082`
- open in Android emulator or on a real Android device through Expo
- current stage is a UI shell for the three main screens
- the real VPN tunnel layer should be added next as native Android functionality

## Why Mini App Exists If The Bot Already Works

The bot is still useful for commands, notifications, and fallback actions.

The Mini App exists for:

- better account UX
- plans and billing views
- profile and preferences
- support entry points
- guided onboarding without long chat flows

The Mini App should not become the VPN client. The actual VPN connect flow belongs in the mobile app.

## Sharing With A Friend

Your friend can open the same Mini App if all of these are true:

- the `MINIAPP_URL` points to a public `https` address
- the Mini App dev server is still running on your machine
- the public tunnel is still alive
- the Telegram bot menu button has been synced with `python -m app.bot.sync_telegram_ui`

For short-term testing, the `cloudflared` tunnel is enough.

For a stable shared setup, deploy `apps/miniapp` to a static host such as Cloudflare Pages, Vercel, or Netlify and set `MINIAPP_URL` to that permanent domain instead of a temporary `trycloudflare` URL.

## What Comes Next

- connect Mini App to backend APIs and Telegram WebApp auth validation
- turn the website shell into a full public product site
- convert the mobile shell into a real Android VPN client with native tunnel integration
# Stable Mini App URL

Temporary tunnels like `trycloudflare`, `localhost.run`, or `loca.lt` are acceptable only for quick local previews.
For Telegram Mini App usage they are not stable enough and may break at any moment when the local process, tunnel, or provider endpoint changes.

The repository now includes a GitHub Pages workflow that publishes the Telegram-compatible static Mini App from:

`apps/miniapp/compat`

Expected long-lived URL after GitHub Pages is enabled for the repository:

`https://insanekinge.github.io/anny-vpn/`

After the workflow runs successfully, use that URL as `MINIAPP_URL` and set the same value in `@BotFather -> Bot Settings -> Menu Button`.
