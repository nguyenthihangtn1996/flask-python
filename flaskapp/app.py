from flask import Flask, render_template, flash, redirect, url_for, request, session, logging
from data import Articles
from flask_mysqldb import MySQL
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt

app = Flask(__name__)


# Config MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '123456'
app.config['MYSQL_DB'] = 'mydb1'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
# init MYSQL
mysql = MySQL(app)


Articles = Articles()

@app.route('/articles')
def articles():
        return render_template('articles.html', articles = Articles)

@app.route('/article/<string:id>/')
def article(id):
        return render_template('article.html', id = id)


@app.route('/about')
def about():
        return render_template('about.html')




@app.route('/')
def index():
        return render_template('home.html')

class RegisterForm(Form):
        name = StringField('Name', [validators.Length(min=10, max=50) ])
        username = StringField('Username', [validators.Length(min=10, max=50) ])
        email = StringField('Email', [validators.Length(min=10, max=50) ])
        password = PasswordField('Password', [
                validators.data_required(),
                validators.EqualTo('confirm', message = "Password not match")
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
                 # Create cursor
                cur = mysql.connection.cursor()

                # Execute query
                cur.execute("INSERT INTO users(name, email, username, password) VALUES(%s, %s, %s, %s)", (name, email, username, password))
                  # Commit to DB
                mysql.connection.commit()

                # Close connection
                cur.close()

                flash('You are now registered and can log in', 'success')

                return redirect(url_for('index'))
        return render_template('register.html', form = form)

if __name__ == "__main__":
    app.secret_key='secret123'
    app.run(debug=True)
