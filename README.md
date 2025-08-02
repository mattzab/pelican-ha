# Pelican Thermostat Integration for Home Assistant

This is a custom integration for Home Assistant that allows you to control your Pelican Thermostat system.

## Features

- **Climate Control**: Full thermostat control with heating, cooling, and auto modes
- **Temperature Sensors**: Real-time temperature, humidity, and CO2 level monitoring
- **Setpoint Control**: Adjust heating and cooling setpoints
- **System Mode Control**: Switch between Off, Heat, Cool, and Auto modes

## Installation

### Option 1: HACS (Recommended)

1. Install [HACS](https://hacs.xyz/) if you haven't already
2. Add this repository as a custom repository in HACS
3. Search for "Pelican Thermostat" in the HACS store
4. Click "Download"
5. Restart Home Assistant

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

This integration uses the Pelican Thermostat API with the following endpoints:

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

## Usage

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
5. **High Poll Frequency**: If you experience issues, try increasing the poll interval to reduce API load

### Debug Logging

To enable debug logging, add this to your `configuration.yaml`:

```yaml
logger:
  default: info
  logs:
    custom_components.pelican_thermostat: debug
```

## Development

### Project Structure
```
custom_components/pelican_thermostat/
├── __init__.py          # Main integration file
├── const.py             # Constants and configuration
├── coordinator.py        # Data coordinator
├── config_flow.py       # Configuration flow
├── climate.py           # Climate entity
├── sensor.py            # Sensor entities
├── manifest.json        # Integration manifest
└── translations/        # Translation files
    └── en.json
```

### Contributing

1. Fork this repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support, please open an issue on GitHub or contact the maintainer.

## Changelog

### Version 1.0.0
- Initial release
- Basic thermostat control
- Temperature, humidity, and CO2 sensors
- Configuration flow
- HACS support
- Offline thermostat handling
- Graceful timeout management 