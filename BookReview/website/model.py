from flask_login import UserMixin
from . import db

class BooksInfo(db.Model):
    BookID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    BookBarcode = db.Column(db.String(50), nullable=False)
    Press = db.Column(db.String(100), nullable=False)
    Edition = db.Column(db.String(100), default=None)
    Genre = db.Column(db.String(100), nullable=False)
    PublicationDate = db.Column(db.String(50), default=None)
    Language = db.Column(db.String(100), nullable=False)
    Author = db.Column(db.String(50), nullable=False)
    Description = db.Column(db.Text, nullable=False)

class BookStatistics(db.Model):
    book_statistic_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    BBookID = db.Column(db.Integer, db.ForeignKey(BooksInfo.BookID), nullable=False)
    NumOfLoans = db.Column(db.Integer, default=0)
    Surplus = db.Column(db.Integer, default=0)
    Total = db.Column(db.Integer, default=0)

    book_info = db.relationship('BooksInfo', backref='BookStatistics')

class Reader(db.Model, UserMixin):
    ReaderID = db.Column(db.Integer, primary_key=True, nullable=False)
    ReaderName = db.Column(db.String(20), nullable=False)
    ReaderPassword = db.Column(db.String(20), nullable=False, default="111111")
    Gender = db.Column(db.String(4), nullable=False)
    RegistrationDate = db.Column(db.Date, nullable=False)

    def get_id(self):
        return self.ReaderID

    def is_admin(self):
        return False

class Operator(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(50), nullable=False)

    # def __init__(self, id:str, name:str, password:str, access):
    #     self.name = name
    #     self.password = password
    #     self.id = id
    #     self.access = access

    # def is_authenticated(self):
    #     return True

    # def is_active(self):
    #     return True

    # def is_anonymous(self):
    #     return False

    # def get_id(self):
    #     return self.id

    def is_admin(self):
        return True
        #return self.access

class BorrowedBookInfo(db.Model):
    BBookID = db.Column(db.Integer, db.ForeignKey(BooksInfo.BookID), primary_key=True)
    BookBarcode = db.Column(db.String(50), nullable=False)
    StartTime = db.Column(db.DateTime, nullable=False)
    ExpiryTime = db.Column(db.DateTime, nullable=False)
    RenewAllowance = db.Column(db.Boolean, default=False)
    OperatorID = db.Column(db.Integer, db.ForeignKey(Operator.id), nullable=False)
    ReaderID = db.Column(db.Integer, db.ForeignKey(Reader.ReaderID), nullable=False)

    book_info = db.relationship('BooksInfo', backref='borrowed_book_info')
    operator = db.relationship('Operator', backref='borrowed_book_info')
    reader = db.relationship('Reader', backref='borrowed_book_info')

class BookStateTable(db.Model):
    BBookID = db.Column(db.Integer, db.ForeignKey(BooksInfo.BookID), primary_key=True)
    BookBarcode = db.Column(db.String(50), nullable=False)
    BookState = db.Column(db.String(50), default='reserved')
    OperatorID = db.Column(db.Integer, nullable=False)
    Renewable = db.Column(db.Boolean, default=False)

    book_info = db.relationship('BooksInfo', backref='book_state')

class AuthorInfo(db.Model):
    Author = db.Column(db.String(20), primary_key=True)
    BBookID = db.Column(db.Integer, db.ForeignKey(BooksInfo.BookID), primary_key=True)

    book_info = db.relationship('BooksInfo', backref='authors')
