from datetime import date, timedelta
from io import BytesIO

from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, File, UploadFile
import pandas as pd

from apimodels import Product, ProductCreate

app = FastAPI(title="Fresh Expiry API", version="1.0.0", description="Product inventory and expiry dates")

# Development-friendly CORS. Restrict origins before deploying publicly.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)



def demo_products() -> list[Product]:
    today = date.today()
    return []
    return [
        Product(id=1, image_url='https://m.media-amazon.com/images/I/61Lj8VhEgiL._AC_SY741_.jpg', name="لبن كامل الدسم", quantity=8, unit="عبوات", expiry_date=today + timedelta(days=1), emoji="🥛"),
        Product(id=2, name="زبادي طبيعي", quantity=14, unit="علبة", expiry_date=today + timedelta(days=4), emoji="🥣"),
        Product(id=3, name="عصير مانجو", quantity=6, unit="عبوات", expiry_date=today + timedelta(days=7), emoji="🥭"),
        Product(id=4, name="جبنة بيضاء", quantity=5, unit="عبوات", expiry_date=today + timedelta(days=2), emoji="🧀"),
        Product(id=5, name="خبز توست", quantity=11, unit="أكياس", expiry_date=today + timedelta(days=10), emoji="🍞"),
        Product(id=6, name="بيض", quantity=3, unit="أطباق", expiry_date=today - timedelta(days=1), emoji="🥚"),
    ]


PRODUCTS = demo_products()


@app.get("/", tags=["Health"])
def root():
    return {"service": "Fresh Expiry API", "docs": "/docs", "products_endpoint": "/api/products"}


@app.get("/health", tags=["Health"])
def health():
    return {"status": "ok"}


@app.get("/api/products", response_model=list[Product], tags=["Products"])
def get_products():
    """Return inventory products. Replace this demo list with your database query."""
    return PRODUCTS

@app.post(
    '/api/products/upload',
    status_code=200
)
async def upload_products(file: UploadFile = File(...)):
    data =  await file.read()
    for ro in pd.read_csv(BytesIO(data), encoding='utf-8-sig').to_dict(orient="records"):
        pp = ProductCreate.model_validate(ro)
        dd = pp.model_dump()
        _id = len(PRODUCTS) + 1
        dd['id']=_id
        PRODUCTS.append(Product.model_validate(dd))
    return {
        'status': 'ok'
    }