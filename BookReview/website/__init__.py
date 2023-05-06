from flask import Flask
from os import path
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

from sqlalchemy.orm import sessionmaker
import json
from datetime import datetime
from sqlalchemy.exc import IntegrityError

users = []
db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'asjkdlIL123HNMSQO'
    # app.config['MYSQL_DATABASE_USER'] = 'root'
    # app.config['MYSQL_HOST'] = 'localhost'
    # app.config['MYSQL_PASSWORD'] = ''
    # app.config['MYSQL_DATABASE_DB'] = 'milestone3'
    app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///database.db'
    db.init_app(app)

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .model import AuthorInfo, BooksInfo, Operator, Reader, BookStatistics

    with app.app_context():
        db.create_all()

        engine = db.get_engine()
        Session = sessionmaker(bind=engine)
        session = Session()

        with open('dbcsv\Author.json', 'r') as f:
            authors = json.load(f)
            for author in authors:
                try:
                    authorinfo = AuthorInfo(
                        Author=author['Author'], BBookID=author['BBookID'])
                    session.add(authorinfo)
                    session.commit()
                    print("Added an author")
                except IntegrityError:
                    session.rollback()

        with open('dbcsv\Book_Statistic.json', 'r') as f:
            bookstats = json.load(f)
            for bookstat in bookstats:
                try:
                    existingStat = session.query(BookStatistics).filter_by(BBookID=bookstat['BBookID']).first()
                    if not existingStat:
                        stat = BookStatistics(
                            BBookID=bookstat['BBookID'], NumOfLoans=bookstat['NumofLoans'], Surplus=bookstat['Surplus'], Total=bookstat['Total'])
                        session.add(stat)
                        session.commit()
                        print("Added a stat")
                except IntegrityError:
                    session.rollback()


        with open('dbcsv\Books.json', 'r') as f:
            books = json.load(f)
            for book in books:
                try:
                    bookInfo = BooksInfo(BookID=book['BookID'], BookBarcode=book['BookBarcode'], Press=book['Press'], Edition=book['Edition'],
                                         Genre=book['GenreName'], PublicationDate=datetime.strptime(book['DatePublication'], '%Y-%m-%d'), Language=book['Language'], Author=book['Author'], Description=book['Description'])
                    session.add(bookInfo)
                    session.commit()
                    print("Added a book")
                except IntegrityError:
                    session.rollback()

        with open('dbcsv\Reader.json', 'r') as f:
            readers = json.load(f)
            for reader in readers:
                try:
                    reader = Reader(
                        ReaderID=reader['ReaderID'], ReaderName=reader['ReaderName'], ReaderPassword=reader['ReaderPassword'], Gender=reader['Gender'], RegistrationDate=datetime.strptime(reader['RegistrationDate'], '%Y-%m-%d'))
                    session.add(reader)
                    session.commit()
                    print("Added a reader")
                except IntegrityError:
                    session.rollback()

    loginManager = LoginManager()
    loginManager.login_view = 'auth.login'
    loginManager.init_app(app)

    @loginManager.user_loader
    def loadUser(id):
        # looking for entries for their primary keys
        if Reader.query.get(int(id)):
            return Reader.query.get(int(id))
        else:
            return Operator.query.get(int(id))

    # @login_manager.user_loader
    # def load_user(id):
    #     for user in users:
    #         if id == user.get_id():
    #             user.to_string()
    #             return user
    #     return None

    return app
