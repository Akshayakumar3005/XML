from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
import xml.etree.ElementTree as ET
import csv

class CountryCodeHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urlparse(self.path)
        query_params = parse_qs(parsed_path.query)

        if parsed_path.path == '/get_country_code':
            country_name = query_params.get('country_name', [None])[0]

            if country_name is None:
                self.send_response(400)
                self.send_header('Content-type', 'text/xml')
                self.end_headers()
                self.wfile.write(bytes('<error>Please provide a country name.</error>', 'utf-8'))
                return

            country_data = get_country_data(country_name)
            if country_data:
                self.send_response(200)
                self.send_header('Content-type', 'text/xml')
                self.end_headers()
                response = ET.Element('response')
                ET.SubElement(response, 'country_name').text = country_name
                ET.SubElement(response, 'currency_name').text = country_data[0]
                ET.SubElement(response, 'currency_code').text = country_data[1]
                self.wfile.write(ET.tostring(response))
            else:
                self.send_response(404)
                self.send_header('Content-type', 'text/xml')
                self.end_headers()
                self.wfile.write(bytes('<error>Country not found.</error>', 'utf-8'))
        else:
            self.send_response(404)
            self.send_header('Content-type', 'text/xml')
            self.end_headers()
            self.wfile.write(bytes('<error>Resource not found.</error>', 'utf-8'))

def get_country_data(country_name):
    with open('currency.csv', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row['Country name'] == country_name:
                return row['Currency name'], row['Currency ISO code']
    return None

def run(server_class=HTTPServer, handler_class=CountryCodeHandler, port=8080):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Starting server on port {port}...')
    httpd.serve_forever()

if __name__ == "__main__":
    run()
