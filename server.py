from collections import namedtuple

from flask import Flask, url_for, render_template, redirect, request
from login import DB, BaseUs, BaseNe

app = Flask(__name__)

Themes = namedtuple('Themes', 'title text')

db = DB()
conn = db.get_connection()
base = BaseUs(conn)
basen = BaseNe(conn)
base.init_table()
basen.init_table()

@app.route('/', methods=['GET', 'POST'])
def start():
    return render_template('start.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        exists = base.exists(request.form['email'], request.form['password'])
    if (exists[0]):
        return redirect(url_for('main'))
    else:
        return redirect(url_for('loginwr'))

@app.route('/loginwr', methods=['GET', 'POST'])
def loginwr():
    if request.method == 'GET':
        return render_template('wronglogin.html')
    elif request.method == 'POST':
        exists = base.exists(request.form['email'], request.form['password'])
    if (exists[0]):
        return redirect(url_for('main'))
    else:
        return redirect(url_for('loingwr'))


@app.route('/registration', methods=['GET', 'POST'])
def registration():
    if request.method == 'GET':
        return render_template('registration.html')
    elif request.method == 'POST':
        base.insert(request.form['emailreg'], request.form['passwordreg'])
        return redirect(url_for('main'))

@app.route('/main', methods=['GET', 'POST'])
def main():
    if request.method == 'GET':
        theme = reversed(basen.get_all())
        print(theme)
        return render_template('main.html', themes=theme)

    elif request.method == 'POST':
        basen.insert(request.form['title'], request.form['text'])
        return redirect(url_for('main'))

@app.route('/main/<n>', methods=['POST', 'GET'])
def retid(n):
    print(0)
    n = int(n)
    themes = basen.get(n)
    print(1)
    return render_template('theme.html', id=n, themes=themes)

@app.errorhandler(404)
def not_found(error):
    return '''<p><img src="https://pbs.twimg.com/media/DsB8QUtWsAAWFEy.jpg"
  width="1580" height="710" alt="lorem"></p>'''

if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
