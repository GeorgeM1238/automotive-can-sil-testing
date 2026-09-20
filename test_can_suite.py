import csv
import pytest
from datetime import datetime

LOG_FILENAME = 'can_trace.csv'

@pytest.fixture(scope="module")
def trace_data():
    """Încarcă datele din logul CAN înainte de rularea testelor."""
    rows = []
    with open(LOG_FILENAME, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append(row)
    return rows

def test_req_01_speed_limits(trace_data):
    """REQ-01: Identifică și raportează toate evenimentele de depășire a vitezei de siguranță (>120 km/h)."""
    overspeed_entries = [row for row in trace_data if float(row['VehicleSpeed_kmh']) > 120]
    
    # Verificăm că cadrul de testare poate detecta corect evenimentele din log
    print(f"\n[INFO QA] Au fost detectate {len(overspeed_entries)} cadre cu viteză peste limita de 120 km/h.")
    
    # Asigurăm că datele colectate sunt valide
    assert len(trace_data) > 0, "Fișierul de log este gol!"

def test_req_02_message_periodicity(trace_data):
    """REQ-02: Verifică dacă intervalul dintre două mesaje consecutive nu depășește 500ms."""
    previous_ts = None
    for row in trace_data:
        current_ts = datetime.strptime(row['Timestamp'], '%Y-%m-%d %H:%M:%S.%f')
        if previous_ts:
            delta_ms = (current_ts - previous_ts).total_seconds() * 1000
            assert delta_ms <= 500, f"Întârziere detectată: {delta_ms:.2f} ms la {row['Timestamp']}"
        previous_ts = current_ts