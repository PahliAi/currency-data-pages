#!/usr/bin/env python3
"""
Bootstrap currency-data-pages with existing data.
Creates latest.json and metadata.json from your current currency_rates.json
"""

import json
import os
import shutil
from datetime import datetime

def bootstrap_currency_pages():
    """Bootstrap GitHub Pages data from existing currency data."""

    # Paths
    source_file = "C:/DEV/Currency/data/currency_rates.json"
    docs_dir = "../docs"

    print("Bootstrapping currency-data-pages...")

    # Create docs directory
    os.makedirs(docs_dir, exist_ok=True)

    # Copy main currency file
    print("1. Copying main currency data file...")
    shutil.copy2(source_file, f"{docs_dir}/currency_rates.json")

    # Load existing data
    print("2. Loading existing currency data...")
    with open(source_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Get latest rates from your data
    print("3. Extracting latest rates...")
    latest_year = max(data['data'].keys())
    latest_date = max(data['data'][latest_year].keys())
    latest_rates_array = data['data'][latest_year][latest_date]
    currencies = data['metadata']['currencies']

    # Create rate dictionary
    latest_rates = {}
    for i, currency in enumerate(currencies):
        if i < len(latest_rates_array) and latest_rates_array[i] is not None:
            latest_rates[currency] = latest_rates_array[i]

    # Create latest.json
    print("4. Creating latest.json...")
    latest_data = {
        'date': latest_date,
        'base_currency': 'EUR',
        'rates': latest_rates,
        'last_updated': datetime.now().isoformat()
    }

    with open(f"{docs_dir}/latest.json", 'w', encoding='utf-8') as f:
        json.dump(latest_data, f, indent=2, ensure_ascii=False)

    # Create metadata.json
    print("5. Creating metadata.json...")

    # Calculate file sizes
    full_size = os.path.getsize(f"{docs_dir}/currency_rates.json")
    latest_size = os.path.getsize(f"{docs_dir}/latest.json")

    metadata = {
        'base_currency': 'EUR',
        'supported_currencies': ['EUR'] + currencies,
        'total_currencies': len(currencies) + 1,
        'data_source': 'European Central Bank via exchangerate-api.com',
        'last_updated': datetime.now().isoformat(),
        'total_records': data['metadata']['total_records'],
        'latest_date': latest_date,
        'file_sizes': {
            'full_data_mb': round(full_size / 1024 / 1024, 2),
            'latest_kb': round(latest_size / 1024, 2)
        }
    }

    with open(f"{docs_dir}/metadata.json", 'w', encoding='utf-8') as f:
        json.dump(metadata, f, indent=2, ensure_ascii=False)

    # Summary
    print(f"\nBootstrap completed successfully!")
    print(f"✓ currency_rates.json: {metadata['file_sizes']['full_data_mb']} MB")
    print(f"✓ latest.json: {metadata['file_sizes']['latest_kb']} KB")
    print(f"✓ metadata.json: Created")
    print(f"✓ Latest data date: {latest_date}")
    print(f"✓ Total currencies: {len(currencies)}")
    print(f"✓ Total records: {metadata['total_records']}")

    print(f"\nNext steps:")
    print(f"1. git add docs/")
    print(f"2. git commit -m 'Add initial currency data'")
    print(f"3. git push origin main")
    print(f"4. Enable GitHub Pages (Settings → Pages → docs folder)")

if __name__ == "__main__":
    bootstrap_currency_pages()