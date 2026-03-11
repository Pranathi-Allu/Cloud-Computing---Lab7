from flask import Flask, jsonify, request
from datetime import datetime
import requests

app = Flask(__name__)

def get_location_from_ip():
    try:
        response = requests.get("http://ip-api.com/json/", timeout=5)
        data = response.json()
        
        if data["status"] == "success":
            return {
                "name": "Classroom (Auto-detected)",
                "latitude": data["lat"],
                "longitude": data["lon"],
                "city": data["city"],
                "region": data["regionName"],
                "country": data["country"],
                "isp": data["isp"],
                "source": "IP Geolocation"
            }
    except Exception as e:
        return None

@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "GPS Microservice is running!", "status": "healthy"})

@app.route("/location", methods=["GET"])
def get_location():
    location = get_location_from_ip()
    
    if location:
        return jsonify({
            "status": "success",
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "location": location
        })
    else:
        return jsonify({"status": "error", "message": "Could not fetch location"}), 500

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "healthy"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)