from app import db #import database connection created in app.py
from sqlalchemy.dialects.postgresql import JSON

class Result(db.Model):
	""" Create a table to store the results of the word counts  """
	__tablename__ = 'results'

	id = db.Column(db.Integer, primary_key=True) # id of the result stored
	url = db.Column(db.String()) # url that we counted the words from
	result_all = db.Column(JSON) # full list of words that we counted
	result_no_stop_words = db.Column(JSON) # list of words counted minus stop words

	def __init__(self, url, result_all, result_no_stop_words):
		self.url = url
		self.result_all = result_all
		self.result_no_stop_words = result_no_stop_words
		
	def __repr__(self):
		return '<id  {}>'.format(self.id)
