from flask import request, jsonify
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from passlib.hash import pbkdf2_sha256
from models import UserModel
from db import db
from flask_jwt_extended import create_access_token
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


"""
User
Get a particular user based on id:
  query user model by id or return 404
  return user


Delete user based on id:
  query user model by id or return 404
  del user
  return message

"""


@blp.route("/user/<int:user_id>")
class User(MethodView):
    @blp.response(200, UserSchema)
    # Get user by id
    def get(self, user_id):
        user = UserModel.query.get_or_404(user_id)
        return user

    def delete(self, user_id):
        # Delete user by id
        user = UserModel.query.get_or_404(user_id)

        db.session.delete(user)
        db.session.commit()

        return {"message": "User Deleted"}, 200


@blp.route("/users")
class UserList(MethodView):
    @blp.response(200, UserSchema)
    def get(self):
        all_users = UserModel.query.all()
        return all_users


"""
Login:
post user_data to db
check if data exist
  create unique token
  login
throw err
"""


@blp.route("/login")
class Login(MethodView):
    @blp.arguments(UserSchema)
    def post(self, user_data):
        # Confirm if the username is the same as the name in db
        user = UserModel.query.filter(
            UserModel.username == user_data["username"]
        ).first()
        # Verify if user And password exist in db
        if user and pbkdf2_sha256.verify(user_data["password"], user.password):
            # create a access token using the id as an identity
            access_token = create_access_token(identity=user.id)
            return {"access_token": access_token}
        abort(401, message="Invalid Credentials")  # Unauthorized
