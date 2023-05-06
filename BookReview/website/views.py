from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user, logout_user
from datetime import datetime
from sqlalchemy.orm import Session, sessionmaker, joinedload
from sqlalchemy.sql import text
from . import db
from . import users

from .model import BorrowedBookInfo, BooksInfo, AuthorInfo, Reader, BookStatistics

views = Blueprint('views', __name__)


@views.route('/dashboard')
@login_required
def dashboard():

    books = BorrowedBookInfo.query.all()
    print("Borrowed Book Info: ", len(books))
    for book in books:
        print(book.BBookID)
        print(book.BookBarcode)

    return render_template('dashboard.html', user=current_user, fetch=books)


@views.route('/addbooks', methods=['GET', 'POST'])
@login_required
def addbooks():
    if request.method == 'POST':
        BookBarcode = request.form.get('BookBarcode')
        Press = request.form.get('Press')
        Edition = request.form.get('Edition')
        Genre = request.form.get('Genre')
        PublicationDate = request.form.get('PublicationDate')
        Language = request.form.get('Language')
        Author = request.form.get('Author')
        Description = request.form.get('Description')

        newBook = BooksInfo(BookBarcode=BookBarcode, Press=Press, Edition=Edition,
                            Genre=Genre, PublicationDate=PublicationDate, Language=Language, Author=Author, Description=Description)
        db.session.add(newBook)
        db.session.commit()
        print("Added New Book")
        print(BookBarcode, Press, Edition, Genre,
              PublicationDate, Language, Author, Description)

        tests = BooksInfo.query.all()
        print("Number of books: ", len(tests))
        for test in tests:
            print(test)

        newAuthor = AuthorInfo(Author=Author, BBookID=newBook.BookID)
        db.session.add(newAuthor)
        db.session.commit()
        print("Added New Author")
        print(newAuthor.Author, newAuthor.BBookID)

    # SELECT * FROM BooksInfo INNER JOIN BookStatistics ON BooksInfo.BookID = BookStatistics.BBookID

    # stats = BookStatistics.query.all()
    # print("Book stats: ", len(stats))
    # # for stat in stats:
    # #     print(stat)

    # asd = BooksInfo.query.all()
    # print("Books: ", len(asd))
    # for book in asd:
    #     print(asd)

    #books = db.session.query.join(BooksInfo, BookStatistics.BBookID==BooksInfo.BookID).all()

    books = db.session.query(BookStatistics, BooksInfo).join(
        BooksInfo, BookStatistics.BBookID == BooksInfo.BookID).all()
    return render_template('addbooks.html', user=current_user, fetch=books)


@views.route('/addusers', methods=['GET', 'POST'])
@login_required
def addusers():
    # msg = ''
    # connection = db.connect()
    # cursor = connection.cursor()
    # if request.method == 'POST':
    #     readerName = request.form.get('readername')
    #     readerPassword = request.form.get('readerpassword')
    #     readerGender = request.form.get('gender')
    #     readerID = request.form.get('readerID')

    #     try:
    #         cursor.execute(f"INSERT INTO READER (ReaderName, ReaderPassword, Gender, RegistrationDate)\
    #                         VALUES ('{readerName}', '{readerPassword}', '{readerGender}', '{datetime.now()}')")
    #         connection.commit()
    #         msg = 'sucessfully inserted'
    #     except Exception as e:
    #         msg = 'an erro has occured when inserting, please try again'
    # cursor.execute("SELECT * FROM Reader")
    # fetch = cursor.fetchall()
    # cursor.close()

    if request.method == 'POST':
        ReaderID = request.form.get('ReaderID')
        ReaderName = request.form.get('ReaderName')
        ReaderPassword = request.form.get('ReaderPassword')
        Gender = request.form.get('Gender')

        newReader = Reader(ReaderID=ReaderID, ReaderName=ReaderName,
                           ReaderPassword=ReaderPassword, Gender=Gender, RegistrationDate=datetime.now())
        db.session.add(newReader)
        db.session.commit()
        print("Added New Reader")
        print(newReader.ReaderID, newReader.ReaderName,
              newReader.ReaderPassword, newReader.Gender)

    readers = Reader.query.all()
    for reader in readers:
        print(reader)
        attributes = list(reader.__dict__.values())
        print(attributes)

    return render_template('addusers.html', user=current_user, fetch=readers)


@views.route('/userdash', methods=['GET', 'POST'])
@login_required
def userdash():
    # msg = ''
    # connection = db.connect()
    # cursor = connection.cursor()
    # if request.method == 'POST':
    #     readerid = current_user.get_id()
    #     bookbarcode = request.form.get('bookbarcode')
    #     expirytime = request.form.get('expiredate')
    #     operatorid = request.form.get('operatorid')
    #     renew = request.form.get('renew')
    #     try:
    #         cursor.execute(f'SELECT BookID FROM BooksInfo WHERE BookBarcode = "{bookbarcode}"')
    #         fetch = cursor.fetchone()
    #         print(fetch)
    #         cursor.execute(f'INSERT INTO BorrowedBookInfo (BBookID, BookBarcode, startTime, ExpiryTime, RenewAllowance, OperatorID, ReaderID)\
    #                        VALUES ({fetch[0]}, "{bookbarcode}", "{datetime.now().date()}", "{expirytime}", {renew}, {operatorid}, {readerid})')
    #         connection.commit()
    #     except Exception as e:
    #         msg = 'Something went wrong' + str(e)

    # cursor.execute(f'SELECT * FROM BorrowedBookInfo WHERE ReaderID = {current_user.get_id()}')
    # fetch = cursor.fetchall()
    # cursor.close()
    ReaderID = current_user.get_id()
    print("type of reader id is: ", type(ReaderID))
    if request.method == 'POST':

        BookBarcode = request.form.get('BookBarcode')
        ExpiryTime = request.form.get('ExpiryTime')
        ExpiryTime = datetime.strptime(ExpiryTime, '%Y-%m-%d')
        OperatorID = request.form.get('OperatorID')
        RenewAllowance = request.form.get('RenewAllowance')

        tests = BooksInfo.query.all()
        for test in tests:
            if test.BookBarcode == 'GHE12384':
                print(test.BookBarcode)

        book = db.session.query(BooksInfo).filter_by(
            BookBarcode=BookBarcode).first()
        print("trying to print a book: ", book)

        print("Printing bookid: ", book.BookID)
        print("Type of book id: ", type(book.BookID))

        OperatorID = int(OperatorID)
        ReaderID = int(ReaderID)

        newBorrowed = BorrowedBookInfo(BBookID=book.BookID, BookBarcode=book.BookBarcode, StartTime=datetime.now(), ExpiryTime=ExpiryTime, RenewAllowance=RenewAllowance, OperatorID=OperatorID, ReaderID=ReaderID)
        db.session.add(newBorrowed)
        db.session.commit()

    borrowed = db.session.query(BorrowedBookInfo).filter_by(
        ReaderID=ReaderID).all()

    return render_template('userdash.html', user=current_user, fetch=borrowed)


@views.route('/signout')
@login_required
def signout():
    users.clear()
    logout_user()
    return redirect(url_for('auth.login'))

@views.route('/front_end')
@login_required
def get_message():
    return render_template('front_end.html',  user=current_user)