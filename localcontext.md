# Pelican HA Integration Development Context

## Project Overview
Home Assistant custom integration for Pelican Wireless Thermostat system.

## Recent Work Completed

### Issue 1: Temperature Setting Not Working (FIXED)
**Problem**: Unable to set temperature from Home Assistant

**Root Cause**: The coordinator was making two separate API calls:
1. Basic data (temperature, humidity, etc.)
2. System data (mode, heat/cool setpoints)

The second call was often failing, causing the climate entity to lack current setpoint data needed for temperature control.

**Solution Implemented**: 
- Modified `/Users/matt/repo/pelican-ha/custom_components/pelican_thermostat/coordinator.py`
- Consolidated all data fetching into a single API request (lines 78-97)
- Parse system mode, heat settings, and cool settings directly from main response (lines 116-195)
- Removed redundant `_parse_system_data` method

### Issue 2: Schedule Support (COMPLETE)

**Goal**: Retrieve and display thermostat schedule status in Home Assistant

**API Documentation Findings**:
- Schedule attribute returns: "On", "Off", or a shared schedule name
- Schedule indicates if thermostat is in schedule mode or manual mode
- API endpoint: `value=schedule` in GET request

**Completed Changes**:
1. Added `VALUE_SCHEDULE = "schedule"` constant to `const.py` (line 35)
2. Updated coordinator to fetch schedule in API request (line 87)
3. Added schedule parsing to `_parse_thermostat_data` method (lines 177-182)
4. Added schedule sensor to `sensor.py` SENSORS list (lines 42-47)

**Status**: Schedule sensor implementation complete and ready for testing

### Issue 3: Configurable Polling Interval (COMPLETE)

**Goal**: Allow users to adjust the polling interval via Home Assistant UI

**Implementation**:
1. Added `CONF_POLL_INTERVAL` and `DEFAULT_POLL_INTERVAL` constants to `const.py`
2. Initial setup form includes polling interval field (30-300 seconds range)
3. Options flow added to `config_flow.py` for reconfiguring after setup
4. Coordinator checks options first, then data, then default value
5. Added `update_poll_interval()` method to coordinator
6. Added options update listener in `__init__.py` to reload on changes

**Usage**:
- During initial setup: Choose polling interval (default: 70 seconds)
- After setup: Go to integration settings → Configure to change interval
- Valid range: 30-300 seconds (0.5 to 5 minutes)
- Integration automatically reloads when interval is changed

**Status**: Complete and ready for testing

## API Information

### Base URL
- Demo: `https://demo.officeclimatecontrol.net/api.cgi`
- Demo credentials: `pelicandemosite@gmail.com` / `pelican`
- Test thermostat: "Lobby"

### API Structure
```
?username=<email>
&password=<password>
&request=get|set
&object=Thermostat|ThermostatSchedule|SharedSchedule|ThermostatHistory
&selection=name:ThermostatName;
&value=attribute1;attribute2;...
```

### Key Thermostat Attributes
- `temperature` - Current measured temperature
- `humidity` - Current humidity (% RH)
- `co2Level` - Current CO2 level
- `runStatus` - Current heating/cooling status (Off, Cool-Stage1, Cool-Stage2, Heat-Stage1, Heat-Stage2, Fan, Fan2)
- `system` - System mode (Off, Auto, Heat, Cool)
- `heatSetting` - Heat setpoint
- `coolSetting` - Cool setpoint
- `schedule` - Schedule status (On, Off, or shared schedule name)

## File Structure
```
custom_components/pelican_thermostat/
├── __init__.py
├── const.py              # Constants and API parameters
├── coordinator.py        # Data coordinator (handles API communication)
├── climate.py            # Climate entity (thermostat control)
├── sensor.py             # Sensor entities (temperature, humidity, CO2, run status)
├── config_flow.py        # Configuration UI
└── manifest.json
```

## Next Steps
1. ✅ Add schedule fetching to coordinator
2. ✅ Parse schedule status in coordinator
3. ✅ Create sensor entity for schedule status
4. 🔄 Test schedule functionality (NEXT)
5. ⏳ Consider adding ability to toggle schedule on/off via switch entity
   - API supports setting schedule: "On", "Off", or shared schedule name
   - Could use switch entity to toggle between On/Off
   - Or select entity to choose between On/Off/shared schedule names

## Testing Commands
```bash
# Test schedule API endpoint
curl -Ls "https://demo.officeclimatecontrol.net/api.cgi?username=pelicandemosite@gmail.com&password=pelican&request=get&object=Thermostat&selection=name:Lobby;&value=schedule"

# Test full data fetch
curl -Ls "https://demo.officeclimatecontrol.net/api.cgi?username=pelicandemosite@gmail.com&password=pelican&request=get&object=Thermostat&selection=name:Lobby;&value=temperature;humidity;co2Level;runStatus;schedule;system;heatSetting;coolSetting"
```

## Notes
- The integration uses XML responses from the API
- All API communication happens over SSL
- The coordinator polls every 70 seconds by default
- Temperature setting fix ensures setpoints are always available to climate entity
- API specification document available at `Pelican_API_Specifications.pdf`
- Schedule can be set via API (supports "On", "Off", or shared schedule name)
- User can define custom attributes via API for any thermostat
