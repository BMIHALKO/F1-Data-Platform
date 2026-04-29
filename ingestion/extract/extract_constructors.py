"""
Extract Constructor reference data from the Jolpica API

This file retrieves constructor/team metadata, handles pagination, and returns records ready for loading into staging.constructors
"""

import time
import requests

BASE_URL = "https://api.jolpi.ca/ergast/f1"

def flatten_constructor(constructor):
    return {
        "constructor_id": constructor.get("constructorId"),
        "constructor_name": constructor.get("name"),
        "nationality": constructor.get("nationality"),
        "profile_url": constructor.get("url"),
    }

def extract_constructors():
    limit = 100
    offset = 0

    all_constructors = []

    while True:
        url = f"{BASE_URL}/constructors.json"
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

        constructors = (
            data.get("MRData", {})
            .get("ConstructorTable", {})
            .get("Constructors", {})
        )

        if not constructors:
            break

        all_constructors.extend(
            flatten_constructor(constructor)
            for constructor in constructors
        )

        if len(constructors) < limit:
            break

        offset += limit
        time.sleep(1)
    
    return all_constructors

if __name__ == "__main__":
    constructors = extract_constructors()

    print(f"Extracted {len(constructors)} constructor records")
    
    for constructor in constructors[:3]:
        print(constructor)