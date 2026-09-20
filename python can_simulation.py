import time 
import can

bus = can.interface.Bus(interface='virtual', channel='can0', bitrate=500000)

print("Simularea CAN a pornit! Apasa Ctrl+C pentru a opri.")

engine_rpm = 800

try: 
    while True:
        data_bytes = [(engine_rpm >> 8) & 0xFF, engine_rpm & 0xFF, 0, 0, 0, 0,0, 0] 

        msg = can.Message(
            arbitration_id=0x100,
            data=data_bytes,
            is_extended_id=False
        )

        bus.send(msg)
        print(f"Trimis pachet CAN 0x100 | RPM: {engine_rpm}")

        engine_rpm = engine_rpm + 100 if engine_rpm <6000 else 800
        time.sleep(0.1)

except KeyboardInterrupt:
    print("\nSimulare oprita")