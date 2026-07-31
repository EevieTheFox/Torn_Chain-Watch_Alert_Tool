#!/usr/bin/env python3

# ChainWatcher

# ChainWatcher is a tool for Torn which gives users large, hard to miss alerts when
# the faction chain timer is getting low.
#
# ChainWatcher was designed with a simple philosophy: chain watching is a brutal,
# thankless, and immensely boring task. But it doesn't have to be.
#
# Dropping a chain is heartbreaking, so ChainWatcher helps you stay alert no matter how
# distracted you are. With full screen flashes, audible beeps, and large text warnings
# of increasing intensity, ChainWatcher is designed to get your attention every time.
# Even when you are playing fortnite, gambling, or making dinner simultaneously.
#
# So chain on with peace of mind knowing ChainWatcher has your back!

# Developed and maintained by EevieTheFox[3942777]
#
# ChainWatcher v1.0 released 31 July 2026
# Licensed under Apache 2.0


#----- Imports -----#
import os
import sys
import time
import json
import signal
import subprocess
import threading
from dataclasses import dataclass
from typing import Optional, Dict, Any

import requests

# -------- Global Constants -------- #
API_KEY = "" # Insert personal public only api key between the quotation marks.
API_URL = f"https://api.torn.com/v2/faction/chain?key={API_KEY}"
POLL_SECONDS = 3  # 2-5s is a good balance

# Threshold definitions (seconds remaining)
@dataclass(frozen=True)
class Threshold:
    timeout: int
    title: str
    message: str
    bg: str
    flashes: int
    tone_hz: int
    tone_repeats: int

THRESHOLDS = [
    Threshold(
        timeout=60,
        title="Chainwatcher",
        message="Extreme Danger! Chain breaks in under 1 minute!",
        bg="#F44336",  # red
        flashes=5,
        tone_hz=1320,
        tone_repeats=5,
    ),
    Threshold(
        timeout=90,
        title="Chainwatcher",
        message="Danger! Chain breaks in 1 minute 30 seconds",
        bg="#FF9800",  # orange
        flashes=3,
        tone_hz=1100,
        tone_repeats=3,
    ),
    Threshold(
        timeout=120,
        title="Chainwatcher",
        message="Warning! Chain breaks in 2 minutes",
        bg="#FFD54A",       # yellow-ish
        flashes=2,
        tone_hz=880,
        tone_repeats=2,
    ),
    Threshold(
        timeout=150,
        title="Chainwatcher",
        message="Check chain. Chain breaks in 2 minutes 30 seconds",
        bg="#F8F0E3",  # white-ish
        flashes=1,
        tone_hz=660,
        tone_repeats=1,
    ),
]

# -------- Utilities -------- #

