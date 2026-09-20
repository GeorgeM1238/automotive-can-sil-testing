import csv
import pytest
from datetime import datetime

LOG_FILENAME = 'can_trace.csv'

@pytest.fixture(scope="module")
def trace_data():
    """Incarca datele din logul CAN inainte de rularea testelor."""
    rows = []
    with open(LOG_FILENAME, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append(row)
    return rows

def test_req_01_speed_limits(trace_data):
    """REQ-01: Identifica si raporteaza toate evenimentele de depasire a vitezei de siguranta (>120 km/h)."""
    overspeed_entries = [row for row in trace_data if float(row['VehicleSpeed_kmh']) > 120]
    
   
    print(f"\n[INFO QA] Au fost detectate {len(overspeed_entries)} cadre cu viteza peste limita de 120 km/h.")
    
   
    assert len(trace_data) > 0, "Fișierul de log este gol!"

def test_req_02_message_periodicity(trace_data):
    """REQ-02: Verifica daca intervalul dintre două mesaje consecutive nu depaseste 500ms."""
    previous_ts = None
    for row in trace_data:
        current_ts = datetime.strptime(row['Timestamp'], '%Y-%m-%d %H:%M:%S.%f')
        if previous_ts:
            delta_ms = (current_ts - previous_ts).total_seconds() * 1000
            assert delta_ms <= 500, f"Intarziere detectata: {delta_ms:.2f} ms la {row['Timestamp']}"
        previous_ts = current_ts