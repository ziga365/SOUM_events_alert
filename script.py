import sys
import requests
from bs4 import BeautifulSoup
import json
import os
from dateutil import parser

def format_date(date_str):
  if not date_str:
    return "nema"

  try:
     dt = parser.parse(date_str)
     return dt.strftime("%B %d, %Y ob %H:%M")
  except ValueError:
    return date_str

def send_discord(event):
   WEBHOOK_URL = os.environ["DISCORD_WEBHOOK_URL"]

   payload = {
      "username": "SOUM Dogodki alert",
      "avatar_url": "https://www.soum.si/wp-content/uploads/2021/02/logo_soum_new_2014_color.png",
      "content" : "nov event just dropped",
      "embeds" : [
         {
            "title": event['ime'],
            "url": event['url'],
            "color" : 2463422,
            "description": f"**Datum:** {format_date(event['datum'])}",
            "image": {
                  "url": event['slika']
              },
            "text" : f"Datum: {event['datum']}"
         }
      ],
   }
   response = requests.post(WEBHOOK_URL, json=payload)

URL = "https://www.soum.si/dogodki-soum/"
headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36"
}
SAVE_FILE = "existing_events.json"
ARCHIVE_FILE = "events_archive.json"

# get save file with events
if os.path.exists(SAVE_FILE) and os.path.getsize(SAVE_FILE) > 0:
  with open(SAVE_FILE, "r", encoding="utf-8") as file:
    saved_events = json.load(file)
else:
  saved_events = {}

# get archive to append to it
if os.path.exists(ARCHIVE_FILE) and os.path.getsize(ARCHIVE_FILE) > 0:
  with open(ARCHIVE_FILE, "r", encoding="utf-8") as file:
    archived_events = json.load(file)
else:
  archived_events = {}

current_events = {}

# get html
try:
  res = requests.get(URL, headers=headers)
  res.raise_for_status()
except requests.exceptions.RequestException as e:
  print(f"Something went wrong: {e}", file=sys.stderr)
  sys.exit(1)

juha = BeautifulSoup(res.text, "html.parser")
#print(res)

# get html parts tagged with .eventon_list_event
events = juha.select(".eventon_list_event")
print("tulk eventov trenutno: " + str(len(events)))
if not events:
   sys.exit(1)

for event in events:
    script_block = event.select_one('script[type="application/ld+json"]')
    if script_block:
        event_data = json.loads(script_block.string)

        event_id = event_data.get('@id')
        name = (event_data.get('name') or "").strip()
        url = event_data.get('url')
        start_date = event_data.get("startDate")
        end_date = event_data.get("endDate")
        image = event_data.get("image")

        current_events[event_id] = {
            "ime": name,
            "url": url,
            "datum": start_date,
            "slika": image
        }


saved_ids = set(saved_events.keys())
current_ids = set(current_events.keys())

new_ids = current_ids - saved_ids
removed_ids = saved_ids - current_ids

if new_ids:
   print(len(new_ids), " novih eventov")
   for event_id in new_ids:
      event = current_events[event_id]
      send_discord(event)
else:
   print("nic novega")

if removed_ids:
   print("ene " + str(len(removed_ids)) + " so zbrisal, je slo v arhiv.")
   for event_id in removed_ids:
      event = saved_events[event_id]
      archived_events[event_id] = event


with open(SAVE_FILE, "w", encoding="utf-8") as file:
  json.dump(current_events, file, indent=4, ensure_ascii=False)

with open(ARCHIVE_FILE, "w", encoding="utf-8") as file:
  json.dump(archived_events, file, indent=4, ensure_ascii=False)