
from bs4 import BeautifulSoup
product_list = ["asuslaptop","realmec55","samsungtv"]
product="asuslaptop"

# Read the HTML file
with open(f'G:\MUKESH\py_project\e_commerce\demo\SwiftBuy_Website_1\\{product}.html', 'r') as file:
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

# Print the scraped data
for feedback in feedback_data:
    print('Stars:', feedback['Stars'])
    print('Username:', feedback['Username'])
    print('Comment:', feedback['Comment'])
    print()
