from re import M
from flask_app import app
from flask import render_template,redirect,request,session,flash
from datetime import datetime
from flask_app.models.author import Author
from flask_app.models.book import Book

@app.route("/")
def load():
    return redirect("/authors")

@app.route("/authors")
def load_authors():
    authors = Author.get_all();
    return render_template("authors.html",all_authors=authors)

@app.route("/view_author/<idIn>")
def view_author(idIn):
    show_table=True
    show_add=True
    data={"id":int(idIn)}
    author = Author.get_favorites(data)
    
    books = Book.get_all()
    for item in author.favorites:
        for book in books:
            if book.id == item.id:
                books.remove(book)
    
    if books==[]:
        show_add=False
    if author.favorites==[]:
        show_table=False

    return render_template("view_author.html",author=author,books=books,showTable=show_table,showAdd=show_add)

@app.route("/add_author",methods=['POST'])
def add_author():
    data={
        "name": request.form['name'],
        "created_at": datetime.now(),
        "updated_at": datetime.now()
    }
    Author.save(data)
    return redirect('/authors')

@app.route("/add_favorite_book",methods=['POST'])
def add_favorite_book():
    data={
        "author_id": request.form['author_id'],
        "book_id": request.form['book_id'],
    }
    Author.add_fav_book(data)
    return redirect(f"/view_author/{request.form['author_id']}")