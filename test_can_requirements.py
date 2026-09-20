import csv
from datetime import datetime

LOG_FILENAME = 'can_trace.csv'

def run_automated_tests():
    print("=========================================================")
    print("  RUNNING AUTOMATED QA TEST SUITE FOR CAN NETWORK LOGS")
    print("=========================================================\n")

    pass_req01 = True
    pass_req02 = True
    
    speed_violations = []
    timing_violations = []

    previous_timestamp = None

    with open(LOG_FILENAME, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        
        for index, row in enumerate(reader, start=1):
            timestamp_str = row['Timestamp']
            speed = float(row['VehicleSpeed_kmh'])
            current_timestamp = datetime.strptime(timestamp_str, '%Y-%m-%d %H:%M:%S.%f')

            # --- VALIDARE REQ-01: Overspeed Limit (100 km/h) ---
            if speed > 100:
                pass_req01 = False
                speed_violations.append((row['Timestamp'], speed))

            # --- VALIDARE REQ-02: Message Cycle Time (< 500 ms) ---
            if previous_timestamp is not None:
                delta_ms = (current_timestamp - previous_timestamp).total_seconds() * 1000
                if delta_ms > 500:
                    pass_req02 = False
                    timing_violations.append((row['Timestamp'], delta_ms))

            previous_timestamp = current_timestamp

    # --- AFISARE REZULTATE TESTE (REPORTING) ---
    print("TEST RESULT: REQ-01 [Overspeed Monitor (>100 km/h)]")
    if pass_req01:
        print("  🟢 PASSED: Toate vitezele au fost în limitele sigure.\n")
    else:
        print(f"  🔴 FAILED: Au fost detectate {len(speed_violations)} depășiri de viteză!")
        print(f"     Exemplu: La timestamp-ul {speed_violations[0][0]}, viteza a fost {speed_violations[0][1]} km/h.\n")

    print("TEST RESULT: REQ-02 [Message Periodicity (<500 ms)]")
    if pass_req02:
        print("  🟢 PASSED: Perioada mesajului 0x100 este stabilă.\n")
    else:
        print(f"  🔴 FAILED: S-au detectat întârzieri pe magistrală!")
        print(f"     Exemplu: La {timing_violations[0][0]}, timpul a fost de {timing_violations[0][1]:.2f} ms.\n")

if __name__ == '__main__':
    run_automated_tests()