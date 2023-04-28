from marshmallow import Schema, fields


class ItemSchema(Schema):
    # dump_only does validation on returning data, not incoming data
    # we don't need to get an item id when creating an item from a payload
    # incoming id info comes from the url
    id = fields.Str(dump_only=True)
    # required means it must be part of the payload
    name = fields.Str(required=True)
    price = fields.Float(required=True)
    store_id = fields.Str(required=True)

class ItemUpdateSchema(Schema):
    # fields are not necessary since this is for updating
    # the item id comes in through the url
    name = fields.Str()
    price = fields.Float()

class StoreSchema(Schema):
    id = fields.Str(dump_only=True)
    name = fields.Str(required=True)