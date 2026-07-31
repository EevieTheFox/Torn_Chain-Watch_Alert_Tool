# ChainWatch Alerts

ChainWatch Alerts is a lightweight desktop alert tool for monitoring an active Torn faction chain. It polls the Torn API every three seconds and warns you as the chain timer approaches zero.

Alerts become progressively more urgent and include:

- A desktop notification
- A fullscreen flashing overlay
- An audible warning tone
- Color-coded urgency levels

Separate scripts are provided for Windows and Linux:

| Platform | Script |
|---|---|
| Windows | `chainwatch_windows_sharable.py` |
| Linux | `chainwatch_alert_sharable.py` |

## How It Works

ChainWatch requests the current faction chain state from the Torn API V2 endpoint:

```text
https://api.torn.com/v2/faction/chain
```

The script checks the remaining chain timeout every three seconds. When the timer crosses a configured threshold, it displays the corresponding alert.

The default alert thresholds are:

| Time Remaining | Color | Flashes | Tone |
|---:|---|---:|---:|
| 2 minutes 30 seconds | White | 1 | 660 Hz × 1 |
| 2 minutes | Yellow | 2 | 880 Hz × 2 |
| 1 minute 30 seconds | Orange | 3 | 1100 Hz × 3 |
| Under 1 minute | Red | 5 | 1320 Hz × 5 |

Each threshold fires only once during a countdown. When someone makes a hit and the chain timer increases, the fired thresholds are reset so they can alert again during the next countdown.

If the program starts while the chain is already below one or more thresholds, it immediately fires only the most urgent applicable alert.

## Requirements

### All Platforms

- Python 3.9 or newer
- An internet connection
- A Torn API key - public access key, no additional permissions needed

The only shared third-party Python dependency is:

```text
requests
```

### Windows

The Windows script additionally requires:

```text
winotify
```

The following modules are included with standard Python on Windows and do not need to be installed separately:

- `tkinter`
- `winsound`
- `ctypes`

### Linux

The Linux script uses the following system utilities:

- `notify-send` for desktop notifications
- Tkinter for the fullscreen overlay
- SoX and its `play` command for audible tones

SoX is technically optional. Without it, the script falls back to the terminal bell, which may be silent depending on your terminal and desktop configuration.

## API Key Setup

Create a Torn API key that can access faction chain information. A public-only key is sufficient for the script's intended use.

Open the appropriate script and locate:

```python
API_KEY = ""
```

Place your API key between the quotation marks:

```python
API_KEY = "your_api_key_here"
```

Do not publish, commit, or share a copy of the script after inserting your personal API key.

The included sharable scripts intentionally leave this field blank.

## Windows Installation

### 1. Install Python

Install Python 3.9 or newer from the official Python installer or the Microsoft Store.

When using the standard installer, enable **Add Python to PATH** during installation.

Verify the installation in PowerShell:

```powershell
python --version
```

On some systems, use the Python launcher instead:

```powershell
py --version
```

### 2. Download the Windows Script

Place `chainwatch_windows_sharable.py` in a folder of your choice.

For example:

```text
C:\Users\YourName\ChainWatch
```

### 3. Install Python Dependencies

Open PowerShell in that folder and run:

```powershell
python -m pip install requests winotify
```

Or, when using the Python launcher:

```powershell
py -m pip install requests winotify
```

### 4. Add Your API Key

