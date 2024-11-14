from flask import Flask, render_template, redirect,url_for, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped
from sqlalchemy.testing.schema import mapped_column
from sqlalchemy import Integer, String
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('secret_key')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///customers.db'

# CREATE DB
class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)
db.init_app(app)

# CREATE USER TABLE
class User(db.Model):
    id: Mapped[int] = mapped_column(Integer,primary_key=True)
    name: Mapped[str] = mapped_column(String(250), nullable=False)
    email: Mapped[str] = mapped_column(String(250), unique=True,nullable=False)
    message: Mapped[str] = mapped_column(String(400),nullable=False)

class Studies(db.Model):
    id: Mapped[int] = mapped_column(Integer,primary_key=True)
    institution_name : Mapped[str] = mapped_column(String(250), nullable=False)
    description : Mapped[str] = mapped_column(String(300), nullable=False)
    place : Mapped[str] = mapped_column(String(250),nullable=False)
    year: Mapped[str] = mapped_column(String(200),nullable=False)
    img_url: Mapped[str] = mapped_column(String(250), nullable=False)


with app.app_context():
    db.create_all()

@app.route("/")
def home_page():
    return render_template('index.html')

@app.route('/about-me')
def about_page():
    result = db.session.execute(db.select(Studies))
    my_studies = result.scalars().all()
    print(my_studies)
    return render_template('about.html',all_studies=my_studies)

@app.route('/send-message',methods=['GET','POST'])
def send_message():
    if request.method == 'POST':
        new_user = User(
            name = request.form['name'],
            email = request.form['email'],
            message = request.form['message']
        )
        db.session.add(new_user)
        db.session.commit()
        return render_template('send.html',user=new_user)


if __name__ == "__main__":
    app.run(debug=True)