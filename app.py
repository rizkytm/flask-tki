from flask import Flask, request, render_template, flash, redirect, url_for, session, logging
from data import Articles
from flaskext.mysql import MySQL
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt
from pymysql.cursors import DictCursor

app = Flask(__name__)

app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PORT'] = 3306
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'flask'

mysql = MySQL(cursorclass=DictCursor)
mysql.init_app(app)

Articles = Articles()

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/about')
def about():
	return render_template('about.html')

@app.route('/articles')
def articles():
	return render_template('articles.html', articles = Articles)

@app.route('/article/<string:id>/')
def article(id):
	return render_template('article.html', id = id)

class RegisterForm(Form):
	name = StringField('Name', [validators.Length(min=1, max=50)])
	username = StringField('Username', [validators.Length(min=4, max=25)])
	email = StringField('Email', [validators.Length(min=6, max=50)])
	password = PasswordField('Password', [
		validators.DataRequired(),
		validators.EqualTo('confirm', message='Passwords do not match')
	])
	confirm = PasswordField('Confirm Password')

@app.route('/register', methods=['GET', 'POST'])
def register():
	form = RegisterForm(request.form)
	if request.method == 'POST' and form.validate():
		name = form.name.data
		email = form.email.data
		username = form.username.data
		password = sha256_crypt.encrypt(str(form.password.data))

		conn = mysql.connect()
		cursor = conn.cursor()

		cursor.execute("INSERT INTO users(name, email, username, password) VALUES(%s, %s, %s, %s)", (name, email, username, password))

		conn.commit()

		cursor.close()

		flash('You are now registered and can log in', 'success')

		return redirect(url_for('index'))
	return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
	if request.method == 'POST':
		username = request.form['username']
		password_candidate = request.form['password']

		conn = mysql.connect()
		cursor = conn.cursor()

		result = cursor.execute("SELECT * FROM users WHERE username = %s", [username])

		if result > 0:
			data = cursor.fetchone()
			password = data['password']

			if sha256_crypt.verify(password_candidate, password):
				session['logged_in'] = True
				session['username'] = username

				flash('You are now logged in', 'success')
				return redirect(url_for('dashboard'))
			else:
				error = 'Invalid login'
				return render_template('login.html', error=error)
			cursor.close()
		else:
			error = 'Username not found'
			return render_template('login.html', error=error)

	return render_template('login.html')

@app.route('/dashboard')
def dashboard():
	return render_template('dashboard.html')

@app.route('/logout')
def logout():
	session.clear()
	flash('You are now logged out', 'success')
	return redirect(url_for('login'))		

if __name__ == '__main__':
	app.secret_key='secret123'
	app.run(debug=True)