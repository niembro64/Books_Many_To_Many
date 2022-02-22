from turtle import showturtle
from flask_app import app
from flask import render_template,redirect,request,session,flash
from datetime import datetime
from flask_app.models.book import Book
from flask_app.models.author import Author

@app.route("/books")
def load_books():
    books = Book.get_all();
    return render_template("books.html",all_books=books)

@app.route("/view_book/<idIn>")
def view_book(idIn):
    show_table=True
    show_add=True
    data={"id":idIn}
    book=Book.get_favby(data)
    authors = Author.get_all()
    for item in book.favorited_by:
        for author in authors:
            if author.id == item.id:
                authors.remove(author)
    if book.favorited_by==[]:
        show_table=False
    if authors==[]:
        show_add=False
    return render_template("view_book.html",book=book, authors=authors, showTable=show_table,showAdd=show_add)

@app.route("/add_book",methods=['POST'])
def add_book():
    data={
        "title": request.form['title'],
        "num_of_pages": request.form['num_of_pages'],
        "created_at": datetime.now(),
        "updated_at": datetime.now()
    }
    print(Book.save(data))
    return redirect("/books")


@app.route("/add_favorite_author",methods=['POST'])
def add_favorite_author():
    data={
        "author_id": request.form['author_id'],
        "book_id": request.form['book_id'],
    }
    Book.add_fav_author(data)
    return redirect(f"/view_book/{request.form['book_id']}")