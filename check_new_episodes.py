import os
import re
import requests

def scan_tv_shows(base_path):
    shows = {}
    for root, dirs, files in os.walk(base_path):
        for file in files:
          print(f"Scanning file: {file}")
            match = re.search(r"(S\d{2}E\d{2})", file, re.IGNORECASE)
            if match:
                rel_path = os.path.relpath(root, base_path).split(os.sep)
                if len(rel_path) >= 1:
                    show_name = rel_path[0]
                    episode = match.group(1).upper()
                    shows.setdefault(show_name, []).append(episode)
    return shows

def get_latest_episode(show_name):
    url = f"https://api.tvmaze.com/singlesearch/shows?q={show_name}&embed=episodes"
    try:
        response = requests.get(url)
        if response.status_code != 200:
            return "N/A"
        data = response.json()
        episodes = data['_embedded']['episodes']
        latest = max(
            (ep for ep in episodes if ep.get("airdate")),
            key=lambda ep: ep["season"] * 100 + ep["number"]
        )
        return f"S{latest['season']:02d}E{latest['number']:02d}"
    except Exception as e:
        return f"Error: {e}"

def check_for_updates(shows, base_path):
    print(f"📺 Checking for new episodes in {base_path}\n")
    for show, eps in shows.items():
        latest = get_latest_episode(show)
        if latest != "N/A" and latest not in eps:
            print(f"🔔 {show} is missing the latest episode: {latest}")
        else:
            print(f"✅ {show} is up to date.")

tv_path = "/mnt/user/Media/Media/TV Shows 1080P"
shows = scan_tv_shows(tv_path)
check_for_updates(shows, tv_path)
