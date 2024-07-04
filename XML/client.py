from flask import Flask, render_template, request, jsonify
import requests
import csv
import xml.etree.ElementTree as ET

app = Flask(__name__)

@app.route('/')
def index():
    # Read country names from the CSV file
    country_names = []
    with open('currency.csv', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            country_names.append(row['Country name'])
    return render_template('index.html', country_names=country_names)

@app.route('/get_country_code')
def get_country_code():
    country_name = request.args.get('country_name', '')

    # Fetch country data from the server
    response = requests.get(f'http://localhost:8080/get_country_code?country_name={country_name.replace(" ", "%20")}')
    root = ET.fromstring(response.text)
    currency_name = root.find('currency_name').text
    currency_code = root.find('currency_code').text

    return jsonify({"country_name": country_name, "currency_name": currency_name, "currency_code": currency_code})

if __name__ == "__main__":
    app.run(debug=True)
