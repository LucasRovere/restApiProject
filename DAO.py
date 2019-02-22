
import sqlite3

class DAO:
	def __init__(self):
		self.connect = sqlite3.connect('book.db')
		print(self.connect)
		self.cursor = self.connect.cursor()

		self.cursor.execute("""	CREATE TABLE
							IF NOT EXISTS book (
            					isbn integer,
            					title text,
            					description text,
            					language text
            				)""")

	def AddList(self, data):
		sqlString = "INSERT INTO BOOK (isbn, title, description, language) VALUES "

		for book in data:
			sqlString += "(" + str(book['isbn']) + ", '" + str(book['title']) + "', '" + str(book['description']) + "', '" + str(book['language']) + "'" + "), "

		return self.cursor.execute(sqlString)

	def AddSingle(self, book):
		sqlString = "INSERT INTO BOOK (isbn, title, description, language) VALUES "
		sqlString += "(" + str(book['isbn']) + ", '" + str(book['title']) + "', '" + str(book['description']) + "', '" + str(book['language']) + "'" + "), "

		return self.cursor.execute(sqlString)

	def GetAll(self):
		sqlString = "SELECT * FROM BOOK"
		return self.cursor.execute(sqlString)

	def Get(self, isbn):
		sqlString = "SELECT * FROM BOOK WHERE isbn=" + str(isbn)
		return self.cursor.execute(sqlString)