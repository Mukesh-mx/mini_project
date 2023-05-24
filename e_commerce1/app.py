from flask import Flask, render_template, request, redirect, session
from pymongo import MongoClient
import bcrypt
from bs4 import BeautifulSoup
import re
from textblob import TextBlob

app = Flask(__name__)
app.secret_key = "root"

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['ecommerce']
users_collection = db['users']
product_list = ["asuslaptop","realmec55","samsungtv"]



def find_product(product_name):
    # Read the HTML files
    with open(f'G:/MUKESH/py_project/e_commerce/demo/SwiftBuy_Website_1/{product_name}.html', 'r') as file1:
        html_data1 = file1.read()
    with open(f'G:/MUKESH/py_project/e_commerce/demo/SwiftBuy_Website_2/{product_name}.html', 'r') as file2:
        html_data2 = file2.read()

    # Create BeautifulSoup objects
    soup1 = BeautifulSoup(html_data1, 'html.parser')
    soup2 = BeautifulSoup(html_data2, 'html.parser')

    # Find the feedback entries and price elements
    feedback_entries1 = soup1.find_all('div', class_='feedback-entry')
    price_entry1 = soup1.find('b')

    feedback_entries2 = soup2.find_all('div', class_='feedback-entry')
    price_entry2 = soup2.find('b')

    # Extract the prices
    price1 = price_entry1.text.strip()
    price2 = price_entry2.text.strip()

    # Remove non-digit characters from the prices
    price_1 = re.sub(r'\D', '', price1)
    price_2 = re.sub(r'\D', '', price2)

    price_min = min(price_1,price_2)

    # Scrape the values for each feedback entry
    feedback_data = []
    sentiment_results = []
    total_polarity1=0
    total_polarity2=0
    for entry in feedback_entries1:
        stars_element = entry.find('div', class_='stars')
        username_element = entry.find('div', class_='username')
        comment_element = entry.find('div', class_='comment')

        stars = stars_element.get_text() if stars_element else None
        username = username_element.get_text().replace('Username: ', '') if username_element else None
        comment = comment_element.get_text().replace('Comment: ', '') if comment_element else None

        feedback_data.append({'Stars': stars, 'Username': username, 'Comment': comment, 'Price': price_1})

        if comment:
        # Perform sentiment analysis using TextBlob
            blob = TextBlob(comment)
            polarity = blob.sentiment.polarity
            sentiment = 'Positive' if polarity > 0 else 'Negative' if polarity < 0 else 'Neutral'
            
            sentiment_results.append({'Comment': comment, 'Sentiment': sentiment, 'Polarity': polarity})
            total_polarity1 += polarity

    for entry in feedback_entries2:
        stars_element = entry.find('div', class_='stars')
        username_element = entry.find('div', class_='username')
        comment_element = entry.find('div', class_='comment')

        stars = stars_element.get_text() if stars_element else None
        username = username_element.get_text().replace('Username: ', '') if username_element else None
        comment = comment_element.get_text().replace('Comment: ', '') if comment_element else None

        if comment:
        # Perform sentiment analysis using TextBlob
            blob = TextBlob(comment)
            polarity = blob.sentiment.polarity
            sentiment = 'Positive' if polarity > 0 else 'Negative' if polarity < 0 else 'Neutral'
            
            sentiment_results.append({'Comment': comment, 'Sentiment': sentiment, 'Polarity': polarity})
            total_polarity2 += polarity


        feedback_data.append({'Stars': stars, 'Username': username, 'Comment': comment})

    return feedback_data, price_min, sentiment_results, total_polarity1, total_polarity2


@app.route('/',methods=["GET","POST"])
def home():
    if request.method == 'POST':
        search =request.form.get("search")
        if search in product_list:
            feedback, price, sentiment, total_polarity1, total_polarity2 = find_product(search)
            render_template("index.html", feedbacks=feedback, price=price, sentiment=sentiment,
                                   total_polarity1=total_polarity1, total_polarity2=total_polarity2)
        

        
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
