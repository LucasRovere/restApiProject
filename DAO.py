
import sqlite3
import os
from WebSearcher import WebSearcher

class DAO:
	def __init__(self):
		connect = sqlite3.connect('book.db')
		cursor = connect.cursor()
		cursor.execute("PRAGMA table_info(book)")
		checkTable = cursor.fetchall()
		# Se a tabela não existir, o sistema cria e popula com os dados do kotlin
		if len(checkTable) == 0:
			cursor.execute(" CREATE TABLE book ( id integer primary key, isbn text, title text, description text, language text)")
			connect.commit()
			connect.close()

			ws = WebSearcher()
			self.AddList(ws.SearchKotlinDB())

	def AddList(self, data):
		try:
			connect = sqlite3.connect('book.db')
			cursor = connect.cursor()

			sqlString = "INSERT INTO BOOK (isbn, title, description, language) VALUES (:isbn, :title, :description, :language)"

			cursor.executemany(sqlString, data)
			connect.commit()
			connect.close()

			return True

		except:
			return False

	def AddSingle(self, data):
		try:
			connect = sqlite3.connect('book.db')
			cursor = connect.cursor()

			sqlString = "INSERT INTO BOOK (isbn, title, description, language) VALUES (:isbn, :title, :description, :language)"

			cursor.execute(sqlString, data)
			connect.commit()
			connect.close()

			return True

		except:
			return False

	def GetAll(self):
		connect = sqlite3.connect('book.db')
		cursor = connect.cursor()

		sqlString = "SELECT * FROM BOOK"
		data = cursor.execute(sqlString)
		data = cursor.fetchall()
		connect.close()

		return data

	def Get(self, isbn):
		connect = sqlite3.connect('book.db')
		cursor = connect.cursor()

		sqlString = "SELECT * FROM BOOK WHERE isbn=" + str(isbn)
		cursor.execute(sqlString)
		data = cursor.fetchall()
		connect.close()

		return data