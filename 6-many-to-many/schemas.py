from marshmallow import Schema, fields

# use plain schemas as parent classes to avoid infinite nesting loops
class PlainItemSchema(Schema):
    # dump_only does validation on returning data, not incoming data
    # we don't need to get an item id when creating an item from a payload
    # incoming id info comes from the url
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    price = fields.Float(required=True)


class PlainStoreSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str()


class PlainTagSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str()


class ItemSchema(PlainItemSchema):
   # store_id only needed when getting data (load_only)
   store_id = fields.Int(required=True, load_only=True)
   # store is a nested PlainStoreSchema object and only needed when returning (dump_only)
   store = fields.Nested(PlainStoreSchema(), dump_only=True)
   tags = fields.List(fields.Nested(PlainTagSchema(), dump_only=True))


class ItemUpdateSchema(Schema):
    # fields are not necessary since this is for updating
    # the item id comes in through the url
    name = fields.Str()
    price = fields.Float()


class StoreSchema(PlainStoreSchema):
    # items are a list of nested PlainItemSchema objects only needed when returning (dump_only)
    items = fields.List(fields.Nested(PlainItemSchema()), dump_only=True)
    tags = fields.List(fields.Nested(PlainTagSchema(), dump_only=True))


class TagSchema(PlainTagSchema):
    store_id = fields.Int(load_only=True)
    items = fields.List(fields.Nested(PlainItemSchema(), dump_only=True))
    store = fields.Nested(PlainStoreSchema(), dump_only=True)


class TagAndItemSchema(Schema):
    message = fields.Str()
    item = fields.Nested(ItemSchema)
    tag = fields.Nested(TagSchema)