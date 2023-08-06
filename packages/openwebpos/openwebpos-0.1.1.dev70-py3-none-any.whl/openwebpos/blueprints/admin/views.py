import datetime

from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required

from openwebpos.blueprints.user.decorators import admin_required
from openwebpos.blueprints.pos.models.menu import Menu, Item, Ingredient, Recipe
from openwebpos.blueprints.pos.models.order import OrderPager, OrderType, \
    TransactionType, Order, Transaction

from .forms import MenuForm, MenuItemForm, PagerForm, IngredientForm

bp = Blueprint('admin', __name__, template_folder='templates',
               url_prefix='/admin')
admin_menu = Blueprint('admin_menu', __name__, url_prefix='/menu')
bp.register_blueprint(admin_menu)


@bp.before_request
@login_required
@admin_required
def before_request():
    """
    Protects all the admin endpoints.
    """
    pass


@admin_menu.route('/')
def index():
    return render_template('admin/menu/index.html')


@bp.get('/')
def index():
    """
    Render the admin index page.
    """
    return render_template('admin/index.html', title='Admin')


@bp.get('/settings')
def settings():
    """
    Renders the admin settings page.
    """
    return render_template('admin/settings.html', title='Admin - Settings')


@bp.get('/config')
def config():
    """
    Renders the admin config page.
    """
    return render_template('admin/config.html', title='Admin - Config')


@admin_menu.get('/menus')
def menus():
    """
    Renders the admin menus page.
    """
    _menus = Menu.query.all()
    form = MenuForm()
    return render_template('admin/menus.html', title='Admin - Menus',
                           menus=_menus, form=form)


@admin_menu.post('/menus')
def add_menus():
    """
    Adds a menu to the database.
    """
    form = MenuForm()
    if form.validate_on_submit():
        m = Menu(name=form.name.data)
        m.save()
        return redirect(url_for('admin.menu_items', menu_name=m.name))
    return redirect(url_for('admin.menus'))


@admin_menu.post('/menu/<int:menu_id>/update')
def update_menu(menu_id):
    """
    Updates a menu in the database.
    """
    form = MenuForm()
    if form.validate_on_submit():
        m = Menu.query.get(menu_id)
        m.name = form.name.data
        m.save()
        return redirect(url_for('admin.menus'))
    return redirect(url_for('admin.menus'))


@admin_menu.get('/menu/<int:menu_id>/delete')
def delete_menu(menu_id):
    """
    Deletes a menu from the database.
    """
    m = Menu.query.get_or_404(menu_id)
    if m.not_empty():
        return redirect(url_for('admin.menus'))
    m.delete()
    return redirect(url_for('admin.menus'))


@admin_menu.get('/menu/<string:menu_name>/items')
def menu_items(menu_name):
    """
    Renders the admin menu items page.
    """
    _menu = Menu.query.filter_by(name=menu_name).first_or_404()
    _menu_items = Item.query.filter_by(menu_id=_menu.id).all()
    _menu_ingredients = Recipe.query.filter_by(menu_id=_menu.id).all()
    # _ingredients = Ingredient.query.filter_by(active=True).all()
    _ingredients = Ingredient.list_ingredients_not_in_menu(_menu.id)
    form = MenuItemForm()
    _title = f'Admin - {_menu.name} Menu Items'
    return render_template('admin/menu_items.html', title=_title,
                           menu_items=_menu_items, menu=_menu, form=form,
                           menu_ingredients=_menu_ingredients,
                           ingredients=_ingredients)


@admin_menu.post('/menu/<string:menu_name>/items')
def add_menu_items(menu_name):
    """
    Adds a menu item to the database.
    """
    form = MenuItemForm()
    if form.validate_on_submit():
        m = Menu.query.filter_by(name=menu_name).first_or_404()
        mi = Item(name=form.name.data, price=form.price.data, menu_id=m.id)
        mi.save()
        return redirect(url_for('admin.menu_items', menu_name=menu_name))
    return redirect(url_for('admin.menu_items', menu_name=menu_name))


@admin_menu.route('/menu/<string:menu_name>/item/<string:menu_item_name>/edit',
          methods=['GET', 'POST'])
def edit_menu_item(menu_name, menu_item_name):
    """
    Updates a menu item in the database.
    """
    form = MenuItemForm(
        obj=Item.query.filter_by(name=menu_item_name).first_or_404())
    _item_id = Item.query.filter_by(
        name=menu_item_name).first_or_404().id
    _ingredients = Ingredient.query.filter_by(active=True).all()
    if form.validate_on_submit():
        mi = Item.query.filter_by(name=menu_item_name).first_or_404()
        mi.name = form.name.data
        mi.price = form.price.data
        mi.save()
        return redirect(url_for('admin.menu_items', menu_name=menu_name))
    return render_template('admin/edit_menu_item.html', form=form,
                           ingredients=_ingredients,
                           item_id=_item_id)


