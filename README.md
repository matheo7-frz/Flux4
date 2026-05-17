# PS4 Emu Launcher

A desktop launcher and frontend for the [shadPS4](https://github.com/shadps4-emu/shadPS4) PS4 emulator, built with Python and PySide6.

## Features

- **Firmware Management**: Import and validate PS4 firmware files (PS4UPDATE.PUP)
- **Game Library**: Browse, organize, and launch your PS4 game collection with cover art
- **shadPS4 Integration**: Auto-detect or manually configure shadPS4, launch games directly
- **PS4-Styled UI**: Dark blue theme inspired by the PlayStation 4 interface
- **Settings Panel**: Configure GPU backend, resolution, fullscreen mode, and more
- **Cross-Platform**: Works on Windows, Linux, and macOS

## Screenshots

The launcher features a modern PS4-inspired dark theme with:
- Dashboard with status overview
- Firmware import and validation
- Game library grid with covers
- Full settings panel

## Installation

### Prerequisites

- Python 3.10 or higher
- pip (Python package manager)

### Install from source

```bash
# Clone the repository
git clone https://github.com/your-username/ps4-emu-launcher.git
cd ps4-emu-launcher

# Install dependencies
pip install -r requirements.txt

# Run the launcher
python main.py
```

### Install as package

```bash
pip install .
ps4-emu-launcher
```

## Setup Guide

### 1. Install shadPS4

The launcher requires [shadPS4](https://github.com/shadps4-emu/shadPS4/releases) to be installed on your system.

- Download the latest release from GitHub
- Extract it to a known location
- The launcher will try to auto-detect it, or you can set the path manually in Settings

### 2. Import PS4 Firmware

PS4 games require the console's firmware to run:

1. Go to the **Firmware** tab
2. Click **Import Firmware (.PUP)**
3. Select your `PS4UPDATE.PUP` file
4. The launcher validates and installs it automatically

### 3. Add Games

Add your PS4 game dumps to the library:

1. Go to the **Library** tab
2. Click **Add Game Folder** to add individual games
3. Or click **Scan Directory** to find all games in a folder
4. Double-click a game to launch it

### Game Folder Structure

A valid PS4 game dump should contain:
```
GameFolder/
  eboot.bin          (main executable)
  sce_sys/
    param.sfo        (game metadata)
    icon0.png        (game icon/cover)
```

## Configuration

Settings are stored in `~/.ps4-emu-launcher/config.json` and include:

| Setting | Description | Default |
|---------|-------------|---------|
| GPU Backend | Vulkan or OpenGL | Vulkan |
| Resolution | Render resolution | 1920x1080 |
| Fullscreen | Launch in fullscreen | Off |
| Log Level | Emulator log verbosity | Info |

## Project Structure

```
ps4-emu-launcher/
├── main.py                    # Entry point
├── requirements.txt           # Python dependencies
├── setup.py                   # Package installation
├── src/
│   ├── __init__.py
│   ├── main_window.py         # Main window with sidebar
│   ├── styles.py              # PS4-themed stylesheets
│   ├── core/
│   │   ├── config.py          # Configuration management
│   │   ├── firmware_manager.py # Firmware validation & import
│   │   ├── emulator_manager.py # shadPS4 integration
│   │   └── game_library.py    # Game scanning & catalog
│   └── pages/
│       ├── home.py            # Dashboard page
│       ├── firmware.py        # Firmware management page
│       ├── library.py         # Game library page
│       └── settings.py        # Settings page
```

## License

MIT License
