# Currency Data Pages

GitHub Pages repository providing real-time currency exchange rate data for MCP Currency server.

## Live Data Endpoints

- **Latest Rates**: https://pahliai.github.io/currency-data-pages/latest.json
- **Full Historical Data**: https://pahliai.github.io/currency-data-pages/currency_rates.json
- **Metadata**: https://pahliai.github.io/currency-data-pages/metadata.json

## Features

- 29+ major currencies with EUR as base
- Daily updates at 6:00 AM CET
- Historical data back to 1999
- Optimized JSON structure for fast queries
- GitHub Actions automated deployment

## Manual Update

To manually trigger a currency data update:

1. Go to the **Actions** tab
2. Select **Update Currency Data** workflow
3. Click **Run workflow**

## Data Structure

### latest.json
```json
{
  "date": "2025-09-29",
  "base_currency": "EUR",
  "rates": {
    "USD": 1.1234,
    "GBP": 0.8567,
    ...
  },
  "last_updated": "2025-09-29T08:00:00Z"
}
```

### currency_rates.json
Optimized array-based structure with rates organized by year for efficient storage and fast queries.

## Usage with MCP Currency

This repository provides the data backend for the [Currency MCP](https://github.com/pahliai/currency-mcp) server.