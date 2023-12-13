from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
from pymongo import MongoClient
from bson.objectid import ObjectId
from bson.json_util import dumps
from datetime import datetime
from dotenv import load_dotenv
import os
import pytz

load_dotenv()
app = Flask(__name__)
CORS(app)

# Set the timezone to East Africa Time
my_timezone = pytz.timezone('Africa/Nairobi')

# Set the timezone for the app

app.config['TIMEZONE'] = my_timezone


# Replace the following connection string with your MongoDB Atlas connection string imported from the .env file
mongo_uri = os.environ.get('DB_URI')
client = MongoClient(mongo_uri)

# 'test_db' name of your database
db = client.test_db
devices_collection = db.devices
readings_collection = db.readings
notifications_collection = db.notifications

# Define the base route for all API endpoints
api_base_url = '/airsentry/api/v1'

@app.route('/')
def api_info():
    # Render an HTML template describing the Indoor Air Quality Monitoring API and project
    return render_template('api_info.html')

# Device CRUD operations
@app.route(f'{api_base_url}/devices', methods=['GET', 'POST'])
def manage_devices():
    if request.method == 'GET':
        devices = list(devices_collection.find())
        return dumps(devices)
    elif request.method == 'POST':
        device_data = request.json
        device_id = devices_collection.insert_one(device_data).inserted_id
        return jsonify({"device_id": str(device_id)})

@app.route(f'{api_base_url}/devices/<device_id>', methods=['GET', 'PUT', 'DELETE'])
def manage_device(device_id):
    if request.method == 'GET':
        device = devices_collection.find_one({"_id": ObjectId(device_id)})
        return dumps(device)
    elif request.method == 'PUT':
        updated_data = request.json
        devices_collection.update_one({"_id": ObjectId(device_id)}, {"$set": updated_data})
        return jsonify({"message": "Device updated successfully"})
    elif request.method == 'DELETE':
        devices_collection.delete_one({"_id": ObjectId(device_id)})
        return jsonify({"message": "Device deleted successfully"})

# Reading CRUD operations
@app.route(f'{api_base_url}/readings', methods=['GET', 'POST'])
def manage_readings():
    if request.method == 'GET':
        readings = list(readings_collection.find())
        return dumps(readings)
    elif request.method == 'POST':
        reading_data = request.json

        if 'timestamp' not in reading_data:
            reading_data['timestamp'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        else:
            reading_data['timestamp'] = datetime.strptime(reading_data['timestamp'], "%Y-%m-%d %H:%M:%S")

        reading_id = readings_collection.insert_one(reading_data).inserted_id

        # check if the reading is above the threshold and create a notification if it is 
        if reading_data['air'] > 100:
            notification_data = {
                "condition": "air",
                "device_id": reading_data['device_id'],
                "timestamp": reading_data['timestamp'],
                "message": "Air quality is above threshold"
            }
            notifications_collection.insert_one(notification_data)

        if reading_data['temperature'] > 30:
            notification_data = {
                "condition": "temperature",
                "device_id": reading_data['device_id'],
                "timestamp": reading_data['timestamp'],
                "message": "Temperature is above threshold"
            }
            notifications_collection.insert_one(notification_data)

        if reading_data['humidity'] > 70:
            notification_data = {
                "condition": "humidity",
                "device_id": reading_data['device_id'],
                "timestamp": reading_data['timestamp'],
                "message": "Humidity is above threshold"
            }
            notifications_collection.insert_one(notification_data)

        if reading_data['co'] > 100:
            notification_data = {
                "condition": "co",
                "device_id": reading_data['device_id'],
                "timestamp": reading_data['timestamp'],
                "message": "CO is above threshold"
            }
            notifications_collection.insert_one(notification_data)

        return jsonify({"reading_id": str(reading_id)})
    
# function to get the most recent reading for a device
@app.route(f'{api_base_url}/readings/<device_id>', methods=['GET'])
def get_latest_reading(device_id):
    if request.method == 'GET':
        reading = readings_collection.find_one({"device_id": device_id}, sort=[("timestamp", -1)])
        return dumps(reading)

# Notification CRUD operations
@app.route(f'{api_base_url}/notifications', methods=['GET', 'POST'])
def manage_notifications():
    if request.method == 'GET':
        notifications = list(notifications_collection.find())
        return dumps(notifications)
    elif request.method == 'POST':
        notification_data = request.json
        notification_id = notifications_collection.insert_one(notification_data).inserted_id
        return jsonify({"notification_id": str(notification_id)})
    
# function to get the most recent notification for a device, by looking up the most recent reading and getting the notification with the same timestamp
@app.route(f'{api_base_url}/notifications/<device_id>', methods=['GET'])
def get_notifications_today(device_id):
    if request.method == 'GET':
        # Get the current date and time
        current_datetime = datetime.now()

        # Calculate the start of the present day
        start_of_day = current_datetime.replace(hour=0, minute=0, second=0, microsecond=0)

        # Query notifications for the specified device within the present day
        notifications = notifications_collection.find({
            "device_id": device_id,
            "timestamp": {"$gte": start_of_day}
        })

        # Convert the cursor to a list and return as JSON
        return dumps(list(notifications))

    
# Get daily average of air quality, temperature and humidity for the last 7 days and return them as arrays of days and values
@app.route(f'{api_base_url}/readings/averages/<device_id>', methods=['GET'])
def get_daily_averages(device_id):
    if request.method == 'GET':
        readings = list(readings_collection.find({"device_id": device_id}, sort=[("timestamp", -1)]))
        
        # Get the last 7 days of readings
        readings = readings[:7]

        # Get the average of each reading type for each day
        averages = []
        for reading in readings:
            averages.append({
                "day": reading['timestamp'].strftime("%Y-%m-%d"),
                "air": round(reading.get('air', 0), 2),
                "temperature": round(reading.get('temperature', 0), 2),
                "humidity": round(reading.get('humidity', 0), 2),
                "co": round(reading.get('co', 0), 2),
            })

        return dumps(averages)

if __name__ == '__main__':
    app.run(debug=True)
