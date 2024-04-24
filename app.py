from flask import Flask, render_template, request, redirect, session
from pymongo import MongoClient

app = Flask(__name__)
app.secret_key = "your_secret_key"

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['user_db']
collection = db['users']

# Default admin username and password
default_username = 'admin'
default_password = 'admin'

# Check if admin user exists, if not, create it
if collection.find_one({'username': default_username}) is None:
    collection.insert_one({'username': default_username, 'password': default_password})

# Check if 'naveen' user exists, if not, create it
if collection.find_one({'username': 'naveen'}) is None:
    collection.insert_one({'username': 'naveen', 'password': 'naveen'})

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = collection.find_one({'username': username})

        if user:
            if user['password'] == password:
                if username == password == 'naveen':
                    return render_template('index1.html', message="Username and password are equal. Go to the next page.")
                elif username == 'naveen':
                    return render_template('login.html', message="Username is correct. Enter the valid password.")
                elif password == 'naveen':
                    return render_template('login.html', message="Password is correct. Enter the valid username.")
                else:
                    session['username'] = username
                    return redirect('/index1')
            else:
                return render_template('login.html', message="Invalid password. Enter the valid password.")
        else:
            return render_template('login.html', message="Invalid username. Enter the valid username.")

    return render_template('login.html')

@app.route('/index1')
def index1():
    if 'username' in session:
        return render_template('index1.html')
    return redirect('/')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
