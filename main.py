from io import BytesIO
from typing import Annotated

import pandas as pd
from fastapi import Depends, FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from apimodels import Product, ProductCreate
from db import Product as DBProduct
from db import get_session
from db.repos import DBRepo

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


@app.get("/health", tags=["Health"])
def health():
    return {"status": "ok"}


@app.get("/api/products", response_model=list[Product], tags=["Products"])
def get_products(
    session: Annotated[Session, Depends(get_session)],
):
    """Return inventory products. Replace this demo list with your database query."""
    return session.query(DBProduct).all()


@app.post("/api/products/upload", status_code=200)
async def upload_products(
    session: Annotated[Session, Depends(get_session)],
    file: Annotated[UploadFile, File(...)],
):
    data = await file.read()
    records = pd.read_csv(BytesIO(data), encoding="utf-8-sig").to_dict(
            orient="records"
        )
    repo = DBRepo(session)
    repo.add_all(records)
    return {"status": "ok"}
