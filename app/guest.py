from flask import (
    Blueprint, render_template, request, url_for, redirect
)
from werkzeug.exceptions import abort

from app.db import get_db

bp = Blueprint('guest', __name__, url_prefix='/guest')

@bp.route('/')
def guests():
    db = get_db()
    guests = db.execute(
        'SELECT id, nick, message, created'
        ' FROM guests ORDER BY created DESC'
    ).fetchall()

    return render_template('guests.html', guests=guests)


def get_guest(id):
    guest = get_db().execute(
        'SELECT id, nick, created, message FROM guests WHERE id = ?', (id,)
    ).fetchone()

    if guest is None:
        abort(404)

    return guest


@bp.route('/create', methods=['POST'])
def create_guest():
    nick = request.form['nick']
    message = request.form['message']
    error = None

    if not nick:
        flash('Nick is required')
    else:
        db = get_db()
        db.execute(
            'INSERT INTO guests (nick, message) VALUES (?, ?)', (nick, message)
        )
        db.commit()

    return redirect(url_for('guest.guests'))


@bp.route('/<int:id>/delete', methods=['GET'])
def delete_guest(id):
    get_guest(id)
    db = get_db()
    db.execute('DELETE FROM guests WHERE id = ?', (id,))
    db.commit()

    return redirect(url_for('guest.guests'))