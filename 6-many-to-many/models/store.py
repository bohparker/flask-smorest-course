from db import db


class StoreModel(db.Model):
    __tablename__ = 'stores'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    # create a many-to-one relationship
    # items is a list of item models
    # lazy dynamic so that the list of items doesn't auto load when querying StoreModel
    # cascade to decide what happens to this record's relationship when it is deleted
    items = db.relationship('ItemModel', back_populates='store', lazy='dynamic', cascade='all, delete')
    tags = db.relationship('TagModel', back_populates='store', lazy='dynamic')