# Competitor Price Monitor

The **Competitor Price Monitor** is a Python-based tool designed to track product prices from competitor websites, send alerts for price drops, and provide daily email reports. This tool is perfect for businesses that want to stay competitive by monitoring market prices and receiving timely updates.

## Features

- **Price Monitoring**: Monitors product prices from multiple competitor URLs.
- **Price Drop Alerts**: Sends email alerts when a product's price drops by a specified percentage threshold (default 10%).
- **Historical Data Tracking**: Logs product price data in a CSV file with timestamps.
- **Daily Reports**: Sends daily email reports summarizing monitored product prices.
- **Email Integration**: Notifies users about price changes and sends reports via email.
- **Customizable Monitoring Interval**: Set the monitoring interval to suit your business needs (default is 24 hours).

## Requirements

- Python 3.x
- `requests`: For sending HTTP requests to competitor websites.
- `beautifulsoup4`: For parsing and extracting data from HTML.
- `smtplib`: For sending emails via Gmail’s SMTP server.
- `csv`: For writing product price data to CSV files.

### Install Required Libraries

```bash
pip install requests beautifulsoup4
