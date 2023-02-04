from flask import request, jsonify
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from passlib.hash import pbkdf2_sha256
from models import UserModel
from db import db
from schemas import UserSchema

blp = Blueprint("Users", __name__, description="Operations on User")

"""
register:
  add user to db
  check if user exist in db
    return a conflict error
  add_user to db
  save hash user password

"""


@blp.route("/register")
class UserRegister(MethodView):
    @blp.arguments(UserSchema)
    def post(self, user_data):
        if UserModel.query.filter(UserModel.username == user_data["username"]).first():
            # Conflict Error
            abort(409, message="A user with this username already exists")

        user = UserModel(
            username=user_data["username"],
            password=pbkdf2_sha256.hash(user_data["password"])
        )

        db.session.add(user)
        db.session.commit()

        return {"message": "User Created Successfully"}, 201