Edit `chainwatch_windows_sharable.py` and insert your API key as described in [API Key Setup](#api-key-setup).

### 5. Run ChainWatch

```powershell
python .\chainwatch_windows_sharable.py
```

Or:

```powershell
py .\chainwatch_windows_sharable.py
```

Keep the PowerShell window open while ChainWatch is running. Press `Ctrl+C` to stop it.

### Windows Behavior

The Windows version uses native Windows features:

- `winotify` for toast notifications
- `winsound` for alert tones
- Tkinter for the fullscreen overlay
- Windows extended window styles for click-through behavior

The fullscreen overlay is intentionally click-through. It should not intercept mouse clicks while you are attacking or typing in another application. The overlay closes automatically after flashing and can also be dismissed with `Escape` while it has keyboard focus.

## Linux Installation

Commands differ slightly by distribution.

### Fedora

```bash
sudo dnf install python3 python3-pip python3-tkinter libnotify sox
```

Install the Python dependency:

```bash
python3 -m pip install --user requests
```

### Ubuntu or Debian

```bash
sudo apt update
sudo apt install python3 python3-pip python3-tk libnotify-bin sox
```

Install the Python dependency:

```bash
python3 -m pip install --user requests
```

### Arch Linux

```bash
sudo pacman -S python python-pip tk libnotify sox
```

Install the Python dependency:

```bash
python3 -m pip install --user requests
```

### Using a Virtual Environment

A virtual environment avoids installing Python packages globally:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install requests
```

The required system packages, including Tkinter, `notify-send`, and SoX, must still be installed through your distribution's package manager.

### Run ChainWatch on Linux

Place `chainwatch_alert_sharable.py` in a folder of your choice, insert your API key, and run:

```bash
python3 chainwatch_alert_sharable.py
```

Press `Ctrl+C` to stop it.

You may optionally make the script executable:

```bash
chmod +x chainwatch_alert_sharable.py
./chainwatch_alert_sharable.py
```

## Linux Desktop Notes

### Notifications

Desktop notifications are sent through `notify-send` and remain visible for approximately five seconds. Whether they appear above fullscreen applications or bypass Do Not Disturb depends on the desktop environment and notification settings.

Test notifications manually with:

```bash
notify-send "ChainWatch Test" "Notifications are working"
```

### Audio

Test SoX audio with:

```bash
play -n synth 0.18 sine 880
```

If `play` is unavailable, confirm that SoX is installed:

```bash
command -v play
```

### Tkinter Overlay

Test Tkinter with:

```bash
python3 -m tkinter
```

A small Tk test window should appear.

### Wayland Limitation

The Linux overlay is fullscreen and topmost, but it is not click-through. Under Wayland, Tkinter does not provide a reliable cross-desktop method for making the overlay ignore mouse and keyboard input.

The Linux overlay can be dismissed by clicking it or pressing `Escape`. Because it may briefly intercept input, consider placing Torn on one monitor and allowing alerts to appear on another, or modifying the overlay behavior for your desktop environment.

The native Windows version does implement click-through behavior.

## Customization

The primary settings are near the top of each script.

### Polling Frequency

```python
POLL_SECONDS = 3
```

Three seconds is frequent enough for chain monitoring without making unnecessary API requests. Lower values increase API usage and may provide little practical benefit.

Torn strictly enforces a per key API polling limit of 100 per minute. Setting POLL_SECONDS to 1 or lower may put your Torn account at risk of being restricted or banned.

If you intend to run this script on multiple devices at once, either use separate public access API keys, or set POLL_SECONDS to 5 on all devices. This will allow you to run the script on up to six devices at once.

### Alert Thresholds

Alerts are defined in the `THRESHOLDS` list:

```python
Threshold(
    timeout=150,
    title="Chainwatch",
    message="Check chain. Chain breaks in 2 minutes 30 seconds",
    bg="#F8F0E3",
    flashes=1,
    tone_hz=660,
    tone_repeats=1,
)
```

Each field controls a part of the alert:

| Field | Purpose |
|---|---|
| `timeout` | Chain timer threshold in seconds |
| `title` | Desktop notification title |
| `message` | Notification and overlay text |
| `bg` | Overlay background color |
| `flashes` | Number of overlay flashes |
| `tone_hz` | Alert tone frequency |
| `tone_repeats` | Number of audio beeps |

Thresholds can be added, removed, or changed. Keeping them ordered from most urgent to least urgent is recommended for readability, although the script determines urgency using the numeric timeout value.

## Running Automatically

### Windows Startup Folder

1. Press `Win+R`.
2. Enter:

   ```text
   shell:startup
   ```

3. Create a shortcut in the Startup folder that runs:

   ```text
   pythonw.exe C:\path\to\chainwatch_windows_sharable.py
   ```

Using `pythonw.exe` runs the script without a visible console window. However, error messages will also be hidden. Test the script with regular `python.exe` first.

### Linux Autostart

For desktop autostart, create:

```text
~/.config/autostart/chainwatch.desktop
```

Example contents:

```ini
[Desktop Entry]
Type=Application
Name=ChainWatch Alerts
Exec=python3 /absolute/path/to/chainwatch_alert_sharable.py
Terminal=false
X-GNOME-Autostart-enabled=true
```

Use the full absolute path to the script. If using a virtual environment, point `Exec` to that environment's Python executable:

```ini
Exec=/absolute/path/to/.venv/bin/python /absolute/path/to/chainwatch_alert_sharable.py
```

Because ChainWatch displays desktop notifications and a GUI overlay, it should be launched inside your graphical desktop session rather than as a headless system service.

## Troubleshooting

### The Script Immediately Closes

Run it from PowerShell or a terminal instead of double-clicking it. This keeps errors visible:

```bash
python3 chainwatch_alert_sharable.py
```

or on Windows:

```powershell
python .\chainwatch_windows_sharable.py
```

### `ModuleNotFoundError: No module named 'requests'`

Install Requests using the same Python interpreter used to run the script:

```bash
python3 -m pip install requests
```

On Windows:

```powershell
python -m pip install requests
```

### `ModuleNotFoundError: No module named 'winotify'`

The Windows version requires Winotify:

```powershell
python -m pip install winotify
```

### No Fullscreen Overlay Appears

Confirm that Tkinter is installed and working.

Linux:

```bash
python3 -m tkinter
```

Windows:

```powershell
python -m tkinter
```

Some desktop environments or window managers may restrict fullscreen or always-on-top windows.

### No Desktop Notification Appears on Linux

Confirm that `notify-send` is installed:

```bash
command -v notify-send
```

Then test it manually:

```bash
notify-send "ChainWatch Test" "Notification test"
```

### No Sound on Linux

Install SoX and confirm that `play` exists:

```bash
command -v play
```

Also verify that the active audio output is not muted and that SoX is using the expected audio backend.

### Torn API Error

Common causes include:

- A missing or invalid API key
- A key without the required faction access
- Temporary Torn API availability issues
- No active faction chain
- Loss of internet connectivity

API and network errors are printed to the terminal. ChainWatch waits for the next polling interval and retries automatically.

### Alerts Repeat After Every Hit

This is expected. A hit refreshes the chain timer, which resets the fired threshold state. If the timer later falls through a threshold again, that threshold alerts again.

## Security

Your Torn API key is stored as plain text inside the script. Treat the configured script as private.

Recommended precautions:

- Never commit a configured copy to a public Git repository.
- Never upload or send the configured script to someone else.
- Keep the sharable version's `API_KEY` field blank.
- Revoke and replace the key immediately if it is exposed.
- Use only the minimum API permissions required.

A useful `.gitignore` rule for a private configured copy is:

```gitignore
chainwatch_windows.py
chainwatch_alert.py
```

You can keep the blank `*_sharable.py` versions tracked while ignoring your locally configured copies.

## Stopping ChainWatch

When running in a terminal, press:

```text
Ctrl+C
```

If it was launched without a console, stop the associated Python process through Task Manager on Windows or your desktop's system monitor on Linux.

## License and Disclaimer

ChainWatch Alerts is an independent community tool and is not affiliated with or endorsed by Torn or its developers.

Use it responsibly and in accordance with Torn's rules and API policies. Alerts depend on network access, API response timing, operating-system notification behavior, and local system performance. ChainWatch should assist human chain watchers, not replace attentive monitoring entirely.
