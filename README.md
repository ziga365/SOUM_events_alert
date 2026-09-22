# ŠOUM Event Tracker

A small Python scraper that checks a university event page, keeps track of events locally, and sends Discord notifications when new events are published.

## Features
- Scrapes event data from the page's embedded JSON-LD.
- Detects newly added and removed events.
- Keeps a local archive of events in JSON files.
- Sendsnew events to Discord using webhooks.

## Setup
1. **Clone or download** the project files into a local directory.

2. **Install the dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
3. **Set your Discord Webhook URL** as an environment variable
    - macOS / Linux
   ```bash
   export DISCORD_WEBHOOK_URL="your_webhook_url_here"
   ```
    - Windows 10 / 11
   ```bash
   $env:DISCORD_WEBHOOK_URL="your_webhook_url_here"
   ```
4. **Run** the script:
   ```bash
   python script.py
   ```