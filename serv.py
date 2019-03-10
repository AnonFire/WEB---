from flask import Flask, render_template, request, url_for, redirect
from login import DB, BaseUs, BaseNe

app = Flask(__name__)
db = DB()
conn = db.get_connection()
base = BaseUs(conn)
letters = BaseNe(conn)
base.init_table()
letters.init_table()

cur_name = ''
@app.route('/', methods=['GET', 'POST'])

@app.route('/login', methods=['GET', 'POST'])
def login():
    global cur_name
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        exists = base.exists(request.form['email'], request.form['password'])
        if exists[0]:
            cur_name = request.form['email']
            return redirect(url_for('main'))
        else:
            return redirect(url_for('login'))

@app.route('/registration', methods=['POST', 'GET'])
def registration():
    global cur_name
    if request.method == 'GET':
        return render_template('registration.html')
    elif request.method == 'POST':
        base.insert(request.form['emailreg'], request.form['passwordreg'])
        cur_name = request.form['emailreg']
        return redirect(url_for('main'))

@app.route('/main', methods=['GET', 'POST'])
def main():
    global cur_name
    if request.method == 'GET':
        theme = []
        print(letters.get_all())
        for i in letters.get_all():
            if i[3] == cur_name:
                theme.append(i)
        return render_template('main.html', themes=theme, user=cur_name)
    elif request.method == 'POST':
        cur_name = ''
        return redirect(url_for('login'))

@app.route('/main/<id>', methods=['POST', 'GET'])
def retid(id):
    if request.method == 'GET':
        themes = letters.get(id)
        return render_template('theme.html', id=id, themes=themes)

@app.route('/sent_letter', methods=['GET', 'POST'])
def add_theme():
    if request.method == 'GET':
        return render_template('add_theme.html')
    elif request.method == 'POST':
        letters.insert(request.form['title'], request.form['text'], request.form['name'])
        return redirect(url_for('main'))


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
