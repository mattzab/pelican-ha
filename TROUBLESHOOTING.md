# Troubleshooting Guide

## Configuration Page Not Appearing

If you cannot access the configuration page when following the setup steps, try these solutions:

### 1. Restart Home Assistant
After installing the integration, restart Home Assistant completely:
- Go to **Settings** → **System** → **Restart**
- Wait for Home Assistant to fully restart

### 2. Check Installation Location
Make sure the integration is installed in the correct location:
- **HACS Installation**: Should be in `config/custom_components/pelican_thermostat/`
- **Manual Installation**: Should be in `config/custom_components/pelican_thermostat/`

### 3. Verify File Structure
Ensure all required files are present:
```
config/custom_components/pelican_thermostat/
├── __init__.py
├── const.py
├── coordinator.py
├── config_flow.py
├── climate.py
├── sensor.py
├── manifest.json
└── translations/
    └── en.json
```

### 4. Check Home Assistant Logs
Look for errors in the Home Assistant logs:
- Go to **Settings** → **System** → **Logs**
- Look for any errors related to `pelican_thermostat`
- Common errors include import issues or missing dependencies

### 5. Manual Integration Search
Try searching manually:
1. Go to **Settings** → **Devices & Services**
2. Click **Add Integration**
3. Search for "Pelican" (not just "Pelican Thermostat")
4. If it doesn't appear, try searching for "pelican"

### 6. Check Dependencies
Ensure the required dependency is installed:
- The integration requires `aiohttp`
- This should be automatically installed, but you can check in **Settings** → **System** → **Add-ons** → **Supervisor** → **System** → **Hardware**

### 7. Clear Browser Cache
Sometimes the UI needs a refresh:
- Clear your browser cache
- Hard refresh the page (Ctrl+F5 or Cmd+Shift+R)

### 8. Check Integration Status
Verify the integration is properly loaded:
1. Go to **Settings** → **Devices & Services**
2. Look for "Pelican Thermostat" in the integrations list
3. If it appears but is not working, try removing and re-adding it

### 9. Debug Mode
Enable debug logging to see what's happening:
```yaml
# Add to configuration.yaml
logger:
  default: info
  logs:
    custom_components.pelican_thermostat: debug
```

### 10. Manual Configuration
If the UI doesn't work, you can try manual configuration:
```yaml
# Add to configuration.yaml
pelican_thermostat:
  username: "your_username"
  password: "your_password"
  base_url: "https://your-site.officeclimatecontrol.net/api.cgi"
  thermostat_name: "Your Thermostat Name"
  poll_interval: 70
```

## Common Error Messages

### "Integration not found"
- Restart Home Assistant
- Check file permissions
- Verify all files are present

### "Import error"
- Check Python syntax in all files
- Ensure all imports are correct
- Look for missing dependencies

### "Configuration flow not found"
- Verify `config_flow: true` in manifest.json
- Check config_flow.py file exists and is valid

## Still Having Issues?

If none of the above solutions work:
1. Check the Home Assistant logs for specific error messages
2. Try installing via HACS instead of manual installation
3. Verify your Home Assistant version is compatible (2023.8.0+)
4. Create an issue on GitHub with the specific error message

## Testing the Integration

Once configured, you can test if it's working:
1. Check if entities appear in **Settings** → **Devices & Services**
2. Look for climate and sensor entities
3. Check the logs for successful API calls
4. Try controlling the thermostat from the UI 