from random import choice

from flask import render_template, request, make_response

from app import app, db, user_datastore
from models import Poem, Foto


@app.route('/')
def index():
    foto = choice(Foto.query.all())
    poem = choice(Poem.query.all())
    return render_template("index.html", foto=foto, poem=poem)


@app.route('/about')
def about():
    return render_template("about.html", title="Биография")


@app.route('/poems')
def works():
    per_page = 20
    all_pages = 1 + len(Poem.query.all()) // per_page
    request_page = request.args.get('page')
    if request_page and request_page.isdigit and int(request_page) <= all_pages:
        poem_page = int(request_page)
    else:
        poem_page = 1
    page = Poem.query.paginate(poem_page, per_page)
    return render_template("works.html", page=page, title="Произведения")


@app.route('/poems/<int:num>', methods=["GET", "POST"])
def piece_of_poetry(num):
    return render_template("poems.html", poem=Poem.query.get(num))


@app.route('/foto')
def foto():
    active = request.args.get('active')
    foto = Foto.query.all()
    if active and active.isdigit() and int(active) <= len(foto):
        active = int(active)
    else:
        active = 1
    return render_template("foto.html", title="Фотографии", foto=foto, active=active)


@app.route('/img/<ind>')
def get_img(ind):
    resp = make_response(Foto.query.get(ind).img)
    resp.headers['Content-Type'] = 'image/jpg'
    return resp


@app.route('/action')
def action():
    return render_template("action.html", title='События')


@app.route('/books')
def books():
    return render_template("books.html", title='Книги')


@app.errorhandler(404)
def not_found_error(error):
    return render_template('error.html', error=404), 404


@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('error.html', error=500), 500
