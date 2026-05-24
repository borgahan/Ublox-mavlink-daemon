# blueos-mavlink-gps-bridge

## The Problem
The default BlueOS NMEA extension currently ignores modern multi-constellation NMEA talker IDs that start with `$GN`. It expects the legacy `$GP` prefix exclusively. This discrepancy causes data stream blindness when using modern u-blox or multi-constellation GNSS modules, resulting in 0 satellite indicators on the interface and aggressive dashboard flickering as telemetry systems fail to interpret the GNSS messages correctly.

## The Solution
The `blueos-mavlink-gps-bridge` project intercepts the raw NMEA strings from the GPS receiver and actively bridges them into standard MAVLink telemetry before pushing them out via `udpout:127.0.0.1:14550`.

Key features include:
- **Non-Blocking Memory Queue:** Implements a strict `ser.in_waiting` memory queue logic to prevent terminal or Docker port hanging and improve stream reliability.
- **Permanent UDEV Vendor Mapping:** Introduces permanent UDEV rules to map the hardware consistently to `/dev/ttyGPS`, effectively eliminating the dynamic device port drift typical in Linux environments when USB devices are reconnected.
- **Direct MAVLink Injection:** Connects securely to the core telemetry port `14550` and dynamically broadcasts parsed `$GNGGA` and `$GPGGA` streams as `GPS_INPUT` MAVLink messages.

## The Setup
1. Transfer this repository to the target device (e.g., Raspberry Pi).
2. Give the installation script executable permissions:
   ```bash
   chmod +x install.sh
   ```
3. Run the installation script to configure UDEV rules and install the Systemd background daemon:
   ```bash
   ./install.sh
   ```
4. Check the live background daemon logs to verify operation:
   ```bash
   sudo journalctl -u gps_bridge.service -f
   ```
