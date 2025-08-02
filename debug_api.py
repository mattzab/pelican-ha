#!/usr/bin/env python3
"""Debug script for testing Pelican Thermostat API."""

import requests
import sys

def test_api():
    """Test the Pelican Thermostat API."""
    base_url = "https://demo.officeclimatecontrol.net/api.cgi"
    
    # Test GET request
    params = {
        "username": "pelicandemosite@gmail.com",
        "password": "pelican",
        "request": "get",
        "object": "Thermostat",
        "selection": "name:Lobby;",
        "value": "temperature;humidity;co2Level"
    }
    
    try:
        print("Testing Pelican Thermostat API...")
        response = requests.get(base_url, params=params, timeout=10)
        response.raise_for_status()
        print(f"GET Response: {response.text}")
        
        # Test SET request
        set_params = params.copy()
        set_params["request"] = "set"
        set_params["value"] = "system:Off"
        
        print("\nTesting SET request...")
        set_response = requests.get(base_url, params=set_params, timeout=15)
        set_response.raise_for_status()
        print(f"SET Response: {set_response.text}")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_api() 