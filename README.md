# dvdrip

Rip DVDs quickly and easily from the command line.

## Features

- **High-quality encoding** with x265 (HEVC) video and preserved audio tracks
- **Auto-detection** of optical drives - no need to specify input device
- **TMDb metadata integration** for automatic file naming based on movie/TV show info
- **Multiple output modes**: single file, per-title, or per-chapter
- **Join multiple titles** into a single file (great for special features discs)
- **Subtitle control** - include all, or exclude with `--no-subtitles`
- **Scan mode** to preview disc contents before ripping

## Dependencies

- [Python 3](https://www.python.org/)
- [HandBrakeCLI](https://handbrake.fr/)
- [FFmpeg](https://ffmpeg.org/) (required for `--join` feature)
- [tmdbsimple](https://github.com/celiao/tmdbsimple) (optional, for metadata lookup)

### Installation

```bash
# Ubuntu/Debian
sudo apt install handbrake-cli ffmpeg

# Install optional TMDb support
pip install tmdbsimple
```

## Quick Start

### 1. Scan the disc first

```bash
# Auto-detects optical drive
python3 dvdrip.py --scan

# Or specify the device
python3 dvdrip.py --scan -i /dev/sr0
```

This shows you the disc structure including titles, chapters, audio tracks, and subtitles.

### 2. Rip the disc

```bash
# Basic rip - all titles
python3 dvdrip.py -o MovieName

# Rip specific titles only
python3 dvdrip.py -t 1,2,3 -o MovieName

# Rip main feature only
python3 dvdrip.py --main-feature -o MovieName
```

## Common Use Cases

### Ripping a Movie

```bash
python3 dvdrip.py --main-feature -o "The Matrix"
```

### Ripping a TV Show (split by chapter)

When episodes are stored as chapters within a single title:

```bash
python3 dvdrip.py -c -o "Breaking Bad S01"
```

### Ripping Special Features and Joining Them

```bash
# Rip titles 2-8 and join them into one file
python3 dvdrip.py -t 2-8 --join -o "Special Features"

# Join only specific titles
python3 dvdrip.py --join-titles 2,3,5 -o "Behind The Scenes"

# Keep individual files after joining
python3 dvdrip.py -t 2-8 --join --keep-files -o "Special Features"
```

### Using TMDb Metadata for Naming

```bash
# Search TMDb and use metadata for file naming
python3 dvdrip.py --title-search "The Matrix" --year 1999 -o /output/path

# For TV shows
python3 dvdrip.py --title-search "Breaking Bad" --tv -o /output/path

# Skip metadata lookup
python3 dvdrip.py --no-metadata -o MovieName
```

To use TMDb features, set up your API key:
```bash
# Option 1: Environment variable
export TMDB_API_KEY="your_api_key_here"

# Option 2: Config file
echo "your_api_key_here" > ~/.tmdb_api_key
```

### Excluding Subtitles

```bash
python3 dvdrip.py --no-subtitles -o MovieName
```

## Command Reference

| Option | Description |
|--------|-------------|
| `-i, --input` | Input device/path (auto-detected if omitted) |
| `-o, --output` | Output filename/directory (required for ripping) |
| `--scan` | Scan disc and display contents without ripping |
| `-t, --titles` | Comma-separated title numbers or ranges (e.g., `1,2,3` or `1-5`) |
| `-c, --chapter_split` | Split each chapter into a separate file |
| `--main-feature` | Rip only the longest title (main feature) |
| `--join` | Join all ripped titles into a single MP4 file |
| `--join-titles` | Join specific titles (e.g., `1,2,3`) |
| `--keep-files` | Keep individual files after joining |
| `--no-subtitles` | Exclude all subtitle tracks |
| `--title-search` | Search TMDb for metadata |
| `--year` | Release year (helps narrow TMDb search) |
| `--tv` | Search for TV show instead of movie |
| `--no-metadata` | Skip TMDb metadata lookup |
| `-v, --verbose` | Show detailed output |
| `-n, --dry-run` | Preview what would happen without writing files |
| `--mount-timeout` | Seconds to wait for disc to mount (default: 15) |

## Output

- **Single title**: Creates `OutputName.mp4`
- **Multiple titles**: Creates `OutputName/` directory with `Title01.mp4`, `Title02.mp4`, etc.
- **Chapter split**: Creates `Title01_01.mp4`, `Title01_02.mp4`, etc.
- **Joined output**: Creates `OutputName - Joined.mp4` (or metadata-based name)

## Encoding Settings

- **Video**: x265 (HEVC) at CRF 16 with detelecine, deinterlace, and light denoise
- **Audio**: Copied from source (preserves all audio tracks)
- **Container**: MP4 with optimization for streaming

## Troubleshooting

### Drive not detected
```bash
# List available optical drives
ls /dev/sr*

# Specify device manually
python3 dvdrip.py -i /dev/sr0 --scan
```

### Permission issues
```bash
# Add yourself to the cdrom group
sudo usermod -aG cdrom $USER
# Log out and back in
```

### Disc won't mount
The script will attempt to mount read-only automatically. If this fails:
```bash
sudo mount -o ro /dev/sr0 /mnt/dvd
python3 dvdrip.py -i /mnt/dvd -o OutputName
```

## Notes

- Tested on Linux and macOS with Python 3
- The `--join` feature requires FFmpeg and uses x265 re-encoding to handle potential dimension/format differences between titles
- Disc is automatically ejected after ripping completes
