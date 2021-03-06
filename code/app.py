from flask import Flask, request
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

items = []


class Item(Resource):
    def get(self, name):
        item = next(filter(lambda x: x['name'] == name, items), None)
        return {'item': item}, 200 if item is not None else 404


class ItemList(Resource):
    def get(self):
        return {'items': items}

    def post(self):
        data = request.get_json()
        name = data['name']
        if next(filter(lambda x: x['name'] == name, items), None) is not None:
            return {'message': "An item with name '{}' already exists.".format(name)}, 400
        item = {'name': name, 'price': data['price']}
        items.append(item)
        return item, 201


api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/item')

app.run(port=5000, debug=True)