# Runs each command for the alert
def run(cmd: list[str]) -> None:
    subprocess.run(cmd, check=False, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

# Sends a desktop notification
def notify(title: str, body: str) -> None:
    # -u critical tends to punch through DND modes on some DEs (not all).
    run(["notify-send", "-u", "normal", "-t", "5000", title, body])
# Checks that there is a command to process
def has_cmd(name: str) -> bool:
    return subprocess.call(["bash", "-lc", f"command -v {name} >/dev/null 2>&1"]) == 0

# Plays the audio beep
def play_tone(hz: int, repeats: int = 1) -> None:
    # Preferred: sox "play" (package often named sox)
    if has_cmd("play"):
        for _ in range(repeats):
            # 0.18s beep with quick fade to reduce click
            run(["play", "-q", "-n", "synth", "0.18", "sine", str(hz), "fade", "0.01", "0.16", "0.01"])
            time.sleep(0.05)
    else:
        # Fallback: terminal bell
        for _ in range(repeats):
            sys.stdout.write("\a")
            sys.stdout.flush()
            time.sleep(0.1)

# Calls the API to check the chain timeout in seconds until chain breaks
def get_chain_state() -> Optional[tuple[int, int]]:
    """
    Returns (timeout, current) or None on request/API error.
    """
    params = {"selections": "chain", "key": API_KEY, "timestamp": int(time.time())}
    try:
        r = requests.get(API_URL, params=params, timeout=10)
        r.raise_for_status()
        data: Dict[str, Any] = r.json()

        if "error" in data:
            err = data["error"]
            print(f"[chainwatcher] Torn API error: {err}", file=sys.stderr)
            return None

        chain = data.get("chain", {})
        timeout = int(chain.get("timeout", 0) or 0)
        current = int(chain.get("current", 0) or 0)
        return (timeout, current)

    except (requests.RequestException, ValueError, json.JSONDecodeError) as e:
        print(f"[chainwatcher] Request failed: {e}", file=sys.stderr)
        return None


# -------- Overlay window (Tkinter) -------- #

# Creates overlay for full screen alert
def show_overlay(bg: str, text: str, flashes: int) -> None:
    # Import here so the script still works headless (just skips overlay)
    try:
        import tkinter as tk
        from tkinter import font
    except Exception:
        return

    root = tk.Tk()
    root.title("Chainwatcher Alert")

    # Fullscreen + topmost + no decorations
    root.attributes("-fullscreen", True)
    root.attributes("-topmost", True)
    root.attributes("-alpha", 0.35)
    root.configure(bg=bg)

    # Close on Esc or click
    root.bind("<Escape>", lambda e: root.destroy())
    root.bind("<Button-1>", lambda e: root.destroy())

    # Big centered label
    f = font.Font(family="Sans", size=44, weight="bold")
    label = tk.Label(root, text=text, bg=bg, fg="black", font=f)
    label.pack(expand=True)

    # Flash effect: toggle bg <-> white
    flash_state = {"i": 0, "on": False}

    # Runs the flash
    def do_flash():
        i = flash_state["i"]
        if i >= flashes * 2:
            # auto-close after flashing + short dwell
            root.after(800, root.destroy)
            return
        flash_state["on"] = not flash_state["on"]
        color = "white" if flash_state["on"] else bg
        root.configure(bg=color)
        label.configure(bg=color)
        flash_state["i"] += 1
        root.after(140, do_flash)

    root.after(10, do_flash)
    root.mainloop()

# Fires the entire alert including overlay, sound, notification, and flash
def fire_alert(t: Threshold) -> None:
    notify(t.title, t.message)

    # Start tone in background
    tone_thread = threading.Thread(
        target=play_tone,
        args=(t.tone_hz, t.tone_repeats),
        daemon=True
    )
    tone_thread.start()

    # Overlay runs in main thread
    show_overlay(t.bg, t.message, t.flashes)

# -------- Main loop -------- #

def main() -> int:

    # Allow Ctrl+C clean exit
    signal.signal(signal.SIGINT, lambda s, f: sys.exit(0))
    signal.signal(signal.SIGTERM, lambda s, f: sys.exit(0))

    last_timeout: Optional[int] = None
    fired = set()

    while True:
        state = get_chain_state()
        if state is None:
            time.sleep(POLL_SECONDS)
            continue

        timeout, current = state

        # No active chain countdown → don't fire alerts.
        # Also reset so next real chain starts clean.
        if timeout <= 0 or current <= 0:
            fired.clear()
            last_timeout = None
            time.sleep(POLL_SECONDS)
            continue

        # Reset fired thresholds when chain gets refreshed / timeout increases
        if last_timeout is not None and timeout > last_timeout:
            fired.clear()

        # Decide which thresholds became applicable since the last poll.
        candidates = []

        if last_timeout is None:
            # Optional: "catch-up" behavior when starting mid-chain.
            # If you DON'T want catch-up at all, leave this empty and do nothing here.
            for th in THRESHOLDS:
                if th.timeout not in fired and timeout <= th.timeout:
                    candidates.append(th)
        else:
            for th in THRESHOLDS:
                if th.timeout in fired:
                    continue
                # crossed downward past the threshold since last sample
                if last_timeout > th.timeout >= timeout:
                    candidates.append(th)

        # Fire only the MOST urgent candidate (smallest timeout).
        if candidates:
            most_urgent = min(candidates, key=lambda t: t.timeout)
            fired.add(most_urgent.timeout)
            fire_alert(most_urgent)

        last_timeout = timeout
        time.sleep(POLL_SECONDS)

# ----- Exit Condition ----- #
if __name__ == "__main__":
    raise SystemExit(main())
