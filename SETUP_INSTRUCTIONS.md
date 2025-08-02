# Pelican Thermostat Integration Setup Instructions

## Overview

This Home Assistant integration allows you to control your Pelican Thermostat system. The integration provides:

- **Climate Control**: Full thermostat control with heating, cooling, and auto modes
- **Sensor Monitoring**: Real-time temperature, humidity, and CO2 level monitoring
- **Setpoint Control**: Adjust heating and cooling setpoints
- **System Mode Control**: Switch between Off, Heat, Cool, and Auto modes

## Installation

### Option 1: HACS Installation (Recommended)

1. Install [HACS](https://hacs.xyz/) if you haven't already
2. In HACS, go to **Integrations** → **Custom Repositories**
3. Add this repository: `https://github.com/yourusername/pelican-ha`
4. Search for "Pelican Thermostat" in the HACS store
5. Click **Download**
6. Restart Home Assistant

### Option 2: Manual Installation

1. Download this repository
2. Copy the `custom_components/pelican_thermostat` folder to your Home Assistant `config/custom_components/` directory
3. Restart Home Assistant

## Configuration

1. Go to **Settings** → **Devices & Services**
2. Click **Add Integration**
3. Search for "Pelican Thermostat"
4. Enter your configuration:
   - **Username**: Your Pelican Thermostat username
   - **Password**: Your Pelican Thermostat password
   - **Base URL**: The API base URL (default: https://demo.officeclimatecontrol.net/api.cgi)
   - **Thermostat Name**: The name of your thermostat (e.g., "Lobby")
   - **Poll Interval**: How often to check for updates (default: 70 seconds, range: 30-300 seconds)

## API Information

The integration uses the Pelican Thermostat API with the following endpoints:

### Get Data
```
GET https://demo.officeclimatecontrol.net/api.cgi?username=YOUR_USERNAME&password=YOUR_PASSWORD&request=get&object=Thermostat&selection=name:THERMOSTAT_NAME;&value=temperature;humidity;co2Level
```

### Set Values
```
GET https://demo.officeclimatecontrol.net/api.cgi?username=YOUR_USERNAME&password=YOUR_PASSWORD&request=set&object=Thermostat&selection=name:THERMOSTAT_NAME;&value=PARAMETER:VALUE
```

### Available Parameters

- `system:Auto` - Set system mode to Auto
- `system:Heat` - Set system mode to Heat
- `system:Cool` - Set system mode to Cool
- `system:Off` - Set system mode to Off
- `heatSetting:65` - Set heating setpoint to 65°F
- `coolSetting:75` - Set cooling setpoint to 75°F

## Entities Created

### Climate Entity
- **climate.pelican_thermostat**: Main thermostat control entity

### Sensor Entities
- **sensor.pelican_thermostat_temperature**: Current temperature
- **sensor.pelican_thermostat_humidity**: Current humidity
- **sensor.pelican_thermostat_co2_level**: Current CO2 level

## Usage Examples

### Climate Control
The main climate entity provides full thermostat control:
- Set HVAC mode (Off, Heat, Cool, Auto)
- Adjust temperature setpoints
- View current temperature and humidity

### Automation Examples

```yaml
# Turn on heat when temperature drops below 65°F
automation:
  - alias: "Turn on heat when cold"
    trigger:
      platform: numeric_state
      entity_id: sensor.pelican_thermostat_temperature
      below: 65
    action:
      - service: climate.set_hvac_mode
        target:
          entity_id: climate.pelican_thermostat
        data:
          hvac_mode: heat

# Turn off system when leaving home
automation:
  - alias: "Turn off thermostat when leaving"
    trigger:
      platform: state
      entity_id: person.your_name
      to: "not_home"
    action:
      - service: climate.set_hvac_mode
        target:
          entity_id: climate.pelican_thermostat
        data:
          hvac_mode: off
```

## Troubleshooting

### Common Issues

1. **Connection Failed**: Check your username, password, and base URL
2. **No Data**: Verify your thermostat name is correct
3. **API Errors**: Check the Home Assistant logs for detailed error messages
4. **Thermostat Offline**: The integration handles offline thermostats gracefully - commands will be queued and sent when the thermostat comes back online
5. **Timeouts**: Some SET operations may timeout when thermostats are offline - this is normal
6. **High Poll Frequency**: If you experience issues, try increasing the poll interval to reduce API load

### Debug Logging

To enable debug logging, add this to your `configuration.yaml`:

```yaml
logger:
  default: info
  logs:
    custom_components.pelican_thermostat: debug
```

### Testing the API

You can test the API manually using the provided test scripts:

```bash
# Test GET API
python3 test_api.py

# Test SET API
python3 test_comprehensive_api.py
```

## Notes

- The integration handles API timeouts gracefully, especially when thermostats are offline
- Some SET operations may timeout but still be successful when the thermostat comes back online
- The integration assumes Fahrenheit temperature units
- XML responses are parsed automatically
- Error handling is comprehensive with detailed logging
- Offline thermostats are handled gracefully - entities remain available for control

## Support

For support, please:
1. Check the Home Assistant logs for error messages
2. Test the API manually using the provided test scripts
3. Open an issue on GitHub with detailed error information 