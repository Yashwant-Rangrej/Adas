#!/bin/bash
cd "$(dirname "$0")" || exit
ADAS_DIR=$(pwd)

echo "=== Installing ADAS as a Startup Service ==="

cat <<EOF | sudo tee /etc/systemd/system/adas.service
[Unit]
Description=ADAS Robot System
After=network.target

[Service]
Type=simple
User=$USER
WorkingDirectory=$ADAS_DIR
ExecStart=/bin/bash $ADAS_DIR/run.sh
Restart=on-failure
RestartSec=5

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl daemon-reload
sudo systemctl enable adas.service

echo ""
echo "✅ Service installed successfully!"
echo "The ADAS system will now start automatically every time you power on the robot."
echo ""
echo "Useful Commands:"
echo "- View live logs: sudo journalctl -u adas.service -f"
echo "- Stop system: sudo systemctl stop adas.service"
echo "- Start system: sudo systemctl start adas.service"
echo "- Disable auto-boot: sudo systemctl disable adas.service"
