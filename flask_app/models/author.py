from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import book

class Author:
    def __init__( self , data ):
        self.id = data['id']
        self.name = data['name']
        self.favorites = []
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM authors;"

        results = connectToMySQL('books_schema').query_db(query)

        authors = []

        for author in results:
            authors.append( cls(author) )
        return authors
    
    @classmethod
    def get_one(cls, data):
        query = "SELECT * FROM authors WHERE id=%(id)s;"

        result = connectToMySQL('books_schema').query_db(query,data)

        author = cls(result[0])

        return author
    
    @classmethod
    def edit(cls, data ):
        query = "UPDATE authors SET name=%(name)s, updated_at=NOW() WHERE id=%(id)s"
        
        result = connectToMySQL('books_schema').query_db(query,data)
        return result
    
    @classmethod
    def save(cls, data ):
        query = "INSERT INTO authors ( name , created_at, updated_at ) VALUES ( %(name)s ,  NOW() , NOW() );"

        return connectToMySQL('books_schema').query_db( query, data )
    
    @classmethod
    def delete(cls, data ):
        query = "DELETE FROM authors WHERE id=%(id)s"
        
        result = connectToMySQL('books_schema').query_db(query,data)
        return result
    
    @classmethod
    def get_favorites(cls, data ):
        query = "SELECT * FROM authors LEFT JOIN favorites ON favorites.author_id=authors.id LEFT JOIN books ON favorites.book_id=books.id WHERE authors.id=%(id)s"
        results = connectToMySQL('books_schema').query_db(query,data)
        
        author = cls(results[0])
        
        for row in results:
            if row['book_id'] != None:
                book_data = {
                    "id": row['books.id'],
                    "title": row['title'],
                    "num_of_pages": row['num_of_pages'],
                    "created_at": row['books.created_at'],
                    "updated_at": row['books.updated_at'],
                }
                author.favorites.append( book.Book(book_data) )
            
        return author
    
    @classmethod
    def add_fav_book(cls,data):
        query = "INSERT INTO favorites (author_id, book_id) VALUES (%(author_id)s, %(book_id)s)"
        
        return connectToMySQL('books_schema').query_db(query,data)