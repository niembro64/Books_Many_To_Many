from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import author

class Book:
    def __init__( self , data ):
        self.id = data['id']
        self.title = data['title']
        self.num_of_pages = data['num_of_pages']
        self.favorited_by = []
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM books;"

        results = connectToMySQL('books_schema').query_db(query)

        books = []

        for book in results:
            books.append( cls(book) )
        return books
    
    @classmethod
    def get_one(cls, data):
        query = "SELECT * FROM books WHERE id=%(id)s;"

        result = connectToMySQL('books_schema').query_db(query,data)

        book = cls(result[0])

        return book
    
    @classmethod
    def edit(cls, data ):
        query = "UPDATE books SET title=%(title)s, num_of_pages=%(num_of_pages)s updated_at=NOW() WHERE id=%(id)s"
        
        result = connectToMySQL('books_schema').query_db(query,data)
        return result
    
    @classmethod
    def save(cls, data ):
        query = "INSERT INTO books ( title, num_of_pages , created_at, updated_at ) VALUES ( %(title)s , %(num_of_pages)s ,  NOW() , NOW() );"

        return connectToMySQL('books_schema').query_db( query, data )
    
    @classmethod
    def delete(cls, data ):
        query = "DELETE FROM books WHERE id=%(id)s"
        
        result = connectToMySQL('books_schema').query_db(query,data)
        return result
    
    @classmethod
    def get_favby(cls, data ):
        query = "SELECT * FROM books LEFT JOIN favorites ON favorites.book_id=books.id LEFT JOIN authors ON favorites.author_id=authors.id WHERE books.id=%(id)s"
        results = connectToMySQL('books_schema').query_db(query,data)
        
        book = cls(results[0])
        for row in results:
            if row['authors.id'] != None:
                author_data = {
                    "id": row['authors.id'],
                    "name": row['name'],
                    "created_at": row['authors.created_at'],
                    "updated_at": row['authors.updated_at'],
                }
                book.favorited_by.append( author.Author(author_data) )
        return book
    
    @classmethod
    def add_fav_author(cls,data):
        query = "INSERT INTO favorites (author_id, book_id) VALUES (%(author_id)s, %(book_id)s)"
        
        return connectToMySQL('books_schema').query_db(query,data)