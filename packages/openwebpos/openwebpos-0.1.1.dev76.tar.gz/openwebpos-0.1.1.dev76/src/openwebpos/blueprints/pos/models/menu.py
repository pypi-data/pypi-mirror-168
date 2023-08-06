from openwebpos.extensions import db
from openwebpos.utils.sql import SQLMixin


class Menu(SQLMixin, db.Model):
    __tablename__ = 'menu'
    name = db.Column(db.String(255), nullable=False)
    active = db.Column(db.Boolean, default=True, nullable=False)
    menu_items = db.relationship('Item', backref='menu', lazy='dynamic')
    recepies = db.relationship('Recipe', backref='menu', lazy='dynamic')

    def not_empty(self):
        return self.menu_items.count() > 0

    @staticmethod
    def list_active():
        return Menu.query.filter_by(active=True).all()

    @staticmethod
    def insert_menus(name):
        """
        Inserts a menu into the database.
        """
        menus = [
            {'name': f'{name}'},
        ]

        for menu in menus:
            menu = Menu(**menu)
            menu.save()

    def __init__(self, **kwargs):
        super(Menu, self).__init__(**kwargs)


class Ingredient(SQLMixin, db.Model):
    __tablename__ = 'ingredients'

    name = db.Column(db.String(60))
    recipes = db.relationship('Recipe', backref='ingredient', lazy='dynamic')
    price = db.Column(db.Numeric(10, 2), nullable=False, default=0.00)
    addon = db.Column(db.Boolean, default=False)
    order_item_options = db.relationship('OrderItemOption',
                                         backref='ingredient', lazy='dynamic')
    active = db.Column(db.Boolean, default=True)

    @staticmethod
    def insert_ingredients(name):
        ingredients = [
            {'name': f'{name}'},
        ]

        for ingredient in ingredients:
            ingredient = Ingredient(**ingredient)
            ingredient.save()

    def not_in_menu(self, menu_id):
        return not self.in_menu(menu_id)

    def in_menu(self, menu_id):
        return Recipe.query.filter_by(ingredient_id=self.id,
                                      menu_id=menu_id).first()

    @staticmethod
    def list_ingredients_not_in_menu(menu_id):
        ingredients = Ingredient.query.filter_by(active=True).filter(
            ~Ingredient.recipes.any(menu_id=menu_id)).all()
        if ingredients:
            return ingredients
        return Ingredient.query.filter_by(active=True).all()

    def __init__(self, **kwargs):
        super(Ingredient, self).__init__(**kwargs)


class Item(SQLMixin, db.Model):
    __tablename__ = 'item'
    name = db.Column(db.String(255), nullable=False)
    price = db.Column(db.Numeric(10, 2), default=0.00, nullable=False)
    active = db.Column(db.Boolean, default=True, nullable=False)
    menu_id = db.Column(db.Integer, db.ForeignKey('menu.id'), nullable=False)
    order_items = db.relationship('OrderItem', backref='item',
                                  lazy='dynamic')

    @staticmethod
    def insert_items(name, price, menu_id):
        items = [
            {'name': f'{name}', 'price': {price}, 'menu_id': {menu_id}},
        ]

        for item in items:
            item = Item(**item)
            item.save()

    def __init__(self, **kwargs):
        super(Item, self).__init__(**kwargs)


class Recipe(SQLMixin, db.Model):
    __tablename__ = 'recipe'
    menu_id = db.Column(db.Integer, db.ForeignKey('menu.id'),
                        nullable=False)
    ingredient_id = db.Column(db.Integer, db.ForeignKey('ingredients.id'),
                              nullable=False)
    quantity = db.Column(db.Integer, default=1, nullable=False)

    def __init__(self, **kwargs):
        super(Recipe, self).__init__(**kwargs)
