import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort

from db import items
from schemas import ItemSchema, ItemUpdateSchema


blp = Blueprint('items', __name__, description='Operations on items')

@blp.route('/item/<string:item_id>')
class Item(MethodView):

    @blp.response(200, ItemSchema)
    def get(self, item_id):
        try:
            return items[item_id]
        except KeyError:
            abort(404, message='Item not found.')

    @blp.arguments(ItemUpdateSchema)
    # injected arguments are passed first (item_data)
    @blp.response(200, ItemSchema)
    def put(self, item_data, item_id):
        try:
            item = items[item_id]
            # udpate the item in the dictionary
            item |= item_data

            return item
        except KeyError:
            abort(404, message='Item not found.')

    def delete(self, item_id):
        try:
            del items[item_id]
            return {'message': 'Item deleted'}
        except KeyError:
            abort(404, message='Item not found.')

@blp.route('/item')
class ItemList(MethodView):

    # many=True because multiple items are returned
    @blp.response(200, ItemSchema(many=True))
    def get(self):
        return items.values()
    
    @blp.arguments(ItemSchema)
    # the arguments get passed as params to the def (item_data)
    @blp.response(201, ItemSchema)
    def post(self, item_data):
        for item in items.values():
            if (
                item_data['name'] == item['name']
                and item_data['store_id'] == item['store_id']
            ):
                abort(400, message='Store already exists.')
        item_id = uuid.uuid4().hex
        item = {**item_data, 'id': item_id}
        items[item_id] = item

        return item