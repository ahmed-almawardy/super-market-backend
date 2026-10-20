# Fresh Expiry — React Native + FastAPI

A starter supermarket inventory app inspired by the supplied screenshot. It is built with Expo React Native for **iOS and Android**, with a FastAPI backend and Arabic right-to-left interface.

## Included

- Welcome/onboarding screen.
- Supermarket expiry dashboard with search and filters (all, within 2 days, 3–7 days, over 7 days).
- Product cards with quantity and expiry date.
- Product list fetched from FastAPI (`GET /api/products`).
- Local notification scheduled for **9:00 AM tomorrow** when products expire tomorrow.
- Pull-to-refresh, loading state, API errors, and sample data.

## 1. Start the FastAPI backend

Requirements: Python 3.10+.

```bash
cd backend
python -m venv .venv
# Linux/macOS
source .venv/bin/activate
# Windows PowerShell: .venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Open `http://127.0.0.1:8000/docs` to see the interactive API documentation.

The sample records use dates relative to the server's current date, so the app has useful example products whenever you launch it. Replace the sample list in `backend/main.py` with your database/repository layer when ready.

## 2. Run the React Native app

Requirements: Node.js LTS and npm. Install Expo Go on a physical phone, or use the iOS Simulator / Android Emulator.

```bash
cd mobile
npm install
```

Edit `mobile/src/config.js` and set `API_BASE_URL`:

- **Android Emulator:** `http://10.0.2.2:8000`
- **iOS Simulator:** `http://127.0.0.1:8000`
- **Physical iOS/Android phone:** use your computer's LAN IP, for example `http://192.168.1.20:8000` (phone and computer on the same Wi-Fi; allow port 8000 through your firewall).

Then run:

```bash
npx expo start
```

Scan the QR code with Expo Go, or press `i` / `a` for a simulator/emulator.

## API response shape

`GET /api/products` returns an array like:

```json
[
  {
    "id": 1,
    "name": "لبن كامل الدسم",
    "quantity": 8,
    "unit": "عبوات",
    "expiry_date": "2026-10-19",
    "image_url": null,
    "emoji": "🥛"
  }
]
```

`expiry_date` uses ISO format `YYYY-MM-DD`. `image_url` may be a full reachable HTTP(S) URL or `null`.

## Notifications: important behavior

On app startup/refresh, the app fetches the current product list and schedules a local notification for **tomorrow at 9 AM** if any products expire tomorrow. Notification permission is requested from the user. The device OS delivers an already-scheduled local notification even if the app is not open at delivery time, subject to OS settings and permissions.

This starter only refreshes and schedules after the app is opened or manually refreshed. If the product list can change while nobody opens the app, or you need reliable notifications across many users/devices, implement server-side scheduling and push notifications (Expo Push Notifications with saved device push tokens, or APNs/FCM). Use HTTPS and authentication in production.

## Build installable app files

This ZIP contains source code, not signed `.ipa` / `.apk` binaries. To create installable builds, configure an Expo account and use EAS Build:

```bash
cd mobile
npx eas-cli build:configure
npx eas-cli build --platform android
npx eas-cli build --platform ios
```

iOS distribution requires Apple signing/setup; Android APK/AAB output depends on the EAS build profile you choose.
