from decimal import Decimal
from openwebpos.extensions import db
from openwebpos.utils.sql import SQLMixin
from openwebpos.utils import gen_order_number


class OrderType(SQLMixin, db.Model):
    __tablename__ = 'order_types'
    name = db.Column(db.String(255), nullable=False, unique=True)
    active = db.Column(db.Boolean, default=True)
    orders = db.relationship('Order', backref='order_type', lazy='dynamic')

    @staticmethod
    def insert_order_types():
        order_types = [
            {'name': 'Dine In'},
            {'name': 'Take Out'},
            {'name': 'Phone'}
        ]

        for order_type in order_types:
            order_type = OrderType(**order_type)
            order_type.save()

    def __init__(self, **kwargs):
        super(OrderType, self).__init__(**kwargs)


class OrderPager(SQLMixin, db.Model):
    __tablename__ = 'order_pagers'
    name = db.Column(db.String(255), nullable=False, unique=True)
    active = db.Column(db.Boolean, default=True)
    hidden = db.Column(db.Boolean, default=False)
    orders = db.relationship('Order', backref='order_pager', lazy='dynamic')

    @staticmethod
    def insert_order_pagers():
        order_pagers = [
            {'name': 'Dine In', 'hidden': True},
            {'name': 'Take Out', 'hidden': True},
            {'name': 'Phone', 'hidden': True}
        ]

        for order_pager in order_pagers:
            order_pager = OrderPager(**order_pager)
            order_pager.save()

    @staticmethod
    def has_pagers():
        return OrderPager.query.filter_by(hidden=False).count() > 0

    def __init__(self, **kwargs):
        super(OrderPager, self).__init__(**kwargs)


class TransactionType(SQLMixin, db.Model):
    __tablename__ = 'transaction_types'
    name = db.Column(db.String(255), nullable=False, unique=True)
    active = db.Column(db.Boolean, default=True)
    transactions = db.relationship('Transaction', backref='transaction_type',
                                   lazy='dynamic')

    @staticmethod
    def insert_transaction_types():
        transaction_types = [
            {'name': 'Cash'},
            {'name': 'Card'},
            {'name': 'Zelle'},
            {'name': 'Cash App'}
        ]

        for transaction_type in transaction_types:
            transaction_type = TransactionType(**transaction_type)
            transaction_type.save()

    @staticmethod
    def list_active():
        return TransactionType.query.filter_by(active=True).all()

    def __init__(self, **kwargs):
        super(TransactionType, self).__init__(**kwargs)


class Transaction(SQLMixin, db.Model):
    __tablename__ = 'transactions'
    transactionTypeID = db.Column(db.Integer,
                                  db.ForeignKey('transaction_types.id'))
    orderID = db.Column(db.Integer, db.ForeignKey('orders.id'))
    amount = db.Column(db.Numeric(10, 2), nullable=False, default=Decimal(0.00))
    change = db.Column(db.Numeric(10, 2), nullable=False, default=Decimal(0.00))
    active = db.Column(db.Boolean, default=True)

    @staticmethod
    def add_transaction(order_id, transaction_type_id, amount, order_total):
        _change = Decimal(amount) - Decimal(order_total)
        amount = Decimal(amount)
        if amount < order_total:
            _change = 0
        transaction = Transaction(
            orderID=order_id,
            transactionTypeID=transaction_type_id,
            amount=amount,
            change=_change
        )
        transaction.save()

    def __init__(self, **kwargs):
        super(Transaction, self).__init__(**kwargs)


