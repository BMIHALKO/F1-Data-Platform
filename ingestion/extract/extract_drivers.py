"""
Extract driver reference data from the Jolpica API

This file retrieves driver metadata, handles pagination, and returns records ready for loading into staging.drivers
"""
import requests
import time

BASE_URL = "https://api.jolpi.ca/ergast/f1"

def flatten_driver(driver):
    return {
        "driver_id": driver.get("driverId"),
        "permanent_number": driver.get("permanentNumber"),
        "driver_code": driver.get("code"),
        "given_name": driver.get("givenName"),
        "family_name": driver.get("familyName"),
        "date_of_birth": driver.get("dateOfBirth"),
        "nationality": driver.get("nationality"),
        "profile_url": driver.get("url"),
    }

def extract_drivers():
    limit = 100
    offset = 0
    all_drivers = []

    while True:
        url = f"{BASE_URL}/drivers.json"
        params = {
            "limit": limit,
            "offset": offset,
        }

        response = requests.get(url, params = params, timeout = 30)

        if response.status_code == 429:
            raise RuntimeError(
                "Jolpica rate limit reached. Stop retrying and try again later"
            )

        data = response.json()

        drivers = (
            data.get("MRData", {})
            .get("DriverTable", {})
            .get("Drivers", [])
        )

        if not drivers:
            break

        all_drivers.extend(flatten_driver(driver) for driver in drivers)

        if len(drivers) < limit:
            break

        offset += limit
        time.sleep(1)

    return all_drivers

if __name__ == "__main__":
    drivers = extract_drivers()

    print(f"Extracted {len(drivers)} driver records")

    for driver in drivers[:3]:
        print(driver)