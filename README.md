# ChainWatcher

ChainWatcher is a lightweight desktop alert tool for monitoring an active Torn faction chain. It polls the Torn API every three seconds and warns you as the chain timer approaches zero.

Alerts become progressively more urgent and include:

- A desktop notification
- A fullscreen flashing overlay
- An audible warning tone
- Color-coded urgency levels

Separate scripts are provided for Windows and Linux:

| Platform | Script |
|---|---|
| Linux | `chainwatcher_linux_v1.py` |
| Windows | `chainwatcher_windows_v1.py` |

## How It Works

ChainWatcher requests the current faction chain state from the Torn API V2 endpoint:

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

### <u>All Platforms</u>

- Python 3.9 or newer
- An internet connection
- A Torn API key - public access key, no additional permissions needed

The only shared third-party Python dependency is:

```text
requests
```

### <u>Windows</u>

The Windows script additionally requires:

```text
winotify
```

The following modules are included with standard Python on Windows and do not need to be installed separately:

- `tkinter`
- `winsound`
- `ctypes`

### <u>Linux</u>

The Linux script uses the following system utilities:

- `notify-send` for desktop notifications
- Tkinter for the fullscreen overlay
- SoX and its `play` command for audible tones

SoX is technically optional. Without it, the script falls back to the terminal bell, which may be silent depending on your terminal and desktop configuration.

## Linux Installation

Commands differ slightly by distribution.

Follow steps 1 and 2 only for your specific distribution or for running in a virtual environment.

### <u>Fedora</u>

### 1. Install/Update Python and Required Python Packages

```bash
sudo dnf install python3 python3-pip python3-tkinter libnotify sox
```

### 2. Install the Requests Dependency

```bash
python3 -m pip install --user requests
```

Once completed, skip to step 3.

### <u>Ubuntu or Debian</u>

### 1. Install/Update Python and Required Python Packages

```bash
sudo apt update
sudo apt install python3 python3-pip python3-tk libnotify-bin sox
```

### 2. Install the Requests Dependency

```bash
python3 -m pip install --user requests
```

Once completed, skip to step 3.

### <u>Arch Linux</u>

### 1. Install/Update Python and Required Python Packages

```bash
sudo pacman -S python python-pip tk libnotify sox
```

### 2. Install the Requests Dependency

```bash
python3 -m pip install --user requests
```

Once completed, skip to step 3.

### <u>Using a Virtual Environment</u>

A virtual environment avoids installing Python packages globally.

### 1. Install/Update Python and Required Python Packages

