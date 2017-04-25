import json
import pprint
from config import *
import sys
import time
import requests
import time
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# from models import User, Message, 

# from sqlalchemy import MetaData
# # import certifi

# from sqlalchemy import create_engine

# engine = create_engine('mysql://scott:tiger@localhost/foo')

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:3512@localhost/test'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

db.drop_all()
# engine = create_engine('sqlite:////tmp/test.db')
# m = MetaData()
# m.reflect(engine)
# for table in m.tables.values():
# 	print(table.name)
# 	for column in table.c:
# 		print(column.name)


# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
# db = SQLAlchemy(app)


# class User(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(80), unique=True)
#     email = db.Column(db.String(120), unique=True)

#     def __init__(self, username, email):
#         self.username = username
#         self.email = email

#     def __repr__(self):
#         return '<User %r>' % self.username



class User(db.Model):
	__tablename__ = "user"
	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	username = db.Column(db.String(80), unique=True)
	email = db.Column(db.String(120), unique=True)
	created_at = db.Column('created_at', db.Date, default=datetime.utcnow)

	def __init__(self, username, email):
		self.username = username
		self.email = email

	def __repr__(self):
		return '<ID: %d, User: %s, Email: %s, created_at: %r>' % (self.id, self.username, self.email, self.created_at)


class Message(db.Model):
	__tablename__ = "message"
	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	sender_id = db.Column('sender_id', db.Integer, db.ForeignKey('user.id'))
	receiver_id = db.Column('receiver_id', db.Integer, db.ForeignKey('user.id'))
	created_at = db.Column('created_at', db.Date, default=datetime.utcnow)
	# sender = db.Column(db.String(80))
	# receiver = db.Column(db.String(80))
	type = db.Column(db.String(80))

	def __init__(self, sender_id, receiver_id):
		self.sender_id = sender_id
		self.receiver_id = receiver_id
		# self.sender = sender_id.username
		# self.receiver = receiver_id.username
		type = TextMessage

	def __repr__(self):
		return '<ID: %d, Sender: %s, Recv: %s, created_at: %r>' % (self.id, self.sender_id, self.receiver_id, self.created_at)

	__mapper_args__ = {
		'polymorphic_identity' : 'message',
		'polymorphic_on' : type
	}

class TextMessage(Message):
	id = db.Column(db.Integer, db.ForeignKey('message.id'), primary_key=True, autoincrement=True)
	text = db.Column(db.String(250))

	__mapper_args__ = {
		'polymorphic_identity' : 'text',
	}

class VideoMessage(Message):
	id = db.Column(db.Integer, db.ForeignKey('message.id'), primary_key=True, autoincrement=True)
	video_link = db.Column(db.String(250))
	length = db.Column(db.Integer)
	source = db.Column(db.String(100))

	__mapper_args__ = {
		'polymorphic_identity' : 'video',
	}

class ImageMessage(Message):
	id = db.Column(db.Integer, db.ForeignKey('message.id'), primary_key=True, autoincrement=True)
	image_link = db.Column(db.String(250))
	width = db.Column(db.Integer)
	height = db.Column(db.Integer)

	__mapper_args__ = {
		'polymorphic_identity' : 'image',
	}




@app.route("/")
def index():
	return "Hello"

@app.route("/show")
def showUsers():
	print(User.query.all())
	user_list = User.query.all()
	# users = {}
	users = []
	for u in user_list:
		print(u)
		usr = {
			"name":u.username, 
			"email":u.email, 
			"id":u.id,
			"created_at":u.created_at.strftime('%m/%d/%Y')
		}
		users.append(usr)
	return json.dumps(users)
# admin = User('sandra', 'sandra@email.com')

db.create_all()
# db.session.add(admin)
db.session.commit()
User.query.all()
Message.query.all()


# @app.route("/add-user/<username><email>")
# def addUser(username, email):
# 	user = User(username, email)
# 	db.session.add(user)
# 	db.session.commit()
# 	return redirect('/')
@app.route("/addUser", methods=['GET','POST'])
def addUser():
	# username = request.form['username']
	# email = request.form['email']
	if (request.method == 'GET'):
		username = request.args.get('username')
		email = request.args.get('email')
	else:
		username = request.form['username']
		email = request.form['email']
	print(username,email)
	
	try:
		user = User(username, email)
		db.session.add(user)
		db.session.commit()
	# except pymysql.err.IntegrityError:
	# except IntegrityError:
	except:
		print("User %s already in db" % username)

	return (username, email)
	# db.session.commit()
	# return json.dumps({'status':'OK','user':username,'email':email})

@app.route("/removeUser", methods=['GET','POST'])
def removeUserById():
	# username = request.form['username']
	# email = request.form['email']
	if (request.method == 'GET'):
		# username = request.args.get('username')
		# email = request.args.get('email')
		uid = request.args.get('id')
	else:
		# username = request.form['username']
		# email = request.form['email']
		uid = request.form['id']
	# print(username,email)
	print(uid)
	
	try:
		user = User(username, email)
		db.session.add(user)
		db.session.commit()
	# except pymysql.err.IntegrityError:
	# except IntegrityError:
	except:
		print("User %s already in db" % username)

	return (username, email)

@app.route("/textMessage", methods=['GET','POST'])
def createTextMessage():
	if (request.method == 'GET'):
		uid_send = int(request.args.get('sid'))
		uid_recv = int(request.args.get('rid'))
		m = str(request.args.get('msg'))
	else:
		uid_send = int(request.form['sid'])
		uid_recv = int(request.form['rid'])
		m = request.form['msg']
	print(uid_send,uid_recv, m)

	try:
		msg = Message(uid_send,uid_recv)
		# tmsg = TextMessage(msg)
		# print(m)
		# tmsg.text = m
		db.session.add(tmsg)
		db.session.commit()
	except:
		print("Message creation failed")

	# pprint(m)
	return (uid_send,uid_recv, m)

@app.route("/getMessageById", methods=['GET','POST'])
def fetchMessageById():
	if (request.method == 'GET'):
		mid = int(request.args.get('mid'))
		# uid_recv = int(request.args.get('rid'))
		# m = str(request.args.get('msg'))
	msg = Message.query.filter_by(id=mid)
	return msg






@app.route("/fetchMessage")
def fetchMessage():
	messages = Message.query.filter_by(sender_id=request.form['send'],receiver_id=request.form['recv'])
	return messages



if __name__ == "__main__":
	app.debug = True
	app.run(port=8000)
