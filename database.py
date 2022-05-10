from flask import Flask
from flask_sqlalchemy import SQLAlchemy


class DatabaseHandler:
    app: Flask
    db = SQLAlchemy()

    def __init__(self, app: Flask):
        self.app = app
        self.db.init_app(app)

    def add_model(self, model):
        self.db.session.add(model)
        self.db.session.commit()
        self.db.session.flush()

    def get_nutrition_db(self, product_name: str):
        return self.get_models(ProductData, product_name)

    def get_models(self, model, db_filter):
        db_query = self.db.session.query(model)
        db_query = db_query.filter(model.product_name == db_filter)

        if db_query.count() < 1:
            db_query = self.db.session.query(model)
            db_filter = "%{}%".format(db_filter)
            db_query = db_query.filter(model.product_name.like(db_filter))
        return db_query.all()


class ProductData(DatabaseHandler.db.Model):
    id = DatabaseHandler.db.Column(DatabaseHandler.db.Integer, primary_key=True)
    file_name = DatabaseHandler.db.Column(DatabaseHandler.db.String(300), nullable=False)
    product_name = DatabaseHandler.db.Column(DatabaseHandler.db.String(300), nullable=False)
    calories = DatabaseHandler.db.Column(DatabaseHandler.db.SmallInteger, nullable=False)
    fat = DatabaseHandler.db.Column(DatabaseHandler.db.SmallInteger, nullable=False)
    carbohydrates = DatabaseHandler.db.Column(DatabaseHandler.db.SmallInteger, nullable=False)
    protein = DatabaseHandler.db.Column(DatabaseHandler.db.SmallInteger, nullable=False)

    def __init__(self, file_name, product_name, calories, fat, carbohydrates, protein):
        self.file_name = file_name
        self.product_name = product_name
        self.calories = calories
        self.fat = fat
        self.carbohydrates = carbohydrates
        self.protein = protein

    def __repr__(self):
        return '<Product %r, %r>' % (self.file_name, self.product_name)