#!/usr/bin/env python3
"""Test script to verify the integration can be imported correctly."""

import sys
import os

def test_imports():
    """Test if all the integration modules can be imported."""
    
    # Add the custom_components directory to the path
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'custom_components'))
    
    try:
        print("Testing integration imports...")
        
        # Test importing the main module
        print("1. Testing __init__.py...")
        import pelican_thermostat
        print("   ✓ __init__.py imported successfully")
        
        # Test importing constants
        print("2. Testing const.py...")
        from pelican_thermostat.const import DOMAIN, DEFAULT_BASE_URL
        print(f"   ✓ const.py imported successfully (DOMAIN: {DOMAIN})")
        
        # Test importing coordinator
        print("3. Testing coordinator.py...")
        from pelican_thermostat.coordinator import PelicanThermostatCoordinator
        print("   ✓ coordinator.py imported successfully")
        
        # Test importing config flow
        print("4. Testing config_flow.py...")
        from pelican_thermostat.config_flow import PelicanThermostatConfigFlow
        print("   ✓ config_flow.py imported successfully")
        
        # Test importing climate
        print("5. Testing climate.py...")
        from pelican_thermostat.climate import PelicanThermostatEntity
        print("   ✓ climate.py imported successfully")
        
        # Test importing sensor
        print("6. Testing sensor.py...")
        from pelican_thermostat.sensor import PelicanThermostatSensor
        print("   ✓ sensor.py imported successfully")
        
        print("\n🎉 All imports successful! The integration should work properly.")
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

if __name__ == "__main__":
    success = test_imports()
    sys.exit(0 if success else 1) 