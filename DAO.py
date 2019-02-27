
import sqlite3
import os
from WebSearcher import WebSearcher

class DAO:
	def __init__(self):
		connect = sqlite3.connect('book.db')
		cursor = connect.cursor()
		cursor.execute("PRAGMA table_info(book)")
		checkTable = cursor.fetchall()

		print("===========================")
		print(checkTable)
		print("===========================")

		cursor.execute(" CREATE TABLE book ( isbn integer, title text, description text, language text)")
		connect.commit()
		connect.close()

		ws = WebSearcher()
		AddList(ws.SearchKotlinDB())

	def AddList(self, data):
		connect = sqlite3.connect('book.db')
		cursor = connect.cursor()

		sqlString = "INSERT INTO BOOK (isbn, title, description, language) VALUES "

		for book in data:
			sqlString += "(" + str(book['isbn']) + ", '" + str(book['title']) + "', '" + str(book['description']) + "', '" + str(book['language']) + "'" + "), "

		sqlString = sqlString[:-2]

		print("===========================")
		print(sqlString)
		print("===========================")

		return cursor.execute(sqlString)

	def AddSingle(self, book):
		connect = sqlite3.connect('book.db')
		cursor = connect.cursor()

		sqlString = "INSERT INTO BOOK (isbn, title, description, language) VALUES "
		sqlString += "(" + str(book['isbn']) + ", '" + str(book['title']) + "', '" + str(book['description']) + "', '" + str(book['language']) + "'" + ") "

		cursor.execute(sqlString)
		connect.commit()
		connect.close()

	def GetAll(self):
		connect = sqlite3.connect('book.db')
		cursor = connect.cursor()

		sqlString = "SELECT * FROM BOOK"
		data = cursor.execute(sqlString)
		connect.commit()
		connect.close()

		return data

	def Get(self, isbn):
		connect = sqlite3.connect('book.db')
		cursor = connect.cursor()

		sqlString = "SELECT * FROM BOOK WHERE isbn=" + str(isbn)
		data = cursor.execute(sqlString)
		connect.commit()
		connect.close()

		return data