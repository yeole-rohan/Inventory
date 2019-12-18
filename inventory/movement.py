import functools
from flask import (
    Blueprint, render_template, redirect, url_for, request,flash
)

from werkzeug.exceptions import abort
from inventory.db import get_db

blueprint = Blueprint('movement', __name__)

@blueprint.route('/movement', methods=['GET', 'POST'])
def movement():
    prods = []
    locs = []
    db = get_db()
    products = db.execute('SELECT * FROM product ORDER BY id ASC')
    location = db.execute('SELECT * FROM location ORDER BY id ASC')
    movements = db.execute('SELECT * FROM product_movement ORDER BY id DESC')
    for i in products:
        prods.append(i)
    for j in location:
        locs.append(j)

    if request.method == 'POST':
        products_to = request.form['to']
        products_from = request.form['from']
        products_to_move = request.form['products']
        qty = request.form['quantity']
        if products_to and products_from and products_to_move and qty:
            db = get_db()
            db.execute('INSERT INTO product_movement (prod_id, from_loc, to_loc, quantity) VALUES (?, ?, ?, ?)',(products_to_move, products_from, products_to, qty))
            db.commit()
            return redirect(url_for('movement.movement'))
    return render_template('movement/movement.html',products=prods, location=locs, movements=movements)


def get_movement(id):
    product = get_db().execute('SELECT id, prod_id, from_loc, to_loc , quantity FROM product_movement WHERE id = ?',(id,)).fetchone()
    if product is None:
        abort(404, "Product Movement with id {} is not added in database. Goto home and add one".format(id))
    else:
        pass
    return product

@blueprint.route('/<int:id>/edit-movement', methods=['GET','POST'])
def edit_movement(id):
    lists = []

    movement = get_movement(id)
    for i in movement:
        lists.append(i)
    if request.method == 'POST':
        products_to_move = request.form['products']
        qty = request.form['quantity']
        error = None
        if products_to_move and qty:
            db = get_db()
            db.execute('UPDATE product_movement SET prod_id = ?, quantity = ? WHERE id = ?', (products_to_move, qty, id))
            db.commit()
        return redirect(url_for('movement.movement'))
    return render_template('movement/edit-movement.html', lists=lists)