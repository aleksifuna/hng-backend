#!/usr/bin/env python3
"""
This module contains an instance and configuration of a flask app
"""
from flask import Flask, jsonify, request
import requests
import os
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)
secret_key = os.getenv("KEY")


@app.route('/api/hello', methods=['GET'])
def hello_name():
    name = request.args.get('visitor_name').strip('"')
    client_ip = request.remote_addr
    response = requests.get(f"http://ip-api.com/json/{client_ip}")
    location = response.json().get("city")
    base_weather_url = "http://api.weatherapi.com/v1/current.json?key="
    weather_url = f"{base_weather_url}{secret_key}&q={location}"
    weather = requests.get(weather_url).json()
    temp = weather.get("current").get("temp_c")
    response_object = {}
    response_object["client_ip"] = client_ip
    response_object["location"] = location
    greetings_1 = f"Hello, {name}!, the temperature "
    greetings_2 = f"is {temp} degrees Celcius in {location}"
    response_object["greeting"] = f"{greetings_1}{greetings_2}"
    return jsonify(response_object)


if __name__ == "__main__":
    app.run(debug=True)
