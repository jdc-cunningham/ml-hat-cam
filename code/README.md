### Boot

There is a boot script that runs the OLED menu/waits for button input

It uses systemd, see the basic service file below below (systemd service)

`WorkingDirectory` is very important, otherwise the imported python paths can break

```
[Unit]
Description=Start ML Hat Cam
After=multi-user.target

[Service]
Type=idle
WorkingDirectory=/home/pi/ml-hat-cam/code
User=root
ExecStart=/usr/bin/python3 /home/pi/ml-hat-cam/code/boot.py
Restart=no

[Install]
WantedBy=multi-user.target
```

Commands for myself

```
$sudo nano /etc/systemd/system/boot_ml-hat-cam.service
$sudo systemctl daemon-reload
$sudo systemctl restart boot_ml-hat-cam.service
```
