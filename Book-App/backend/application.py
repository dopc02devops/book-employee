import os
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from logger import book_logger

app = Flask(__name__)
app.config.from_pyfile('config.py')
secret = app.config.get('SECRETS')
operating_system = os.getenv('OPERATING_SYSTEM')

if operating_system.lower() == "minikube":
    db_Url = app.config.get('MINIKUBE_DB')
elif operating_system.lower() == "kubernetes":
    db_Url = app.config.get('KUBERNETES_DB')
else:
    db_Url = app.config.get('LOCAL_DB')

app.config['SQLALCHEMY_DATABASE_URI'] = db_Url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = secret
db = SQLAlchemy(app)
logger = book_logger()


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float)

    def __init__(self, title, author, price):
        self.title = title
        self.author = author
        self.price = price


with app.app_context():
    logger.info('creating model')
    db.create_all()
    logger.info('model create completed')


@app.route('/book/index')
def index():
    books = Book.query.all()
    logger.info('making request to index page')
    return render_template('index.html', books=books)


@app.route('/book/add/', methods=['POST'])
def insert_book():
    logger.info('making request to add book')
    try:
        if request.method == "POST":
            book = Book(
                title=request.form.get('title'),
                author=request.form.get('author'),
                price=request.form.get('price')
            )
            logger.info(f'added book tittle is: {book.title}')
            logger.info(f'added book author is: {book.author}')
            logger.info(f'added book price is: {book.price}')
            logger.info(f'added book id is: {book.id}')
            db.session.add(book)
            logger.info('adding book to add db session')
            db.session.commit()
            logger.info('committing added book')
            flash("Book added successfully")
            logger.info('book successfully added')
            logger.info('redirecting to index page')
            logger.info('making request to index page')
            return redirect(url_for('index'))
    except Exception as ex:
        logger.error(f'An error occurred {ex}')


@app.route('/book/update/', methods=['POST'])
def update():
    logger.info('making request to update book')
    try:
        if request.method == "POST":
            logger.info('getting book data from request')
            my_data = Book.query.get(request.form.get('id'))
            my_data.title = request.form['title']
            my_data.author = request.form['author']
            my_data.price = request.form['price']
            logger.info(f'updated book tittle is: {my_data.title}')
            logger.info(f'updated book author is: {my_data.author}')
            logger.info(f'updated book price is: {my_data.price}')
            logger.info(f'updated book id is: {my_data.id}')

            db.session.commit()
            logger.info('committing update for updated book')
            flash("Book is updated")
            logger.info('book successfully updated')
            logger.info('making request to index page')
            return redirect(url_for('index'))
    except Exception as ex:
        logger.error(f'An error occurred {ex}')


@app.route('/book/delete/<int:id>/', methods=['GET', 'POST'])
def delete(id):
    logger.info('making request to delete book')
    try:
        if request.method == "POST":
            my_data = Book.query.get(id)
            logger.info('book data to be deleted')
            db.session.delete(my_data)
            logger.info('adding book to delete session')
            db.session.commit()
            logger.info('committing delete book request request')
            flash("Book is deleted")
            logger.info('book successfully deleted')
            logger.info('making request to index page')
            return redirect(url_for('index'))
    except Exception as ex:
        logger.error(f'An error occurred {ex}')


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8081)
    # app.run(host='0.0.0.0', port=8080, debug=True, threaded=True)
