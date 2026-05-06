# Pelican HA Integration Development Context

## Project Overview
Home Assistant custom integration for Pelican Wireless Thermostat system.

## Recent Work Completed

### Feature Branch: Comprehensive Enhancements (IN PROGRESS)
**Branch**: `feature/comprehensive-enhancements`

**Goal**: Implement complete integration with all available API features

**Completed Enhancements**:

#### 1. Enhanced Climate Entity (`climate.py`)
- ✅ Added fan mode support (Auto/On)
- ✅ Added preset modes (Occupied/Vacant status)
- ✅ Added HVAC action display (Heating/Cooling/Fan/Idle)
- Maps Pelican fan modes to Home Assistant fan modes
- Displays current occupied/vacant status as preset mode

#### 2. New Switch Platform (`switch.py`)
- ✅ **Schedule Switch**: Toggle schedule on/off
- ✅ **Front Keypad Switch**: Enable/disable (lock) front keypad
- Provides easy control over schedule and keypad settings

#### 3. Expanded Sensor Platform (`sensor.py`)
Added 25+ new sensors for comprehensive monitoring:
- **Status Sensors**: status, set_by, front_keypad, aux_status, status_display
- **System Configuration**: heat_stages, cool_stages, fan_stages, system_type, temperature_format, cycle_rate, anticipation_degrees, calibration_offset
- **Device Info**: serial_no, gateway, version, install_date
- **Humidity Control**: humidity_control mode
- **Fan Mode**: Current fan mode (Auto/On)

#### 4. New Number Platform (`number.py`)
Added adjustable setpoint controls:
- ✅ **Humidity Controls**: humidify_setting, dehumidify_setting
- ✅ **CO2 Control**: co2_setting
- ✅ **Temperature Limits**: min_heat_setting, max_heat_setting, min_cool_setting, max_cool_setting
- All with appropriate ranges and validation

#### 5. Enhanced Coordinator (`coordinator.py`)
- ✅ Fetches ~50 attributes in single optimized API call
- ✅ Added 9 new setter methods for fan, schedule, keypad, humidity, CO2, and temp limits
- ✅ Improved parsing with helper functions (parse_float, parse_int, parse_string)
- ✅ Handles all new API attributes

#### 6. Expanded Constants (`const.py`)
- ✅ Added 40+ new API value constants
- ✅ Fan mode constants (FAN_AUTO, FAN_ON)
- ✅ Status constants (STATUS_OCCUPIED, STATUS_VACANT, etc.)
- ✅ Configuration constants for all system settings
- ✅ Device info constants

**Next Steps**:
1. Test all new entities in Home Assistant
2. Verify API calls for new setter methods
3. Test fan mode control
4. Test switch entities (schedule, keypad)
5. Test number entities (humidity, CO2, temp limits)
6. Create pull request

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

### Key Thermostat Attributes (Expanded)

#### Measurements
- `temperature` - Current measured temperature
- `humidity` - Current humidity (% RH)
- `co2Level` - Current CO2 level

#### Status
- `runStatus` - Current heating/cooling status (Off, Cool-Stage1, Cool-Stage2, Heat-Stage1, Heat-Stage2, Fan, Fan2)
- `status` - Occupied/Vacant status
- `setBy` - Control source (Station/Remote/Schedule)
- `frontKeypad` - Keypad enabled status (On/Off)
- `auxStatus` - Auxiliary status (On/Off)
- `statusDisplay` - Human readable status text

#### Control Settings
- `system` - System mode (Off, Auto, Heat, Cool)
- `heatSetting` - Heat setpoint
- `coolSetting` - Cool setpoint
- `schedule` - Schedule status (On, Off, or shared schedule name)
- `fan` - Fan mode (Auto/On)

#### Humidity & CO2
- `humidifySetting` - Humidification setpoint
- `dehumidifySetting` - Dehumidification setpoint
- `humidityControl` - Humidity control mode
- `co2Setting` - CO2 setpoint

#### System Configuration
- `heatStages` - Number of heat stages
- `coolStages` - Number of cool stages
- `fanStages` - Number of fan stages
- `systemType` - System type (Conventional/HeatPump)
- `temperatureFormat` - Temperature unit (Fahrenheit/Celsius)
- `cycleRate` - Cycle rate setting
- `anticipationDegrees` - Anticipation offset
- `calibrationOffset` - Temperature calibration offset

#### Temperature Limits
- `minHeatSetting` - Minimum heat setpoint allowed
- `maxHeatSetting` - Maximum heat setpoint allowed
- `minCoolSetting` - Minimum cool setpoint allowed
- `maxCoolSetting` - Maximum cool setpoint allowed
- `minSafeTemp` - Minimum safe temperature
- `maxSafeTemp` - Maximum safe temperature

#### Device Information
- `serialNo` - Device serial number
- `gateway` - Gateway identifier
- `version` - Firmware version
- `installDate` - Installation date

## File Structure
```
custom_components/pelican_thermostat/
├── __init__.py           # Main integration setup, platform registration
├── const.py              # Constants and API parameters (40+ API values)
├── coordinator.py        # Data coordinator with 50+ attributes and 9 setters
├── climate.py            # Climate entity (thermostat with fan & preset modes)
├── sensor.py             # 25+ sensor entities (status, config, device info)
├── switch.py             # Switch entities (schedule, keypad control)
├── number.py             # Number entities (humidity, CO2, temp limits)
├── config_flow.py        # Configuration UI (with polling interval)
└── manifest.json         # Integration manifest
```

## Next Steps
1. ✅ Temperature setting fix (consolidated API calls)
2. ✅ Schedule sensor implementation
3. ✅ Configurable polling interval
4. ✅ Comprehensive API feature implementation
5. 🔄 **Test comprehensive enhancements** (CURRENT)
   - Test fan mode control in climate entity
   - Test preset modes (occupied/vacant)
   - Test HVAC action display
   - Test schedule switch
   - Test keypad switch
   - Test new sensors (status, config, device info)
   - Test number entities (humidity, CO2, temp limits)
6. ⏳ Create documentation for all new features
7. ⏳ Consider adding select entities for:
   - Shared schedule selection
   - Humidity control mode selection

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
- The coordinator polls at user-configurable interval (default 70 seconds, range 30-300s)
- Temperature setting fix ensures setpoints are always available to climate entity
- API specification document available at `Pelican_API_Specifications.pdf`
- Schedule can be set via API (supports "On", "Off", or shared schedule name)
- User can define custom attributes via API for any thermostat
- **Comprehensive Enhancement**: Integration now supports 50+ API attributes
- **4 Platform Types**: Climate, Sensor, Switch, Number
- **25+ Entities**: Full visibility and control over all thermostat features
