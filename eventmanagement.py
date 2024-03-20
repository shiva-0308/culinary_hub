from flask import Flask, render_template, request, jsonify
from geopy.geocoders import Nominatim

app = Flask(__name__)

def get_road_number(address):
    # Parse address to retrieve road number
    road_number = None
    parts = address.split(',')
    if len(parts) > 1:
        road_number = parts[0].strip()
    return road_number

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/reverse_geocode', methods=['POST'])
def reverse_geocode():
    data = request.get_json()
    latitude = data['latitude']
    longitude = data['longitude']
    geolocator = Nominatim(user_agent="geocoder")
    location = geolocator.reverse((latitude, longitude), exactly_one=True)
    if location:
        address = location.address
        road_number = get_road_number(address)
        return jsonify({'address': address, 'road_number': road_number})
    else:
        return jsonify({'error': 'Address not found.'}), 404

@app.route('/update_address', methods=['POST'])
def update_address():
    address = request.form['address']
    # Process the updated address here
    return "Address updated successfully: " + address

if __name__ == '__main__':
    app.run(debug=True)
