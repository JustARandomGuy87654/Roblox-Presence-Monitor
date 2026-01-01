# IMPORTANT: this code only works if the person has their join on for everyone, or if the ROBLOXSECURIY cookie that u put is friend with the account

import requests
import time
from datetime import datetime, timezone

print("Roblox Presence Monitor")
print("Made by nyx")
print("-" * 30)

# Using an alt account for this is strongly recommend because roblox doenst like a lot of requests to their website
ROBLOSECURITY = input("Enter your .ROBLOSECURITY cookie (I recommend you use a alt account for): ").strip()
USER_ID = int(input("Enter the Roblox User ID to monitor: ").strip())

while True:
    try:
        CHECK_INTERVAL = int(input("Enter check interval in seconds (min 15): ").strip())
        if CHECK_INTERVAL < 15:
            print("Interval must be at least 15 seconds.")
        else:
            break
    except ValueError:
        print("Please enter a valid number.")

DISCORD_WEBHOOK = input("Enter Discord webhook URL: ").strip()

print("\nStarting monitor...\n")

# ================= CONFIG =================

PRESENCE_MAP = {
    0: "Offline",
    1: "Online",
    2: "In Game",
    3: "In Studio"
}

session = requests.Session()
session.headers.update({
    "Cookie": f".ROBLOSECURITY={ROBLOSECURITY}",
    "Content-Type": "application/json",
    "User-Agent": "RobloxPresenceMonitor/3.0"
})

last_status = None
last_place_id = None

def get_presence():
    url = "https://presence.roblox.com/v1/presence/users"
    payload = {"userIds": [USER_ID]}
    r = session.post(url, json=payload)
    r.raise_for_status()
    return r.json()["userPresences"][0]


def get_user_info():
    r = session.get(f"https://users.roblox.com/v1/users/{USER_ID}")
    r.raise_for_status()
    return r.json()


def get_avatar_url():
    url = (
        "https://thumbnails.roblox.com/v1/users/avatar-headshot"
        f"?userIds={USER_ID}&size=420x420&format=Png&isCircular=false"
    )
    r = session.get(url)
    r.raise_for_status()
    data = r.json()
    return data["data"][0]["imageUrl"] if data.get("data") else None


def get_game_name(place_id):
    if not place_id:
        return None

    u = session.get(
        f"https://apis.roblox.com/universes/v1/places/{place_id}/universe"
    )
    if u.status_code != 200:
        return None

    universe_id = u.json()["universeId"]

    g = session.get(
        f"https://games.roblox.com/v1/games?universeIds={universe_id}"
    )
    if g.status_code != 200:
        return None

    data = g.json().get("data", [])
    return data[0]["name"] if data else None


def send_embed(username, avatar_url, status_text, game_name=None, game_id=None):
    embed = {
        "author": {
            "name": username,
            "icon_url": avatar_url
        },
        "description": f"**Status:** {status_text}",
        "color": 0x5865F2,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "footer": {
            "text": "Roblox Presence Monitor • made by nyx"
        }
    }

    if game_name and game_id:
        embed["description"] += (
            f"\n🎮 **Game:** [{game_name}]"
            f"(https://www.roblox.com/games/{game_id})"
        )

    if "ENTERED" in status_text:
        embed["color"] = 0x57F287
    elif "LEFT" in status_text:
        embed["color"] = 0xED4245

    session.post(DISCORD_WEBHOOK, json={"embeds": [embed]})

# Main
user_info = get_user_info()
username = user_info["name"]
avatar_url = get_avatar_url()

print(f"Monitoring user: {username} ({USER_ID})")
print("-" * 30)

while True:
    try:
        presence = get_presence()
        status = presence["userPresenceType"]
        place_id = presence.get("placeId")
        status_name = PRESENCE_MAP.get(status, "Unknown")

        if last_status is not None:

            # Entrou em game
            if status == 2 and last_status != 2:
                game_name = get_game_name(place_id)
                send_embed(
                    username,
                    avatar_url,
                    "🟢 ENTERED A GAME",
                    game_name,
                    place_id
                )

            # Saiu do game
            elif last_status == 2 and status != 2:
                game_name = get_game_name(last_place_id)
                send_embed(
                    username,
                    avatar_url,
                    "🔴 LEFT THE GAME",
                    game_name,
                    last_place_id
                )

            elif status != last_status:
                send_embed(
                    username,
                    avatar_url,
                    f"ℹ️ {PRESENCE_MAP.get(last_status)} → {status_name}"
                )

        last_status = status
        last_place_id = place_id

        time.sleep(CHECK_INTERVAL)

    except requests.exceptions.RequestException as e:
        print("Network error:", e)
        time.sleep(30)

    except Exception as e:
        print("Unexpected error:", e)
        time.sleep(30)
