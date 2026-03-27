# Perak Flight Monitoring Dashboard

This project is an IoT-based flight monitoring system that collects aircraft data over Perak, Malaysia using the OpenSky Network API.

## Features
- Real-time and historical flight data collection
- SQLite database storage
- Dashboard visualisation using Streamlit
- Charts for flight frequency and altitude trends
- Map view of aircraft positions

## Files
- `collector.py` – collects and stores flight data
- `dashboard.py` – displays the dashboard
- `database.db` – stores collected data
- `requirements.txt` – Python dependencies

## Run the collector
```bash
py collector.py