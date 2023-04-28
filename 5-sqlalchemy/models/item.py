from db import db


class ItemModel(db.Model):
    __tablename__ = 'items'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    price = db.Column(db.Float(precision=2), unique=False, nullable=False)
    # create a one-to-many relationship to stores
    # first create a foreign key from the other table (since this is the one side)
    store_id = db.Column(
        db.Integer, db.ForeignKey('stores.id'), unique=False, nullable=False
    )
    # then define what the one side has from the many side (a store object)
    store = db.relationship('StoreModel', back_populates='items')