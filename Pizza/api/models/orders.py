from ..utils import db
from enum import Enum
from datetime import datetime

# Enum are ways of creating options in the db


class Sizes(Enum):
    """
    Pizza Sizes
    """
    SMALL = 'small'
    MEDIUM = 'medium'
    LARGE = 'large'
    EXTRA_LARGE = 'extra_large'


class OrderStatus(Enum):
    PENDING = 'pending'
    IN_TRANSIT = 'in_transit'
    DELIVERED = 'delivered'


class Order(db.Model):
    __tablename__ = "orders"
    id = db.Column(db.Integer(), primary_key=True)
    quantity = db.Column(db.Integer(), nullable=False)
    size = db.Column(db.Enum(Sizes), default=Sizes.SMALL)
    order_status = db.Column(db.Enum(OrderStatus), default=OrderStatus.PENDING)
    flavour = db.Column(db.String(), nullable=False)
    date_created = db.Column(db.DateTime(), default=datetime.utcnow)
    customer = db.Column(db.Integer(), db.ForeignKey('users.id'))

    def __repr__(self):
        return f"<Order {self.id}>"

    def save(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_by_id(self, id):
        """
        Get the order by id
        """
        return self.query.get_or_404(id)

    def delete(self):
        """
        Delete the order
        """
        db.session.delete(self)
        db.session.commit()

    def update(self):
        """
        Update the order
        """
        db.session.commit()
