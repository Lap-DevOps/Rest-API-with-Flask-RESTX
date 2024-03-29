from enum import Enum

from api.utils import db


class Sizes(Enum):
    """Enum for pizza sizes"""
    SMALL = 'small'
    MEDIUM = 'medium'
    LARGE = 'large'
    EXTRA_LARGE = 'extra_large'


class Status(Enum):
    """Enum for order statuses"""
    PENDING = 'pending'
    IN_TRANSIT = 'in_transit'
    DELIVERED = 'delivered'
    CANCELLED = 'cancelled'


class Order(db.Model):
    __tablename__ = 'orders'

    id = db.Column(db.Integer, primary_key=True)
    size = db.Column(db.Enum(Sizes), nullable=False)
    order_status = db.Column(db.Enum(Status), nullable=False, default=Status.PENDING)
    flavour = db.Column(db.String(80), nullable=False)
    quantity = db.Column(db.Integer())
    date_created = db.Column(db.DateTime, nullable=False, default=db.func.now())

    customer = db.Column(db.Integer(), db.ForeignKey('users.id'))

    def __repr__(self):
        return f"Order(id={self.id}, user_id={self.user_id}, status={self.status})"

    def save(self):
        """
        Save the current object to the database using the current session.
        """
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_by_id(cls, id):
        """
        Retrieve an object by its ID.

        Args:
            cls: The class itself.
            id: The ID of the object to retrieve.

        Returns:
            The object with the specified ID, or None if not found.
        """
        return cls.query.get(id=id)

    @classmethod
    def delete(cls, id):
        db.session.delete(id)
        db.session.commit()
