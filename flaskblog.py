from datetime import datetime
from flask import Flask, render_template, url_for, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from forms import RegistrationForm, LoginForm
app = Flask(__name__)

app.config['SECRET_KEY'] = '3ec21baf9f0ed5d35f1b3ee214645d1e'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://c21032396:Fab30cf22428dab2c8@csmysql.cs.cf.ac.uk:3306/c21032396_blogv1'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    username = db.Column(db.String(20), unique=True, nullable=False)
    image_file = db.Column(db.String(40), nullable=False, default='default.jpg')
    posts = db.relationship('Post', backref='author', lazy=True)
    password = db.Column(db.String(60), nullable=False)


    def __repr__(self):
        return f"User('{self.email}','{self.username}','{self.image_file}')"

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f"Post('{self.title}','{self.date_posted}')"


posts = [
    {
    'author': 'Victor Omoniyi',
    'title': 'Blog Post 1',
    'content': 'First post content',
    'date_posted': 'December 22nd, 2020'
    },
    {
    'author': 'John Doe',
    'title': 'Blog Post 2',
    'content': 'Second post content',
    'date_posted': 'January 1st, 2021'
        },

]

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html', posts=posts)

@app.route('/about')
def about():
    return render_template('about.html', title='About')

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account Created for {form.username.data}. Welcome {form.username.data}!', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@blog.com' and form.password.data == 'password': #Test user data. Remove later.
            flash('You have been logged in!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger') #Test user data. Remove later.
    return render_template('login.html', title='Login', form=form)


if __name__ == '__main__':
    app.run(debug=True)
