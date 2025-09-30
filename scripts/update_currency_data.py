#!/usr/bin/env python3
"""
Update currency data and deploy to GitHub Pages.

This script:
1. Fetches latest currency rates from exchangerate-api.com
2. Creates optimized JSON files for GitHub Pages
3. Generates metadata with statistics
"""

import requests
import json
import os
from datetime import datetime, timedelta
from typing import Dict, Any, Optional

# Configuration
DOCS_DIR = "docs"
CURRENCY_API_URL = "https://api.exchangerate-api.com/v4/latest/EUR"

TARGET_CURRENCIES = [
    'AUD', 'CAD', 'CHF', 'CZK', 'DKK', 'GBP', 'HKD', 'HUF', 'JPY', 'KRW',
    'NOK', 'NZD', 'PLN', 'SEK', 'SGD', 'USD', 'ZAR', 'TRY', 'IDR', 'MYR',
    'PHP', 'THB', 'RON', 'MXN', 'CNY', 'BRL', 'INR', 'ILS', 'BGN'
]

def ensure_docs_directory():
    """Ensure docs directory exists."""
    os.makedirs(DOCS_DIR, exist_ok=True)

def fetch_latest_rates_from_api() -> Optional[Dict[str, float]]:
    """Fetch today's rates from exchangerate-api.com"""
    try:
        print("📡 Fetching latest rates from exchangerate-api.com...")
        response = requests.get(CURRENCY_API_URL, timeout=10)
        response.raise_for_status()

        data = response.json()
        rates = data.get('rates', {})

        # Filter to our target currencies
        filtered_rates = {
            currency: rates[currency]
            for currency in TARGET_CURRENCIES
            if currency in rates
        }

        print(f"✅ Fetched {len(filtered_rates)} currency rates")
        return filtered_rates

    except Exception as e:
        print(f"❌ Error fetching from API: {e}")
        return None

def load_existing_data() -> Dict[str, Any]:
    """Load existing currency data or create new structure."""
    currency_file = os.path.join(DOCS_DIR, "currency_rates.json")

    if os.path.exists(currency_file):
        with open(currency_file, 'r', encoding='utf-8') as f:
            return json.load(f)

    # Create new structure
    return {
        'metadata': {
            'base_currency': 'EUR',
            'currencies': TARGET_CURRENCIES,
            'data_source': 'European Central Bank via exchangerate-api.com',
            'last_updated': datetime.now().isoformat(),
            'total_records': 0,
            'earliest_date': datetime.now().strftime('%Y-%m-%d'),
            'latest_date': datetime.now().strftime('%Y-%m-%d')
        },
        'currencies': TARGET_CURRENCIES,
        'rates_by_year': {}
    }

def update_currency_data():
    """Main function to update all currency data files."""
    ensure_docs_directory()

    print("🔄 Starting currency data update...")

    # Load existing data
    data = load_existing_data()

    # Get today's date
    today = datetime.now().strftime('%Y-%m-%d')
    current_year = str(datetime.now().year)

    # Fetch latest rates
    latest_rates = fetch_latest_rates_from_api()

    if latest_rates:
        # Ensure year structure exists
        if current_year not in data['rates_by_year']:
            data['rates_by_year'][current_year] = {}

        # Update today's rates - convert to array format
        month_day = today[5:]  # MM-DD format
        rates_array = []
        for currency in TARGET_CURRENCIES:
            rates_array.append(latest_rates.get(currency, None))

        data['rates_by_year'][current_year][month_day] = rates_array

        # Update metadata
        data['metadata'].update({
            'last_updated': datetime.now().isoformat(),
            'latest_date': today,
            'total_records': sum(len(year_data) for year_data in data['rates_by_year'].values())
        })

        print(f"✅ Updated data for {today}")

        # Save full data file
        currency_file = os.path.join(DOCS_DIR, "currency_rates.json")
        with open(currency_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, separators=(',', ':'))

        # Create latest.json (today's rates only)
        latest_data = {
            'date': today,
            'base_currency': 'EUR',
            'rates': latest_rates,
            'last_updated': datetime.now().isoformat()
        }

        latest_file = os.path.join(DOCS_DIR, "latest.json")
        with open(latest_file, 'w', encoding='utf-8') as f:
            json.dump(latest_data, f, ensure_ascii=False, indent=2)

        # Create metadata.json
        metadata = {
            'base_currency': 'EUR',
            'supported_currencies': ['EUR'] + TARGET_CURRENCIES,
            'total_currencies': len(TARGET_CURRENCIES) + 1,
            'data_source': 'European Central Bank via exchangerate-api.com',
            'last_updated': datetime.now().isoformat(),
            'total_records': data['metadata']['total_records'],
            'latest_date': today,
            'date_range': {
                'start': data['metadata'].get('earliest_date', today),
                'end': today
            },
            'file_sizes': {
                'full_data_mb': round(os.path.getsize(currency_file) / 1024 / 1024, 2),
                'latest_kb': round(os.path.getsize(latest_file) / 1024, 2)
            }
        }

        metadata_file = os.path.join(DOCS_DIR, "metadata.json")
        with open(metadata_file, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, ensure_ascii=False, indent=2)

        print(f"📊 Files updated:")
        print(f"  • currency_rates.json: {metadata['file_sizes']['full_data_mb']} MB")
        print(f"  • latest.json: {metadata['file_sizes']['latest_kb']} KB")
        print(f"  • metadata.json: Updated")
        print(f"  • Sample rates: USD={latest_rates.get('USD')}, GBP={latest_rates.get('GBP')}")

    else:
        print("❌ Failed to fetch latest rates, no update performed")
        exit(1)

if __name__ == "__main__":
    update_currency_data()
    print("🎉 Currency data update completed!")