from flask import Flask, url_for, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO
import datetime

app = Flask(__name__)
app.config["SECRET_KEY"] = "zx#$¥\®\°\¥SDFHXGHVC"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///chat.sqlite3"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
socket = SocketIO(app)

class Chat(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	content = db.Column(db.String())
	time = db.Column(db.String())
	
	def __repr__(self):
		return f"<Chat : {self.content}>"
		
with app.app_context():
	db.create_all()

@app.route("/")

def index():
	return render_template("index.html", all_chat=Chat.query.all())
	
	
@socket.on("recvmsg")
def process(data):
	
	chat_text = str(data)
	time = datetime.datetime.now()
	m_time = time.strftime("%H : %M")
	print("chatting")
	db.session.add(Chat(content=chat_text, time =str(m_time) ))
	db.session.commit()
	print("Chat added to db")
	x = Chat.query.filter(Chat.content==chat_text).first()
	print(x)
	socket.emit("show", {"chattext": chat_text, "time": m_time})
	
