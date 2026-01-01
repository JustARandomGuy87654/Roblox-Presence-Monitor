# Roblox-Presence-Monitor
A chill lil project I made out of boredom
its a simple Roblox user monitor that tells you when someone joins a game, leaves, or goes offline/online
nothing fancy, just some Python + Discord magic to keep an eye on people
It uses requests for HTTP stuff and datetime for timestamps

## How it works (kinda
- Python script that hits Roblox APIs
- Uses .ROBLOSECURITY to get presence info
- Sends embeds to your Discord webhook
- Checks every X seconds (you choose, minimum 15s)
- Handles Studio & actual game, so you can see if they re actually playing or just deving stuff

## Techy stuff 
requests - for all the API calls
datetime - timestamps in embeds
Discord Webhooks - for the notifications
No frameworks, no GUI, just raw Python and discord

## Why did i make this
First, i have nothing to do, secound, idk

Made by nyx
My discord: myxxz
