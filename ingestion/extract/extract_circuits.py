"""
Extract circuit reference data from the Jolpica API

This file retrieves circuit/location metadata, handles pagination, and returns records ready for loading into staging.circuits
"""

import time
import requests

BASE_URL = "https://api.jolpi.ca/ergast/f1"

def flatten_circuit(circuit):
    location = circuit.get("Location", {})

    return {
        "circuit_id": circuit.get("circuitId"),
        "circuit_name": circuit.get("circuitName"),
        "latitude": location.get("lat"),
        "longitude": location.get("long"),
        "locality": location.get("locality"),
        "country": location.get("country"),
        "profile_url": circuit.get("url"),
    }

def extract_cicuits():
    limit = 100
    offset = 0

    all_circuits = []

    while True:
        url = f"{BASE_URL}/circuits.json"
        params = {
            "limit": limit,
            "offset": offset,
        }

        response = requests.get(url, params = params, timeout = 30)

        if response.status_code == 429:
            raise RuntimeError(
                "Jolpica rate limit reached. Stop retrying and try again later."
            )

        response.raise_for_status()

        data = response.json()

        circuits = (
            data.get("MRData", {})
            .get("CircuitTable", {})
            .get("Circuits", [])
        )

        if not circuits:
            break

        all_circuits.extend(
            flatten_circuit(circuit)
            for circuit in circuits
        )

        if len(circuits) < limit:
            break

        offset += limit
        time.sleep(1)

    return all_circuits

if __name__ == "__main__":
    circuits = extract_cicuits()

    print(f"Extracted {len(circuits)} circuit records")
    
    for circuit in circuits[:3]:
        print(circuit)