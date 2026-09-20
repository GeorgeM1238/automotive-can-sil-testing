import can

bus = can.interface.Bus(interface='virtual', channel='vcan0', bitrate=500000)

print("Nodul Dashboard (receptor) asculta magistrala CAN...\n")

try:
    while True:
        msg = bus.recv()

        if msg and msg.arbitration_id == 0x100:

            rpm = (msg.data[0] << 8) | msg.data[1]
            print(f"[RX Dashboard] Pachet primit | ID: 0x{msg.arbitration_id:X} -> RPM afisat pe ecran:{rpm}")

except KeyboardInterrupt:
    print("\nReceptor oprit.")