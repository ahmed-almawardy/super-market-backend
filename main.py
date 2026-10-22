from io import BytesIO
from typing import Annotated

import pandas as pd
import requests
from fastapi import Depends, FastAPI, File, UploadFile, Body, Request
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from apimodels import Product, ProductCreate
from db import Product as DBProduct
from db import get_session
from db.repos import DBRepo, VercelRepo

app = FastAPI(
    title="Fresh Expiry API",
    version="1.0.0",
    debug=True,
    description="Product inventory and expiry dates",
)

# Development-friendly CORS. Restrict origins before deploying publicly.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
    allow_headers=["*"],

)


@app.get("/", tags=["Health"])
def root():
    return {
        "service": "Fresh Expiry API",
        "docs": "/docs",
        "products_endpoint": "/api/products",
    }

DB = []
PUSH_NOTIFICATIONS = {}

@app.get("/health", tags=["Health"])
def health():
    return {"status": "ok"}


@app.get("/api/products", response_model=list[Product], tags=["Products"])
def get_products(
    session: Annotated[Session, Depends(get_session)],
):
    return VercelRepo(DB).all()


@app.post("/api/products/upload", status_code=200)
async def upload_products(
    session: Annotated[Session, Depends(get_session)],
    file: Annotated[UploadFile, File(...)],
):
    data = await file.read()
    records = pd.read_csv(BytesIO(data), encoding="utf-8-sig").to_dict(
            orient="records"
        )
    repo = VercelRepo(DB)
    repo.add_all(records)
    return {"status": "ok"}


@app.post('/api/register-push-token')
async def register_push_token(request: Request):
    data = await request.json()
    PUSH_NOTIFICATIONS[data['pushToken']] = data
    print(    PUSH_NOTIFICATIONS)
    check_and_send_expiry_push_notifications()
    return {
        'status': 'ok'
    }


def check_and_send_expiry_push_notifications():
    # tomorrow = date.today() + timedelta(days=1)

    # 1. Fetch products expiring tomorrow from database
    # expiring_products = db.query(Product).filter(Product.expiry_date == tomorrow).all()
    # if not expiring_products:
    #     return

    # 2. Format names
    names = "، ".join([p.name for p in DB[:4]])

    # 3. Fetch registered push tokens from database
    tokens = list(PUSH_NOTIFICATIONS.keys())

    # 4. Send Push Notifications via Expo Push API
    for token_entry in tokens:
        payload = {
            "to": token_entry,
            "title": "تنبيه: منتجات تنتهي غدًا 🔔",
            "body": f"المنتجات التالي تنتهي غداً: {names}. راجع المخزون.",
            "sound": "default",
            # "channelId": "fresh-expiry-tomorrow",
            "channelId": "expiry-alerts",
            "priority": "high",
        }
        requests.post("https://exp.host/--/api/v2/push/send", json=payload)