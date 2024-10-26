from flask import Flask, request, redirect, render_template
import random
import string
import csv
import os

app = Flask(__name__)

# File to store the URL mappings
CSV_FILE = 'url_mapping.csv'

def load_url_mapping():
    """Load URL mappings from a CSV file."""
    if not os.path.exists(CSV_FILE):
        return {}
    with open(CSV_FILE, mode='r') as file:
        reader = csv.reader(file)
        return {rows[0]: rows[1] for rows in reader}

def save_url_mapping(short_code, original_url):
    """Save a new URL mapping to the CSV file."""
    with open(CSV_FILE, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([short_code, original_url])

# Load existing URL mappings
url_mapping = load_url_mapping()

def generate_short_code(length=6):
    """Generate a random short code."""
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        original_url = request.form['url']
        short_code = generate_short_code()
        url_mapping[short_code] = original_url
        save_url_mapping(short_code, original_url)  # Save to CSV
        return f'Shortened URL: <a href="/{short_code}">/{short_code}</a>'
    return render_template('home.html')

@app.route('/<short_code>')
def redirect_to_url(short_code):
    original_url = url_mapping.get(short_code)
    if original_url:
        return redirect(original_url)
    return 'URL not found', 404

@app.route('/urls')
def list_urls():
    """Display all shortened URLs and their original versions in a table."""
    return render_template('tables.html', url_mapping=url_mapping)

if __name__ == '__main__':
    app.run(debug=True)