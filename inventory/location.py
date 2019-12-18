import functools
from flask import (
    Blueprint, render_template, redirect, url_for, request,flash
)

from werkzeug.exceptions import abort
from inventory.db import get_db

blueprint = Blueprint('location', __name__)

@blueprint.route('/warehouse', methods=['GET', 'POST'])
def warehouse():
    db = get_db()
    all = db.execute('SELECT * FROM location ORDER BY loc_name')
    if request.method == 'POST':
        ware_house = request.form['warehouse']
        print(ware_house)
        if ware_house:
            db = get_db()
            db.execute('INSERT INTO location (loc_name) VALUES (?)', (ware_house,))
            db.commit()
        return redirect(url_for('location.warehouse'))
    return render_template('location/warehouse.html', all=all)


def get_location(id):
    product = get_db().execute('SELECT loc_name FROM location WHERE id = ?',(id,)).fetchone()

    if product is None:
        abort(404, "Location with id {} is not added in database. Goto home and add one".format(id))
    else:
        pass
    return product


@blueprint.route('/<int:id>/edit-warehouse', methods=['GET','POST'])
def edit_warehouse(id):
    location = get_location(id)
    if request.method == 'POST':
        name = request.form['warehouse']
        error = None
        if not name:
            error = 'You removed all details of product'
        
        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute('UPDATE location SET loc_name = ? WHERE id = ?', (name, id))
            db.commit()
        return redirect(url_for('location.warehouse'))
    return render_template('location/edit-warehouse.html', location=location)