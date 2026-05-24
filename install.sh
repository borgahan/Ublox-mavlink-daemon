#!/bin/bash
echo "🛰️  Setting up persistent UDEV hardware rules for u-blox modules..."
echo 'SUBSYSTEM=="tty", ATTRS{idVendor}=="1546", SYMLINK+="ttyGPS", MODE="0666"' | sudo tee /etc/udev/rules.d/99-ublox-gps.rules
sudo udevadm control --reload-rules && sudo udevadm trigger

echo "🔧 Installing Systemd background worker daemon..."
sudo cp gps_bridge.service /etc/systemd/system/gps_bridge.service

echo "🔄 Initializing background automation..."
sudo systemctl daemon-reload
sudo systemctl enable gps_bridge.service
sudo systemctl restart gps_bridge.service
echo "✅ Installation complete! Run 'sudo journalctl -u gps_bridge.service -f' to trace live logs."
