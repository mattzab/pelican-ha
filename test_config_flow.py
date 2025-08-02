#!/usr/bin/env python3
"""Test script to verify the config flow can be imported correctly."""

import sys
import os

def test_config_flow():
    """Test if the config flow can be imported."""
    
    # Add the custom_components directory to the path
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'custom_components'))
    
    try:
        print("Testing config flow import...")
        
        # Test importing the config flow
        from pelican_thermostat.config_flow import PelicanThermostatConfigFlow
        print("   ✓ Config flow imported successfully")
        
        # Test creating an instance
        flow = PelicanThermostatConfigFlow()
        print("   ✓ Config flow instance created successfully")
        
        # Test domain property
        domain = flow.domain
        print(f"   ✓ Domain property works: {domain}")
        
        print("\n🎉 Config flow test successful!")
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

if __name__ == "__main__":
    success = test_config_flow()
    sys.exit(0 if success else 1) 