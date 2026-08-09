#=======================================================================================#
# ChainWatcher - Emergency Version

# ChainWatcher is a tool for Torn which gives users large, hard to miss alerts when
# the faction chain timer is getting low.

# Emergency Version is a special edition that only alerts when the chain drops to 60
# seconds or below. This version is intended for those who are background/backup
# watching, or on emergency pings only. THIS IS A LAST RESORT TO SAVE THE CHAIN.

# ChainWatcher was designed with a simple philosophy: chain watching is a brutal,
# thankless, and immensely boring task. But it doesn't have to be.

# Dropping a chain is heartbreaking, so ChainWatcher helps you stay alert no matter how
# distracted you are. With full screen flashes, audible beeps, and large text warnings
# of increasing intensity, ChainWatcher is designed to get your attention every time.
# Even when you are playing fortnite, gambling, or making dinner simultaneously.

# So chain on with peace of mind knowing ChainWatcher has your back!


# Developed and maintained by EevieTheFox[3942777]


# ChainWatcher - Emergency Version v1.0
# Released 9th August 2026

# Licensed under Apache 2.0
#=======================================================================================#





#----- Imports -----#
import os
import sys
import time
import json
import signal
import threading
import winsound
import ctypes
from dataclasses import dataclass
from typing import Optional, Dict, Any
from winotify import Notification
import requests


# -------- Global Constants -------- #
API_KEY = "" #!!!!!===insert personal public only api key between quotation marks===!!!!!
API_URL = f"https://api.torn.com/v2/faction/chain?key={API_KEY}"
POLL_SECONDS = 3 # 2-3 seconds is more than enough on API V2

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
        message="Extreme Danger! Chain breaks under 1 minute!",
        bg="#F44336",  # red
        flashes=5,
        tone_hz=1320,
        tone_repeats=5,
]

# -------- Utilities -------- #

# Displays on screen message
def notify(title: str, body: str) -> None:
    toast = Notification(
        app_id="Chainwatcher",
        title=title,
        msg=body,
        duration="long"
    )
    toast.show()

# Plays sound
def play_tone(hz: int, repeats: int = 1) -> None:
    for _ in range(repeats):
        winsound.Beep(hz, 180)
        time.sleep(0.05)

# Calls API and returns current timeout in seconds left before chain breaks
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

# Creates the overlay window for the full alert
def show_overlay(bg: str, text: str, flashes: int) -> None:
    # Import here so the script still works headless (just skips overlay)
    try:
        import tkinter as tk
        from tkinter import font
    except Exception:
        return

    root = tk.Tk()
    root.title("Chainwatcher Alert")

    # Ensures the overlay is fullscreen + topmost + no decorations
    root.attributes("-fullscreen", True)
    root.attributes("-topmost", True)
    root.attributes("-alpha", 0.35)
    root.overrideredirect(True)
    root.configure(bg=bg)
    root.update_idletasks()
    root.update()

    hwnd = ctypes.windll.user32.GetParent(root.winfo_id()) or root.winfo_id()
    make_clickthrough(hwnd)

    # Close on Esc
    root.bind("<Escape>", lambda e: root.destroy())

    # Big centered label
    f = font.Font(family="Sans", size=44, weight="bold")
    label = tk.Label(root, text=text, bg=bg, fg="black", font=f)
    label.pack(expand=True)

    # Flash effect: toggle bg <-> white
    flash_state = {"i": 0, "on": False}

    #Run flash effect
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

#----- Click-Through Constants -----#
GWL_EXSTYLE = -20
WS_EX_LAYERED = 0x00080000
WS_EX_TRANSPARENT = 0x00000020

# Makes overlay "click-through" to avoid hindering an attack if another alert triggers
def make_clickthrough(hwnd):
    user32 = ctypes.windll.user32
    ex_style = user32.GetWindowLongW(hwnd, GWL_EXSTYLE)
    user32.SetWindowLongW(hwnd, GWL_EXSTYLE, ex_style | WS_EX_LAYERED | WS_EX_TRANSPARENT)

# Function that fires the actual alert, overlay, flash, and sound based on timeout threshold
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

    if hasattr(signal, "SIGTERM"):
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

#------ Exit Condition -----#
if __name__ == "__main__":
    raise SystemExit(main())
