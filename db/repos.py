from apimodels import ProductCreate, Product
from db import Product as DBProduct


class DBRepo:
    def __init__(self, session):
        self.session = session

    def add_all(self, rows):
        post_data = [
            DBProduct(**ProductCreate.model_validate(ro).model_dump())
            for ro in rows
        ]
        self.session.add_all(post_data)
        self.session.commit()


class VercelRepo:
    def __init__(self, db):
        self.db = db

    def all(self):
        return self.db

    def add_all(self, rows):
        post_data = []
        for ro in rows:
            ro_dic = ProductCreate.model_validate(ro).model_dump()
            ro_dic['id'] = len(self.db)  + 1
            post_data.append(Product(**ro_dic))
        self.db.extend(post_data)