@bp.get('/menu/<string:menu_name>/<string:menu_item_name>/delete')
def delete_menu_item(menu_name, menu_item_name):
    """
    Deletes a menu item from the database.
    """
    m = Menu.query.filter_by(name=menu_name).first_or_404()
    mi = Item.query.filter_by(name=menu_item_name,
                              menu_id=m.id).first_or_404()
    mi.delete()
    return redirect(url_for('admin.menu_items', menu_name=menu_name))


@bp.get('/menu/<string:menu_name>/<string:menu_item_name>/active-toggle')
def toggle_menu_item_active(menu_name, menu_item_name):
    """
    Toggles the active state of a menu item.
    """
    m = Menu.query.filter_by(name=menu_name).first_or_404()
    mi = Item.query.filter_by(name=menu_item_name,
                              menu_id=m.id).first_or_404()
    mi.active = not mi.active
    mi.save()
    return redirect(url_for('admin.menu_items', menu_name=menu_name))


@bp.get('/pagers')
def pagers():
    """
    Renders the admin pagers page.
    """
    _pagers = OrderPager.query.filter_by(hidden=False).all()
    form = PagerForm()
    return render_template('admin/pagers.html', title='Admin - Pagers',
                           pagers=_pagers, form=form)


@bp.post('/pagers')
def add_pagers():
    """
    Adds a pager to the database.
    """
    form = PagerForm()
    if form.validate_on_submit():
        p = OrderPager(name=form.name.data)
        p.save()
        return redirect(url_for('admin.pagers'))
    return redirect(url_for('admin.pagers'))


@bp.get('/pagers/<int:pager_id>/active-toggle')
def toggle_pager_active(pager_id):
    """
    Toggles the active state of a pager.
    """
    p = OrderPager.query.get_or_404(pager_id)
    p.active = not p.active
    p.save()
    return redirect(url_for('admin.pagers'))


@bp.get('/pagers/<int:pager_id>/delete')
def delete_pager(pager_id):
    """
    Deletes a pager from the database.
    """
    p = OrderPager.query.get_or_404(pager_id)
    p.delete()
    return redirect(url_for('admin.pagers'))


@bp.get('/order-types')
def order_types():
    """
    Renders the admin order types page.
    """
    _order_types = OrderType.query.all()
    return render_template('admin/order_types.html',
                           title='Admin - Order Types',
                           order_types=_order_types)


@bp.get('/order-types/<int:order_type_id>/active-toggle')
def toggle_order_type_active(order_type_id):
    """
    Toggles the active state of an order type.
    """
    ot = OrderType.query.get_or_404(order_type_id)
    ot.active = not ot.active
    ot.save()
    return redirect(url_for('admin.order_types'))


@bp.get('/transaction-types')
def transaction_types():
    """
    Renders the admin transaction types page.
    """
    _transaction_types = TransactionType.query.all()
    return render_template('admin/transaction_types.html',
                           title='Admin - Transaction Types',
                           transaction_types=_transaction_types)


@bp.get('/transaction-types/<int:transaction_type_id>/active-toggle')
def toggle_transaction_type_active(transaction_type_id):
    """
    Toggles the active state of a transaction type.
    """
    tt = TransactionType.query.get_or_404(transaction_type_id)
    tt.active = not tt.active
    tt.save()
    return redirect(url_for('admin.transaction_types'))


@bp.get('/ingredients')
def ingredients():
    """
    Renders the admin ingredients page.
    """
    _ingredients = Ingredient.query.all()
    form = IngredientForm()
    return render_template('admin/ingredients.html',
                           title='Admin - Ingredients',
                           ingredients=_ingredients, form=form)


@bp.post('/ingredients')
def add_ingredient():
    """
    Adds an ingredient to the database.
    """
    form = IngredientForm()
    if form.validate_on_submit():
        i = Ingredient(name=form.name.data)
        i.save()
        return redirect(url_for('admin.ingredients'))
    return redirect(url_for('admin.ingredients'))


@bp.get('/recipe/<int:menu_id>/<int:ingredient_id>/add')
def add_recipe(menu_id, ingredient_id):
    """
    Renders the admin add recipe page.
    """
    _menu = Menu.query.get_or_404(menu_id)
    _ingredient = Ingredient.query.get_or_404(ingredient_id)
    _recipe = Recipe(menu_id=_menu.id, ingredient_id=_ingredient.id)
    _recipe.save()
    return redirect(url_for('admin.menu_items', menu_name=_menu.name))


@bp.get('/orders')
def orders():
    """
    Renders the admin orders page.
    """
    _orders = Order.query.all()
    return render_template('admin/orders.html', title='Admin - Orders',
                           orders=_orders)


@bp.get('/orders/<int:order_id>/delete')
def delete_order(order_id):
    """
    Deletes an order from the database.
    """
    Order.delete_order(order_id)
    return redirect(url_for('admin.orders'))
