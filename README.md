# AllyVPN

AllyVPN is a Telegram-controlled VPN service backend integrated with a real Marzban panel. The current repository is prepared for local self-hosted operation with production-oriented boundaries: secrets only from environment variables, service-layer isolation, admin-only subscription activation, and user access issuance through Marzban.

## Stack

- Python 3.12
- aiogram 3.26.0
- FastAPI 0.118.0
- SQLAlchemy 2.0.48
- httpx 0.28.1
- pydantic-settings 2.13.1
- SQLite for single-node local run, PostgreSQL-ready via `DATABASE_URL`

## Security Notes

- No secrets are hardcoded.
- Telegram bot token is loaded from environment variables only.
- `.env` is ignored by Git.
- Marzban credentials are read only from environment variables.
- The bot uses service-layer abstractions instead of raw HTTP calls in handlers.
- Support messages are sanitized and length-limited before persistence.
- SQLAlchemy ORM is used end-to-end, avoiding raw SQL string interpolation.
- Logging is structured and does not print configured secrets.

## Folder Structure

```text
app/
  api/
    main.py
    routes/
      debug.py
      health.py
  bot/
    main.py
    handlers/
      about.py
      access.py
      configs.py
      help.py
      menu.py
      start.py
      subscription.py
      support.py
      utils.py
    keyboards/
      common.py
      main_menu.py
      subscription_menu.py
    states/
      support.py
    texts/
      messages.py
  core/
    config.py
    logging.py
    security.py
  db/
    base.py
    models.py
    seed.py
    session.py
  integrations/
    marzban/
      client.py
      exceptions.py
      schemas.py
  services/
    access_service.py
    audit_service.py
    config_service.py
    marzban_service.py
    subscription_service.py
    support_service.py
    user_service.py
  tests/
    conftest.py
    test_marzban_stub.py
    test_start_flow.py
    test_subscription_service.py
    test_support_flow.py
```

## Environment Variables

Required for bot run:

- `BOT_TOKEN`
- `MARZBAN_BASE_URL`
- `MARZBAN_USERNAME`
- `MARZBAN_PASSWORD`

Core runtime:

- `APP_ENV=production`
- `BOT_USERNAME=@AllyVPNsbot`
- `DATABASE_URL=sqlite+aiosqlite:///./allyvpn.db`
- `LOG_LEVEL=INFO`
- `SUPPORT_USERNAME=`
- `ADMIN_TELEGRAM_IDS=123456789,987654321`

Marzban integration:

- `MARZBAN_BASE_URL=`
- `MARZBAN_USERNAME=`
- `MARZBAN_PASSWORD=`
- `MARZBAN_VERIFY_SSL=false`
- `MARZBAN_TIMEOUT=15`
## Local Setup

1. Create and activate a virtual environment.
2. Install dependencies:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

3. Fill `.env` with your real Telegram token and Marzban credentials:

```env
BOT_TOKEN=your_real_token_here
MARZBAN_BASE_URL=https://your-marzban-host
MARZBAN_USERNAME=admin_username
MARZBAN_PASSWORD=admin_password
ADMIN_TELEGRAM_IDS=your_telegram_id
```

## Run Commands

Run the bot:

```powershell
python -m app.bot.main
```

Run the API:

```powershell
uvicorn app.api.main:app --reload
```

## Operation

Implemented:

- Telegram commands `/start`, `/help`, `/menu`, `/whoami`
- Admin-only command `/grant_subscription <telegram_id> <plan_code> [active|trial]`
- Inline navigation for subscription, access, configs, support, and about screens
- Local user persistence and audit trail
- Real Marzban authentication and user provisioning
- FastAPI `/health`

## Marzban Connection

The Marzban integration is isolated in `app/integrations/marzban/` and wrapped by `app/services/marzban_service.py`.

To run against your local Marzban now:

1. Set `MARZBAN_BASE_URL`, `MARZBAN_USERNAME`, `MARZBAN_PASSWORD`.
2. Restart the bot/API.
3. Ask each user to send `/start` once.
4. Send `/whoami` to get your Telegram ID.
5. Put your admin Telegram ID into `ADMIN_TELEGRAM_IDS` in `.env`.
6. Grant access:

```text
/grant_subscription <your_or_friend_telegram_id> m1 active
```

7. User presses `Get Access`.

## For You And Your Friend

If the bot runs on your machine, both of you can use the Telegram bot immediately as long as:

- your machine has outbound access to Telegram
- the bot process can reach the local Marzban API
- both users send `/start` once before you issue a subscription

For the VPN itself to work for your friend, the Marzban-managed VPN endpoints must be reachable from your friend's device. That means:

- do not use `127.0.0.1` or `localhost` in public-facing Marzban/Xray URLs
- if your friend is outside your home network, expose the required inbound ports on the router
- configure firewall rules to allow those inbound ports
- use a domain or public IP that resolves to your server
- use valid TLS certificates if your Marzban/Xray setup expects TLS

If Marzban currently generates subscription URLs or node endpoints with local-only addresses, the bot may create access successfully, but your friend will not be able to connect.

The current client authenticates against `/api/admin/token` and works through adapter methods:

- `login()`
- `get_user(username)`
- `create_user(payload)`
- `modify_user(username, payload)`
- `get_subscription_info(username)`
- `get_user_subscription_url(username)`

## What To Build Next

- Payment integration with provider webhooks and verified subscription activation.
- Telegram Mini App for plan management and device onboarding.
- Android client consuming subscription/config delivery APIs.
