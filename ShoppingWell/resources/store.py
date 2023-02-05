from flask.views import MethodView
from flask_smorest import Blueprint, abort
from db import db
from models import StoreModel, ItemModel
from schemas import StoreSchema
from sqlalchemy.exc import SQLAlchemyError
from flask_jwt_extended import jwt_required

blp = Blueprint("Stores", __name__, description="Operations on Stores")
"""
Create the Store blueprint

get:
    get store
    return store

delete:
    get items
    loop through items
    delete items

    get store
    delete store
"""


@blp.route("/stores/<int:store_id>")
class Store(MethodView):
    @jwt_required()  # Require user to be logged in to access it
    @blp.response(200, StoreSchema)
    def get(self, store_id):
        store = StoreModel.query.get_or_404(store_id)
        return store

    @jwt_required()
    def delete(self, store_id):
        store_items = ItemModel.query.filter_by(store_id=store_id).all()
        for item in store_items:
            db.session.delete(item)

        store = StoreModel.query.get_or_404(store_id)
        db.session.delete(store)
        db.session.commit()

        return {"message": "Store deleted"}


"""
StoreList

get:
    query the store model

post:
    save the StoreModel
    commit the saved store to db

"""


@blp.route("/stores")
class StoreList(MethodView):
    @jwt_required()  # Require user to be logged in to access it
    @blp.response(200, StoreSchema(many=True))
    def get(self):
        return StoreModel.query.all()

    @jwt_required()
    @blp.arguments(StoreSchema)
    @blp.response(200, StoreSchema)
    def post(self, store_data):
        store = StoreModel(**store_data)

        try:
            db.session.add(store)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error occured while creating the store")

        return store, 201
