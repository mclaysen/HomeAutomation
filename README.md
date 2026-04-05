# HomeAutomation

Basic Home Automation services for receiving sensor data and publishing/handling MQTT messages.

## Overview

This repository contains scripts and modules for:
- Reading sensor data (including rtl_433-based inputs)
- Mapping sensor payloads into internal models
- Publishing and subscribing to MQTT topics
- Logging and task-oriented processing

## Project Layout

- `mqtt.py` - Main MQTT-related runtime entrypoint
- `log.py` - Logging utilities
- `models/` - Data models for sensors and mappings
- `mqttHandlers/` - Publisher/subscriber handlers
- `tasks/` - Task scripts
- `inventories/` - Inventory/config data
- `logs/` - Runtime logs
- `config.ini`, `config.ini.dev`, `config.json` - Environment/config files

## Running With Linux Supervisor

On Linux (for example, Raspberry Pi), these services can be managed by Supervisor.

Example Supervisor config:

```ini
[program:rtl_433]
command=/home/pi/startup/rtl433.sh
autostart=true
autorestart=true
stderr_logfile=/var/log/rtl433.err.log
stdout_logfile=/var/log/rtl433.out.log

[program:mqtt]
command=/home/pi/startup/mqtt.sh
autostart=true
autorestart=true
stderr_logfile=/var/log/mqtt.err.log
stdout_logfile=/var/log/mqtt.out.log
environment=HOME="/home/pi",USER="pi"
```

Example `mqtt.sh` script:

```bash
#!/bin/bash
python3 /home/pi/applications/HomeAutomation/mqtt.py
```

Example `rtl433.sh` script:

```bash
#!/bin/bash
rtl_433 -f 433950000 -F mqtt://localhost:1883 -vv
```

### Typical Supervisor Steps

1. Save the config in a file such as `/etc/supervisor/conf.d/homeautomation.conf`.
2. Reload Supervisor config:
   ```bash
   sudo supervisorctl reread
   sudo supervisorctl update
   ```
3. Start services:
   ```bash
   sudo supervisorctl start rtl_433
   sudo supervisorctl start mqtt
   ```
4. Check status:
   ```bash
   sudo supervisorctl status
   ```

## Notes

- Ensure `/home/pi/startup/rtl433.sh` and `/home/pi/startup/mqtt.sh` are executable.
- Confirm Python dependencies and runtime environment are installed for your target device.
- Review log files in `/var/log/` for troubleshooting.