class Order(SQLMixin, db.Model):
    __tablename__ = 'orders'

    orderNumber = db.Column(db.String(255), nullable=False, unique=True)
    orderTypeID = db.Column(db.Integer, db.ForeignKey('order_types.id'))
    orderPagerID = db.Column(db.Integer, db.ForeignKey('order_pagers.id'))
    orderItems = db.relationship('OrderItem', backref='order', lazy='dynamic')
    orderTotal = db.Column(db.Numeric(10, 2), nullable=False,
                           default=Decimal(0.00))
    orderDueTotal = db.Column(db.Numeric(10, 2), nullable=False,
                              default=Decimal(0.00))
    transactions = db.relationship('Transaction', backref='order',
                                   lazy='dynamic')
    paymentStatus = db.Column(db.String(255), nullable=False, default='Unpaid')
    options = db.relationship('OrderItemOption', backref='order',
                              lazy='dynamic')
    active = db.Column(db.Boolean, default=True)

    def get_payment_status(self):
        if self.paymentStatus == 'Paid':
            return 'Paid'
        elif self.paymentStatus == 'Unpaid':
            return 'Unpaid'
        elif self.paymentStatus == 'Partial':
            return 'Partial'

    def get_order_total(self):
        order_total = Decimal(0.00)
        for order_item in self.orderItems:
            order_total += order_item.subtotal + order_item.tax
        return order_total

    def get_payment_amount(self):
        payment_amount = Decimal(0.00)
        for transaction in self.transactions:
            payment_amount += transaction.amount
        return payment_amount

    def get_order_due_total(self):
        order_total = self.get_order_total()
        payment_amount = self.get_payment_amount()
        due_total = order_total - payment_amount
        if due_total < 0:
            due_total = 0
        return due_total

    def get_order_total_due(self):
        order_total = self.get_order_total()
        payment_amount = self.get_payment_amount()
        return order_total - payment_amount

    @staticmethod
    def delete_order(order_id):
        order = Order.query.get(order_id)
        order_items = OrderItem.query.filter_by(orderID=order_id).all()
        for order_item in order_items:
            order_item.delete_order_item()
        order.delete()

    def update_order_total(self):
        self.orderTotal = self.get_order_total()
        self.orderDueTotal = self.get_order_due_total()
        self.update()

    def update_order_due_total(self):
        self.orderDueTotal = self.get_order_due_total()
        self.update()

    def set_order_status(self):
        if self.orderDueTotal == 0:
            self.paymentStatus = 'Paid'
        else:
            self.paymentStatus = 'Unpaid'
        self.update()

    @staticmethod
    def set_payment_amount(order_id, payment_amount):
        order = Order.query.get(order_id)
        order.paymentAmount = order.paymentAmount + Decimal(payment_amount)
        order.save()

    @staticmethod
    def mark_order_paid(order_id):
        order = Order.query.get(order_id)
        order.paymentStatus = 'Paid'
        order.save()

    @staticmethod
    def mark_partial_paid(order_id):
        order = Order.query.get(order_id)
        order.paymentStatus = 'Partial'
        order.save()

    @staticmethod
    def get_by_order_number(order_number):
        return Order.query.filter_by(orderNumber=order_number).first_or_404()

    def __init__(self, **kwargs):
        super(Order, self).__init__(**kwargs)

        if self.orderNumber is None:
            self.orderNumber = gen_order_number()

        if self.orderTotal is None:
            self.orderTotal = Decimal(0.00)

        if self.orderDueTotal is None:
            self.orderDueTotal = Decimal(0.00)


class OrderItem(SQLMixin, db.Model):
    __tablename__ = 'order_items'

    orderID = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    itemID = db.Column(db.Integer, db.ForeignKey('item.id'),
                       nullable=False)
    quantity = db.Column(db.Integer, default=1)
    subtotal = db.Column(db.Numeric(10, 2), default=0.00)
    tax = db.Column(db.Numeric(10, 2), default=0.00)
    active = db.Column(db.Boolean, default=True)
    options = db.relationship('OrderItemOption', backref='order_item',
                              lazy='dynamic')

    def delete_order_item(self):
        order_item = OrderItem.query.filter_by(id=self.id).first()
        for option in order_item.options:
            option.delete()
        order_item.delete()

    @staticmethod
    def get_by_id(id):
        return OrderItem.query.get(id)

    @staticmethod
    def add_to_order(order_id, item_id, quantity=1, subtotal=0.0):
        order_item = OrderItem(orderID=order_id, itemID=item_id,
                               quantity=quantity, subtotal=subtotal)
        order_item.save()

    @staticmethod
    def get_order_items(order_id):
        return OrderItem.query.filter_by(orderID=order_id).all()

    def __init__(self, **kwargs):
        super(OrderItem, self).__init__(**kwargs)

        if self.tax is None:
            self.tax = Decimal(self.subtotal) * Decimal(0.0825)


class OrderItemOption(SQLMixin, db.Model):
    __tablename__ = 'order_item_options'

    orderID = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    orderItemID = db.Column(db.Integer, db.ForeignKey('order_items.id'),
                            nullable=False)
    ingredientID = db.Column(db.Integer, db.ForeignKey('ingredients.id'),
                             nullable=False)
    type = db.Column(db.String(255), nullable=False)
    price = db.Column(db.Numeric(10, 2), nullable=False, default=0.00)
    active = db.Column(db.Boolean, default=True)

    @staticmethod
    def get_order_item_options(order_id):
        return OrderItemOption.query.filter_by(orderID=order_id).all()

    def __init__(self, **kwargs):
        super(OrderItemOption, self).__init__(**kwargs)