The required system packages, including Tkinter, `notify-send`, and SoX, must still be installed through your distribution's package manager. Follow Step 1 for your specific Linux distribution. Then return to this section and complete Step 2:
- [Fedora](#fedora)
- [Ubuntu or Debian](#ubuntu-or-debian)
- [Arch Linux](#arch-linux)

### 2. Create a Virtual Environment, Activate, and Install the Requests Dependency

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install requests
```

Continue to step 3.

### 3. Download the Linux Script

Place `chainwatcher_linux_v1.py` in a folder of your choice.

For example:

```text
~/Scripts/ChainWatcher
```

### 4. Rename the File
For the security of your API key, rename the file after downloading to your local machine.

Examples of good names:
- chainwatcher_private.py
- chainwatcher_personal.py
- chainwatcher_local.py
- chainwatcher_configured.py
- [your torn username]_chainwatcher.py

Examples of bad names:
- Leaving the name as is when downloaded (risk of uploading or sharing a configured file and compromising your API key)
- chainwatcher_public.py
- chainwatcher_sharable.py
- chainwatcher.py
- share_me.py
- what_is_this.py
- random_gibberish.py
- Anything ending in an extension other than .py (this will render the script unusable)

### 5. Add Your API Key

Edit `your_renamed_ChainWatcher_file.py` and insert your API key as described in [API Key Setup](#api-key-setup).

### 6. Run ChainWatcher

```bash
python3 "your_renamed_ChainWatcher_file.py"
```

Optionally you can make the script executable:

1. Make the file executable:

Without an alias:
```bash
chmod +x your_renamed_ChainWatcher_file.py
```

With an alias (for example, 'chainwatcher'):
```bash
chmod +x /path/to/your_renamed_ChainWatcher_file.py
alias chainwatcher='python3 /path/to/your_renamed_ChainWatcher_file.py'
```

2. Run the executable file:

Without an alias:
```bash
./your_renamed_ChainWatcher_file.py
```

With an alias:
```bash
chainwatcher
```

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

Place `chainwatcher_windows_v1.py` in a folder of your choice.

For example:

```text
C:\Users\YourName\ChainWatcher
```

### 3. Rename the File
For the security of your API key, rename the file after downloading to your local machine.

Examples of good names:
- chainwatcher_private.py
- chainwatcher_personal.py
- chainwatcher_local.py
- chainwatcher_configured.py
- [your torn username]_chainwatcher.py

Examples of bad names:
- Leaving the name as is when downloaded (risk of uploading or sharing a configured file and compromising your API key)
- chainwatcher_public.py
- chainwatcher_sharable.py
- chainwatcher.py
- share_me.py
- what_is_this.py
- random_gibberish.py
- Anything ending in an extension other than .py (this will render the script unusable)

### 4. Install Python Dependencies

Open PowerShell in that folder and run:

```powershell
python -m pip install requests winotify
```

Or, when using the Python launcher:

```powershell
py -m pip install requests winotify
```

### 5. Add Your API Key

Edit `your_renamed_ChainWatcher_file.py` and insert your API key as described in [API Key Setup](#api-key-setup).

### 6. Run ChainWatcher

```powershell
python .\your_renamed_ChainWatcher_file.py
```

Or:

```powershell
py .\your_renamed_ChainWatcher_file.py
```

Keep the PowerShell window open while ChainWatcher is running. Press `Ctrl+C` to stop it.

### Windows Behavior

The Windows version uses native Windows features:

- `winotify` for toast notifications
- `winsound` for alert tones
- Tkinter for the fullscreen overlay
- Windows extended window styles for click-through behavior

The fullscreen overlay is intentionally click-through. It should not intercept mouse clicks while you are attacking or typing in another application. The overlay closes automatically after flashing and can also be dismissed with `Escape` while it has keyboard focus.

## API Key Setup

Create a unique Torn API key. A public-only key is sufficient for the script's intended use.

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

## Customization

The primary settings are near the top of each script.

### Polling Frequency

```python
POLL_SECONDS = 3
```

Three seconds is frequent enough for chain monitoring without making unnecessary API requests. Lower values increase API usage and may provide little practical benefit.

Torn strictly enforces a per-key API limit of 100 requests per minute. Setting POLL_SECONDS to 1 or lower can exceed that limit. Torn may temporarily restrict the key or account, and repeated API abuse can result in longer restrictions or a ban.

If you intend to run this script on multiple devices at once, either use separate public access API keys, or set POLL_SECONDS to 5 on all devices. This will allow you to run the script on up to six devices at once.

### Alert Thresholds

Alerts are defined in the `THRESHOLDS` list:

```python
Threshold(
    timeout=150,
    title="Chainwatcher",
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

### Linux Autostart

For desktop autostart, create:

```text
~/.config/autostart/chainwatcher.desktop
```

Example contents:

```ini
[Desktop Entry]
Type=Application
Name=ChainWatcher
Exec=python3 /absolute/path/to/your_renamed_ChainWatcher_file.py
Terminal=false
X-GNOME-Autostart-enabled=true
```

Use the full absolute path to the script. If using a virtual environment, point `Exec` to that environment's Python executable:

```ini
Exec=/absolute/path/to/.venv/bin/python /absolute/path/to/your_renamed_ChainWatcher_file.py
```

Because ChainWatcher displays desktop notifications and a GUI overlay, it should be launched inside your graphical desktop session rather than as a headless system service.

### Windows Startup Folder

1. Press `Win+R`.
2. Enter:

   ```text
   shell:startup
   ```

3. Create a shortcut in the Startup folder that runs:

   ```text
   pythonw.exe C:\path\to\your_renamed_ChainWatcher_file.py
   ```

Using `pythonw.exe` runs the script without a visible console window. However, error messages will also be hidden. Test the script with regular `python.exe` first.

## Troubleshooting

### The Script Immediately Closes

Run it from PowerShell or a terminal instead of double-clicking it. This keeps errors visible:

On Linux:

```bash
python3 your_renamed_ChainWatcher_file.py
```

On Windows:

```powershell
python .\your_renamed_ChainWatcher_file.py
```

### `ModuleNotFoundError: No module named 'requests'`

Install Requests using the same Python interpreter used to run the script:

On Linux

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

On Linux:

```bash
python3 -m tkinter
```

On Windows:

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
notify-send "ChainWatcher Test" "Notification test"
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
- Temporary Torn API availability issues
- No active faction chain
- Loss of internet connectivity
- Exceeding the Torn API poll rate limitation

API and network errors are printed to the terminal. ChainWatcher waits for the next polling interval and retries automatically.

### Alerts Repeat After Every Hit

This is expected behavior. A hit refreshes the chain timer, which resets the fired threshold state. If the timer later falls through a threshold again, that threshold alerts again. In the event that the chain timer is getting low between every hit, alerts will fire between every hit.

## Linux Desktop Notes

### Notifications

Desktop notifications are sent through `notify-send` and remain visible for approximately five seconds. Whether they appear above fullscreen applications or bypass Do Not Disturb depends on the desktop environment and notification settings.

Test notifications manually with:

```bash
notify-send "ChainWatcher Test" "Notifications are working"
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

<i>Note: Linux clickthrough behavior is not being implemented since each version of each distribution requires different code.</i>

The native Windows version does implement click-through behavior.

## Security

Your Torn API key is stored as plain text inside the script. Treat the configured script as private.

Recommended precautions:

- Rename your downloaded copy to something like chainwatcher_private.py before configuring with your API key.
- Never commit a configured copy to any Git repository, public or private.
- Never upload or send the configured script to someone else.
- Keep the sharable version's `API_KEY` field blank.
- Revoke and replace the key immediately if it is exposed.
- Use only the minimum API permissions required: public access.

A useful `.gitignore` rule for a private configured copy is:

```gitignore
your_renamed_ChainWatcher_file.py
*_private.py
*_personal.py
*_local.py
*_configured.py
```

You can keep the blank `*_v1.py` versions tracked while ignoring your locally configured copies.

## Stopping ChainWatcher

When running in a terminal, press:

```text
Ctrl+C
```

If it was launched without a console, stop the associated Python process through Task Manager on Windows or your desktop's system monitor on Linux.

## License, Fair Use Policy, and Disclaimer

ChainWatcher is an independent community tool and is not affiliated with or endorsed by Torn or its developers.

ChainWatcher is licensed under the Apache License 2.0. See the LICENSE file for the full license terms.

By using this program you explicitly agree to use it responsibly and in accordance with Torn's rules and API policies.

### Disclaimer:
Reliability of alerts depends on the user's network access, Torn API response timing, operating-system notification behavior and settings, and local system performance.
ChainWatcher is designed to assist human chain watchers, not replace attentive monitoring entirely. It does not and cannot take any actions in game on the user's behalf.