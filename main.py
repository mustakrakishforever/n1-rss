import feedparser
import time
import requests
import os
from datetime import datetime
from colorama import init, Fore, Style

init(autoreset=True)  # ensures colors reset after each print

# ---------------- Configuration ---------------- #
WEBHOOK_NEWS = "INPUT_YOUR_WEBHOOK_HERE"
N1_FEED = "https://n1info.rs/feed/"

CHECK_INTERVAL = 60  # check every 60 seconds (1 minute)

SENT_LINKS_FILE = "sent_links.txt"
MONITOR_LOG_FILE = "monitor_log.txt"
ERROR_LOG_FILE = "error_log.txt"

# ---------------- Logging ----------------------- #
def log_monitor(message):
    timestamp = datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
    print(Fore.CYAN + f"[INFO] {timestamp} {message}")
    try:
        with open(MONITOR_LOG_FILE, "a", encoding="utf-8") as f:
            f.write(f"[MONITOR] {timestamp} {message}\n")
    except Exception as e:
        log_error(f"Failed to write monitor log: {e}")

def log_error(message):
    timestamp = datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
    print(Fore.RED + f"[ERROR] {timestamp} {message}")
    try:
        with open(ERROR_LOG_FILE, "a", encoding="utf-8") as f:
            f.write(f"[ERROR] {timestamp} {message}\n")
    except:
        pass  # avoid crash if error log fails

# ---------------- Sent links ------------------- #
def load_sent_links():
    if os.path.exists(SENT_LINKS_FILE):
        try:
            with open(SENT_LINKS_FILE, "r", encoding="utf-8") as f:
                return set(line.strip() for line in f if line.strip())
        except Exception as e:
            log_error(f"Failed to load sent links: {e}")
    return set()

def save_sent_link(link):
    try:
        with open(SENT_LINKS_FILE, "a", encoding="utf-8") as f:
            f.write(link + "\n")
    except Exception as e:
        log_error(f"Failed to save sent link: {e}")

# ---------------- Discord ---------------------- #
def send_to_discord(message):
    try:
        payload = {"content": message}
        response = requests.post(WEBHOOK_NEWS, json=payload, timeout=10)
        if response.status_code not in (200, 204):
            log_error(f"Discord returned status {response.status_code}: {response.text}")
        else:
            print(Fore.GREEN + f"[SENT] {message[:60]}...")
    except Exception as e:
        log_error(f"Failed to send to Discord: {e}")

# ---------------- N1 RSS ----------------------- #
def check_n1(sent_links):
    log_monitor("Checking N1 RSS feed...")
    try:
        feed = feedparser.parse(N1_FEED)
        new_found = False
        for entry in feed.entries[:10]:  # check latest 10
            if entry.link not in sent_links:
                sent_links.add(entry.link)
                save_sent_link(entry.link)
                msg = f"**N1 News**: {entry.title}\n{entry.link}"
                send_to_discord(msg)
                print(Fore.YELLOW + f"[NEW] N1 Article: {entry.title}")
                new_found = True
        if not new_found:
            print(Fore.BLUE + "[INFO] No new N1 news.")
    except Exception as e:
        log_error(f"Failed to fetch or parse N1 RSS: {e}")

# ---------------- Main ------------------------ #
def main():
    log_monitor("Script started. Monitoring N1 news...")
    sent_links = load_sent_links()

    while True:
        check_n1(sent_links)
        time.sleep(CHECK_INTERVAL)  # use configurable interval

if __name__ == "__main__":
    main()
