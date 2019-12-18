import functools
from flask import (
    Blueprint, render_template, url_for, flash, request, redirect
)
from werkzeug.exceptions import abort
from inventory.db import get_db

blueprint = Blueprint('product', __name__)

@blueprint.route('/')
def index():
    db = get_db()
    all_data = db.execute('SELECT prod_id, to_loc, quantity from product_movement ORDER BY to_loc')
    return render_template('index.html', all_data=all_data)

@blueprint.route('/add', methods=['GET', 'POST'])
def add():
    db = get_db()
    products = db.execute('SELECT * FROM product ORDER BY id DESC')
    if request.method == 'POST':
        name = request.form['product']
        qty = request.form['quantity']
        error = None
        if not name and qty:
            error = 'You possibly forget to add product name and quantity....'
        
        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute('INSERT INTO product (product_name, product_quantity) VALUES (?, ?)', (name, qty))
            db.commit()
            return redirect(url_for('product.add'))
    return render_template('product/add.html',products=products)

def get_product(id):
    product = get_db().execute('SELECT product_name, product_quantity FROM product WHERE id = ?',(id,)).fetchone()

    if product is None:
        abort(404, "Product with id {} is not added in database. Goto home and add one".format(id))
    else:
        pass
    return product

@blueprint.route('/<int:id>/edit', methods=['GET','POST'])
def edit(id):
    product = get_product(id)
    if request.method == 'POST':
        name = request.form['product']
        qty = request.form['quantity']
        error = None
        if not name and qty:
            error = 'You removed all details of product'
        
        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute('UPDATE product SET product_name = ?, product_quantity = ? WHERE id = ?', (name, qty, id))
            db.commit()
        return redirect(url_for('product.index'))
    return render_template('product/edit.html', product=product)