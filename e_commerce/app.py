from flask import Flask, render_template, request, redirect, session
from pymongo import MongoClient
import bcrypt

app = Flask(__name__)
app.secret_key = "root"

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['ecommerce']
users_collection = db['users']
product_list = ["asuslaptop","realmec55","samsungtv"]



def find_product(product_name):
    from bs4 import BeautifulSoup
    # product="asuslaptop"

    # Read the HTML file
    with open(f'G:\MUKESH\py_project\e_commerce\demo\SwiftBuy_Website_1\\{product_name}.html', 'r') as file:
        html_data = file.read()

    # Create a BeautifulSoup object
    soup = BeautifulSoup(html_data, 'html.parser')

    # Find the feedback entries
    feedback_entries = soup.find_all('div', class_='feedback-entry')

    # Scrape the values for each feedback entry
    feedback_data = []
    for entry in feedback_entries:
        stars_element = entry.find('div', class_='stars')
        username_element = entry.find('div', class_='username')
        comment_element = entry.find('div', class_='comment')

        stars = stars_element.get_text() if stars_element else None
        username = username_element.get_text().replace('Username: ', '') if username_element else None
        comment = comment_element.get_text().replace('Comment: ', '') if comment_element else None

        feedback_data.append({'Stars': stars, 'Username': username, 'Comment': comment})

    # # Print the scraped data
    # for feedback in feedback_data:
    #     print('Stars:', feedback['Stars'])
    #     print('Username:', feedback['Username'])
    #     print('Comment:', feedback['Comment'])
    #     print()
    return feedback_data


@app.route('/',methods=["GET","POST"])
def home():
    if request.method == 'POST':
        search =request.form.get("search")
        if search in product_list:
            feedback=find_product(search)
            return render_template("index.html",feedbacks=feedback)
        

        
        return render_template("index.html")

    print(request.headers)
    # return redirect("/login")
    return render_template("index.html")


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']

        # Check if the username already exists
        if users_collection.find_one({'username': username}):
            return render_template('register.html',message="")

        # Hash the password before storing it
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        # Create a new user document
        user = {
            'username': username,
            'password': hashed_password,
            'email': email,
            'active': False
            }

        # Insert the user document into the collection
        users_collection.insert_one(user)

        session['username'] = username
        return redirect('/dashboard')

    return render_template('register.html',message="")

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Retrieve the user document from the collection
        user = users_collection.find_one({'username': username})

        if user:
            # Check if the entered password matches the stored password
            if bcrypt.checkpw(password.encode('utf-8'), user['password']):
                session['username'] = username
                return redirect('/dashboard')

        return 'Invalid username or password!'

    return render_template('login.html')


@app.route('/dashboard')
def dashboard():
    if request.method == 'POST':
        return {"sucess":200}
    # if 'username' in session:
        # return render_template('dashboard.html', username=session['username'])
    return render_template("dashboard.html")
    # return redirect('/login')



@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect('/login')

if __name__ == '__main__':
    app.run(debug=True)
