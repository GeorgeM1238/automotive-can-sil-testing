# CAN Bus SIL Test Environment & Requirement Verification

![Build Status](https://github.com/GeorgeM1238/automotive-can-sil-testing/actions/workflows/ci.yml/badge.svg)

Software-in-the-Loop (SIL) test framework for CAN communication and automated requirement verification. The project simulates EngineECU and DashboardECU traffic over a virtual CAN interface using DBC definitions, logs frame data to CSV, and executes automated pass/fail checks.

## Verified Requirements

* **REQ-01 (Vehicle Speed Limit):** Signals decoded from frame `0x100` must not exceed the maximum threshold of 120 km/h.
* **REQ-02 (Cycle Time):** Inter-frame latency for cyclic message `EngineData` (`0x100`) must remain <= 500 ms.

## System Architecture

* **`can_network_sim.py`**: Rest-bus simulation using `python-can` and `cantools`. Runs multi-threaded ECU nodes and logs real-time traffic to `can_trace.csv`.
* **`test_can_suite.py`**: Automated test suite implemented with `pytest`. Parses trace logs to validate system requirements against ISO 26262/ASPICE guidelines.
* **`engine.dbc`**: DBC database defining frame layout and signal encoding (`EngineSpeed`, `VehicleSpeed`).
* **`.github/workflows/ci.yml`**: CI pipeline executing headless simulation and test runs on Linux runners (`ubuntu-latest`).

## Local Execution

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt