import serial, time
from pymavlink import mavutil

print("🚀 Launching Production MAVLink GPS Bridge...")

def parse_deg(s, d):
    if not s or '.' not in s: return None
    try:
        p = s.find('.')
        deg = float(s[:p-2]) + (float(s[p-2:]) / 60.0)
        return int(-deg * 1e7) if d in ['S', 'W'] else int(deg * 1e7)
    except: return None

try:
    ser = serial.Serial('/dev/ttyGPS', 115200, timeout=1)
    print("✅ Locked onto permanent /dev/ttyGPS hardware link")
except Exception as e:
    print(f"❌ Hardware Error: {e}"); exit(1)

mav = mavutil.mavlink_connection('udpout:127.0.0.1:14550', source_system=1, source_component=220)
print("✅ Core Telemetry Port 14550 Linked")
print("="*80)

hb, pr = 0, 0
while True:
    try:
        t = time.time()
        if t - hb > 1.0:
            mav.mav.heartbeat_send(mavutil.mavlink.MAV_TYPE_GCS, mavutil.mavlink.MAV_AUTOPILOT_INVALID, 0, 0, 0)
            hb = t
        if ser.in_waiting > 0:
            line = ser.readline().decode('ascii', errors='ignore').strip()
            if "$GNGGA" in line or "$GPGGA" in line:
                p = line.split(',')
                if len(p) >= 8:
                    sat = int(p[7]) if p[7].isdigit() else 0
                    hdop = float(p[8]) if p[8].replace('.','',1).isdigit() else 99.99
                    lat, lon = parse_deg(p[2], p[3]), parse_deg(p[4], p[5])
                    mode = "OUTDOORS (LIVE GNSS)" if lat and lon else "INDOORS (DESK SETUP)"
                    lat_o = lat if lat else int(45.0 * 1e7)
                    lon_o = lon if lon else int(-93.0 * 1e7)
                    mav.mav.gps_input_send(0, 0, 0, 0, 0, 3, lat_o, lon_o, 10.0, hdop, 99.99, 0, 0, 0, 0, 0, 0, sat)
                    if t - pr > 1.0:
                        print(f"🛰️  [{mode}] Wire Active -> Satellites: {sat} | HDOP: {hdop}")
                        pr = t
        else: time.sleep(0.05)
    except KeyboardInterrupt: break
    except: continue
