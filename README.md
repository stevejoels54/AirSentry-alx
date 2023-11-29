# AirSentry - Indoor Air Quality Monitoring Project

## Project Overview

This project features an Indoor Air Quality Monitoring system, including an embedded device, a RESTful API backend using Flask, and a React.js web app. The backend is responsible for handling data from devices, such as readings and notifications, and storing it in a MongoDB Atlas database.

## Getting Started

### Prerequisites

- Python 3.x
- MongoDB Atlas Account
- Postman (optional, for testing API endpoints)

### Setup

1. Clone the repository:

   ```bash
   git clone https://{YOUR_PERSONAL_TOKEN}@github.com/{YOUR_USERNAME}/AirSentry-alx-server.git AirSentry-server
   cd AirSentr-server
   ```

2. Create a virtual environment and activate it:

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate  # On Windows, use .venv\Scripts\activate
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the root directory with the following content (sample content in sample_env):

   ```dotenv
   # .env
   DB_URI=mongodb+srv://<username>:<password>@<your-atlas-cluster-address>/database
   ```

   Replace `<username>`, `<password>`, and `<your-atlas-cluster-address>` with your MongoDB Atlas credentials.

### Run the Flask App

Run the Flask app:

```bash
python app.py
```

The app will be accessible at http://127.0.0.1:5000/airsentry/api/v1/.

## API Endpoints

The AirSentry API provides endpoints to manage devices, readings, and notifications.

### Device Endpoints

- GET /airsentry/api/v1/devices: Returns a list of devices.
- POST /airsentry/api/v1/devices: Creates a new device.
- GET /airsentry/api/v1/devices/<device_id>: Returns information about a specific device.
- PUT /airsentry/api/v1/devices/<device_id>: Updates information about a specific device.
- DELETE /airsentry/api/v1/devices/<device_id>: Deletes a specific device.

### Reading Endpoints

- GET /airsentry/api/v1/readings: Returns a list of readings.
- GET /airsentry/api/v1/readings/<device_id>: Returns most recent reading from the device
- POST /airsentry/api/v1/readings: Creates a new reading.

### Notification Endpoints

- GET /airsentry/api/v1/notifications: Returns a list of notifications.
- POST /airsentry/api/v1/notifications: Creates a new notification.

## Contributing

If you'd like to contribute to this project, please follow these guidelines:

1.  Fork the repository.
2.  Create a new branch for your feature: `git checkout -b feature-name`.
3.  Commit your changes: `git commit -m 'Add a new feature'`.
4.  Push to the branch: `git push origin feature-name`.
5.  Submit a pull request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
