from flask import Flask, jsonify, request, render_template
from pymongo import MongoClient
from bson.objectid import ObjectId
from bson.json_util import dumps
from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv()
app = Flask(__name__)


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

if __name__ == '__main__':
    app.run(debug=True)
