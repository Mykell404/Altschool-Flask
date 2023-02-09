from ..utils import db

# Create the user db


"""
String field has a limit of 255 characters whereas a text field 
has a chracter limit of 30,000 character
"""


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(45), nullable=False, unique=True)
    email = db.Column(db.String(50), nullable=False, unique=True)
    password_hash = db.Column(db.Text(), nullable=False)
    is_staff = db.Column(db.Boolean(), default=False)
    is_active = db.Column(db.Boolean(), default=False)
    orders = db.relationship('Order', backref='user', lazy=True)

    def __repr__(self):
        return f"<User {self.username}>"

    def save(self):
        """
        Create this function on all object instance
        """
        db.session.add(self)
        db.session.commit()


    