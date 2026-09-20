import os
import csv
import time
import datetime
import threading
import can
import cantools


DBC_FILENAME = 'engine.dbc'
DBC_CONTENT = """VERSION ""
NS_ :
BS_:
BU_: EngineECU DashboardECU

BO_ 256 EngineData: 8 EngineECU
 SG_ EngineSpeed : 0|16@1+ (1,0) [0|8000] "RPM" DashboardECU
 SG_ VehicleSpeed : 16|8@1+ (1,0) [0|250] "km/h" DashboardECU
"""

if not os.path.exists(DBC_FILENAME):
    with open(DBC_FILENAME, 'w', encoding='utf-8') as f:
        f.write(DBC_CONTENT)


db = cantools.database.load_file(DBC_FILENAME)
engine_msg = db.get_message_by_name('EngineData')


LOG_FILENAME = 'can_trace.csv'


with open(LOG_FILENAME, 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['Timestamp', 'CAN_ID_Hex', 'RAW_Payload_Hex', 'EngineSpeed_RPM', 'VehicleSpeed_kmh'])


bus = can.interface.Bus(interface='virtual', channel='vcan0', bitrate=500000, receive_own_messages=True)



def dashboard_listener(msg):
    if msg.arbitration_id == engine_msg.frame_id:
        decoded = db.decode_message(msg.arbitration_id, msg.data)
        rx_rpm = decoded['EngineSpeed']
        rx_speed = decoded['VehicleSpeed']
        print(f"   [RX Dashboard] Display -> RPM: {rx_rpm} | Viteza: {rx_speed} km/h")



def logger_listener(msg):
    
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
    can_id_hex = f"0x{msg.arbitration_id:X}"
    raw_payload_hex = msg.data.hex().upper()
    
    rpm = "N/A"
    speed = "N/A"
    
    
    if msg.arbitration_id == engine_msg.frame_id:
        decoded = db.decode_message(msg.arbitration_id, msg.data)
        rpm = decoded['EngineSpeed']
        speed = decoded['VehicleSpeed']
        
   
    with open(LOG_FILENAME, 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow([timestamp, can_id_hex, raw_payload_hex, rpm, speed])



def engine_ecu_node():
    rpm = 1000
    speed = 0
    while True:
        data_bytes = engine_msg.encode({
            'EngineSpeed': rpm,
            'VehicleSpeed': speed
        })
        
        msg = can.Message(
            arbitration_id=engine_msg.frame_id,
            data=data_bytes,
            is_extended_id=False
        )
        
        bus.send(msg)
        print(f"[TX EngineECU] Sent CAN ID 0x{engine_msg.frame_id:X} -> RPM: {rpm} | Speed: {speed} km/h")
        
        rpm = (rpm + 200) if rpm < 6000 else 1000
        speed = (speed + 5) if speed < 200 else 0
        
        time.sleep(0.3)



print("=========================================================")
print("  SIMULARE CAN + TRACE LOGGING (can_trace.csv)")
print("=========================================================\n")

notifier = can.Notifier(bus, [dashboard_listener, logger_listener])


t_engine = threading.Thread(target=engine_ecu_node, daemon=True)
t_engine.start()

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    notifier.stop()
    print("\nSimulare oprita. Log-urile au fost salvate in 'can_trace.csv'.")