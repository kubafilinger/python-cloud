from flask import Blueprint, request, render_template, make_response, redirect, url_for
from flask_dance.contrib.github import github
from flask_dance.contrib.google import google

bp = Blueprint('pages', __name__, url_prefix='/')

@bp.route('/')
def index():
    loggedName = 'test'
    loggedNameGoogle = 'test'

    if not github.authorized:
        return redirect(url_for('github.login'))
    else:
        user = github.get('/user')

        if user.ok:
            loggedName = user.json()['login']


    if not google.authorized:
        return redirect(url_for('google.login'))
    else:
        user = google.get("/plus/v1/people/me")

        if user.ok:
            loggedNameGoogle = user.json()["emails"][0]["value"]


    return render_template('index.html', name=loggedName, googleName=loggedNameGoogle)

@bp.route('/about')
def about():
    return render_template('about.html', name="Kuba", lastName="Filinger")

@bp.route('/gallery')
def gallery():
    return render_template('gallery.html')

@bp.route('/contact')
def contact():
    return render_template('contact.html')