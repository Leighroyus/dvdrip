#!/usr/bin/env python3
# coding=utf-8

"""
Rip DVDs quickly and easily from the commandline.

Features:
  - With minimal configuration:
    - Encodes videos in mp4 files with h.264 video and aac audio.
      (compatible with a wide variety of media players without
      additional transcoding, including PS3, Roku, and most smart
      phones, smart TVs and tablets).
    - Preserves all audio tracks, all subtitle tracks, and chapter
      markers.
    - Intelligently chooses output filename based on a provided prefix.
    - Generates one video file per DVD title, or optionally one per
      chapter.
  - Easy to read "scan" mode tells you what you need need to know about
    a disk to decide on how to rip it.

Why I wrote this:
  This script exists because I wanted a simple way to back up DVDs with
  reasonably good compression and quality settings, and in a format I could
  play on the various media players I own including PS3, Roku, smart TVs,
  smartphones and tablets. Using mp4 files with h.264 video and aac audio seems
  to be the best fit for these constraints.

  I also wanted it to preserve as much as possible: chapter markers, subtitles,
  and (most of all) *all* of the audio tracks. My kids have a number of
  bilingual DVDs, and I wanted to back these up so they don't have to handle
  the physical disks, but can still watch their shows in either language. For
  some reason HandBrakeCLI doesn't have a simple “encode all audio tracks”
  option.

  This script also tries to be smart about the output name. You just tell it
  the pathname prefix, eg: "/tmp/AwesomeVideo", and it'll decide whether to
  produce a single file, "/tmp/AwesomeVideo.mp4", or a directory
  "/tmp/AwesomeVideo/" which will contain separate files for each title,
  depending on whether you're ripping a single title or multiple titles.


Using it, Step 1:

  The first step is to scan your DVD and decide whether or not you want
  to split chapters. Here's an example of a disc with 6 episodes of a TV
  show, plus a "bump", all stored as a single title.

    $ dvdrip --scan -i /dev/cdrom
    Reading from '/media/EXAMPLE1'
    Title   1/  1: 02:25:33  720×576  4:3   25 fps
      audio   1: Chinese (5.1ch)  [48000Hz, 448000bps]
      chapter   1: 00:24:15 ◖■■■■■■■■■‥‥‥‥‥‥‥‥‥‥‥‥‥‥‥‥‥‥‥‥‥‥‥‥‥‥‥‥‥‥‥‥‥‥‥‥‥‥‥‥‥◗
      chapter   2: 00:24:15 ◖‥‥‥‥‥‥‥‥■■■■■■■■■‥‥‥‥‥‥‥‥‥‥‥‥‥‥‥‥‥‥‥‥‥‥‥‥‥‥‥‥‥‥‥‥‥◗
      chapter   3: 00:24:14 ◖‥‥‥‥‥‥‥‥‥‥‥‥‥‥‥‥■■■■■■■■■‥‥‥‥‥‥‥‥‥‥‥‥‥‥‥‥‥‥‥‥‥‥‥‥‥◗
      chapter   4: 00:24:15 ◖‥‥‥‥‥‥‥‥‥‥‥‥‥‥‥‥‥‥‥‥‥‥‥‥■■■■■■■■■■‥‥‥‥‥‥‥‥‥‥‥‥‥‥‥‥◗
      chapter   5: 00:24:15 ◖‥‥‥‥‥‥‥‥‥‥‥‥‥‥‥‥‥‥‥‥‥‥‥‥‥‥‥‥‥‥‥‥‥■■■■■■■■■‥‥‥‥‥‥‥‥◗
      chapter   6: 00:24:14 ◖‥‥‥‥‥‥‥‥‥‥‥‥‥‥‥‥‥‥‥‥‥‥‥‥‥‥‥‥‥‥‥‥‥‥‥‥‥‥‥‥‥■■■■■■■■■◗
      chapter   7: 00:00:05 ◖‥‥‥‥‥‥‥‥‥‥‥‥‥‥‥‥‥‥‥‥‥‥‥‥‥‥‥‥‥‥‥‥‥‥‥‥‥‥‥‥‥‥‥‥‥‥‥‥‥■◗

  Knowing that this is 6 episodes of a TV show, I'd choose to split the
  chapters. If it was a movie with 6 chapters, I would choose to not
  split it.

  Here's a disc with 3 2-segment episodes of a show, plus two "bumps",
  stored as 8 titles.

    Reading from '/media/EXAMPLE2'
    Title   1/  5: 00:23:22  720×576  4:3   25 fps
      audio   1: Chinese (2.0ch)  [48000Hz, 192000bps]
      audio   2: English (2.0ch)  [48000Hz, 192000bps]
      sub   1: English  [(Bitmap)(VOBSUB)]
      chapter   1: 00:11:41 ◖■■■■■■■■■■■■■■■■■■■■■■■■■‥‥‥‥‥‥‥‥‥‥‥‥‥‥‥‥‥‥‥‥‥‥‥‥‥◗
      chapter   2: 00:11:41 ◖‥‥‥‥‥‥‥‥‥‥‥‥‥‥‥‥‥‥‥‥‥‥‥‥■■■■■■■■■■■■■■■■■■■■■■■■■■◗

    Title   2/  5: 00:22:40  720×576  4:3   25 fps
      audio   1: Chinese (2.0ch)  [48000Hz, 192000bps]
      audio   2: English (2.0ch)  [48000Hz, 192000bps]
      sub   1: English  [(Bitmap)(VOBSUB)]
      chapter   1: 00:11:13 ◖■■■■■■■■■■■■■■■■■■■■■■■■‥‥‥‥‥‥‥‥‥‥‥‥‥‥‥‥‥‥‥‥‥‥‥‥◗
      chapter   2: 00:11:28 ◖‥‥‥‥‥‥‥‥‥‥‥‥‥‥‥‥‥‥‥‥‥‥‥■■■■■■■■■■■■■■■■■■■■■■■■■◗

    Title   3/  5: 00:22:55  720×576  4:3   25 fps
      audio   1: Chinese (2.0ch)  [48000Hz, 192000bps]
      audio   2: English (2.0ch)  [48000Hz, 192000bps]
      sub   1: English  [(Bitmap)(VOBSUB)]
      chapter   1: 00:15:56 ◖■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■‥‥‥‥‥‥‥‥‥‥‥‥‥‥‥◗
      chapter   2: 00:06:59 ◖‥‥‥‥‥‥‥‥‥‥‥‥‥‥‥‥‥‥‥‥‥‥‥‥‥‥‥‥‥‥‥‥‥■■■■■■■■■■■■■■■■◗

    Title   4/  5: 00:00:08  720×576  4:3   25 fps
      audio   1: English (2.0ch)  [None]
      chapter   1: 00:00:08 ◖◗

    Title   5/  5: 00:00:05  720×576  4:3   25 fps
      chapter   1: 00:00:05 ◖◗

  Given that these are 2-segment episodes (it's pretty common for kids'
  shows to have two segments per episode -- essentially 2 "mini-episodes") you
  can choose whether to do the default one video per title (episodes) or
  split by chapter (segments / mini-episodes).

Using it, Step 2:

  If you've decided to split by chapter, execute:

    dvdrip.py -c -i /dev/cdrom -o Output_Name

  Otherwise, leave out the -c flag.

  If there is only one video being ripped, it will be named Output_Name.mp4. If
  there are multiple files, they will be placed in a new directory called
  Output_Name.

Limitations:

  This script has been tested on both Linux and Mac OS X with Python 3,
  HandBrakeCLI and VLC installed (and also MacPorts in the case of OS X).
"""

# TODO: Detect if HandBrakeCLI is burning in vobsubs.
# TODO: Support half-open ranges in title specs (DVD title numbers range from
# 1-99)
# TODO: Deal with failed scan of first title better.

import ctypes
import argparse
import stat
import sys
import time
import glob
import os
import re
import subprocess
import tempfile

try:
    import tmdbsimple as tmdb
    TMDB_AVAILABLE = True
except ImportError:
    TMDB_AVAILABLE = False

from pprint import pprint
from collections import namedtuple
from math import gcd


class UserError(Exception):
    def __init__(self, message):
        self.message = message

CHAR_ENCODING = 'UTF-8'

def is_block_device(path: str) -> bool:
    try:
        st = os.stat(path)
        return stat.S_ISBLK(st.st_mode)
    except FileNotFoundError:
        return False

def find_mountpoint(devnode: str) -> str | None:
    """
    Return mountpoint for devnode if mounted, else None.
    """
    p = subprocess.run(["findmnt", "-n", "-o", "TARGET", "--source", devnode],
                       text=True, capture_output=True, check=False)
    mp = p.stdout.strip()
    return mp if p.returncode == 0 and mp else None

def mount_device_readonly(devnode: str, timeout_sec: int = 20) -> str:
    """
    Mount devnode read-only to a temp dir and return that mount dir.
    Retries for up to timeout_sec because optical drives often need time
    to spin up / re-enumerate after USB resets.
    """
    mount_dir = tempfile.mkdtemp(prefix="dvdrip_mount_")
    deadline = time.time() + float(timeout_sec)
    last_err = ""

    while time.time() < deadline:
        p = subprocess.run(
            ["sudo", "mount", "-o", "ro", devnode, mount_dir],
            text=True, capture_output=True, check=False
        )
        if p.returncode == 0:
            return mount_dir

        last_err = (p.stderr.strip() or p.stdout.strip() or "")
        low = last_err.lower()

        transient = (
            "no medium found" in low or
            "not ready" in low or
            "can't read superblock" in low or
            "wrong fs type" in low
        )
        if transient:
            time.sleep(1.0)
            continue

        break

    try:
        os.rmdir(mount_dir)
    except OSError:
        pass

    raise RuntimeError(f"Failed to mount {devnode} read-only: {last_err}")

def unmount(mount_dir: str) -> None:
    subprocess.run(["sudo", "umount", mount_dir], check=False)
    try:
        os.rmdir(mount_dir)
    except OSError:
        pass

def _udev_props(devnode: str) -> dict:
    # udevadm info --query=property --name=/dev/sr1
    p = subprocess.run(
        ["udevadm", "info", "--query=property", f"--name={devnode}"],
        text=True, capture_output=True, check=False
    )
    props = {}
    if p.returncode != 0:
        return props
    for line in p.stdout.splitlines():
        if "=" in line:
            k, v = line.split("=", 1)
            props[k.strip()] = v.strip()
    return props

def _device_has_media(devnode: str) -> bool:
    """
    Best-effort check that a disc is present and readable.

    sysfs media != none is helpful but not sufficient on flaky USB drives,
    so we also probe blkid which tends to fail when the disc isn't ready.
    """
    name = os.path.basename(devnode)  # sr0
    sys_media = f"/sys/class/block/{name}/device/media"
    try:
        with open(sys_media, "r") as f:
            media = f.read().strip().lower()
        if media in ("", "none"):
            return False
    except FileNotFoundError:
        pass  # sysfs not available on this system, fall through to blkid

    # Probe for a readable filesystem/descriptor. On DVD-Video (UDF/ISO),
    # blkid usually returns something when the disc is actually readable.
    p = subprocess.run(["blkid", devnode], text=True, capture_output=True, check=False)
    return p.returncode == 0

def find_optical_drive_device(prefer_with_media: bool = True) -> str:
    candidates = sorted(glob.glob("/dev/sr*"))
    scored = []

    for dev in candidates:
        props = _udev_props(dev)
        if props.get("ID_CDROM") != "1":
            continue

        has_media = _device_has_media(dev)

        # If we prefer media, skip drives that don't currently report readable media.
        if prefer_with_media and not has_media:
            continue

        score = 0
        if has_media:
            score += 10

        # Prefer the one that udev thinks is /dev/cdrom if present
        if "/dev/cdrom" in props.get("DEVLINKS", ""):
            score += 2

        scored.append((score, dev))

    if not scored:
        if prefer_with_media:
            raise RuntimeError(
                "No optical drive with readable media found under /dev/sr*. "
                "Check the disc is inserted and the drive is stable."
            )
        raise RuntimeError("No optical drive found under /dev/sr* (ID_CDROM=1).")

    scored.sort(reverse=True)
    return scored[0][1]

def check_err(*popenargs, **kwargs):
    process = subprocess.Popen(stderr=subprocess.PIPE, *popenargs, **kwargs)
    _, stderr = process.communicate()
    retcode = process.poll()
    if retcode:
        cmd = kwargs.get("args")
        if cmd is None:
            cmd = popenargs[0]
        raise subprocess.CalledProcessError(retcode, cmd, output=stderr)
    return stderr.decode(CHAR_ENCODING, 'replace')

def check_output(*args, **kwargs):
    s = subprocess.check_output(*args, **kwargs).decode(CHAR_ENCODING)
    return s.replace(os.linesep, '\n')

HANDBRAKE = 'HandBrakeCLI'

TITLE_COUNT_REGEXES = [
        re.compile(r'^Scanning title \d+ of (\d+)\.\.\.$'),
        re.compile(r'^\[\d\d:\d\d:\d\d] scan: DVD has (\d+) title\(s\)$'),
]

def FindTitleCount(scan, verbose):
    for regex in TITLE_COUNT_REGEXES:
        for line in scan:
            m = regex.match(line)
            if m: break
        if m:
            return int(m.group(1))
    if verbose:
        for line in scan:
            print(line)
    raise AssertionError("Can't find TITLE_COUNT_REGEX in scan")


STRUCTURED_LINE_RE = re.compile(r'( *)\+ (([a-z0-9 ]+):)?(.*)')

def ExtractTitleScan(scan):
    result = []
    in_title_scan = False
    for line in scan:
        if not in_title_scan:
            if line.startswith('+'):
                in_title_scan = True
        if in_title_scan:
            m = STRUCTURED_LINE_RE.match(line)
            if m:
                result.append(line)
            else:
                break
    return tuple(result)


TRACK_VALUE_RE = re.compile(r'(\d+), (.*)')

def MassageTrackData(node, key):
    if key in node:
        track_data = node[key]
        if type(track_data) is list:
            new_track_data = {}
            for track in track_data:
                k, v = TRACK_VALUE_RE.match(track).groups()
                new_track_data[k] = v
            node[key] = new_track_data

def ParseTitleScan(scan):
    pos, result = ParseTitleScanHelper(scan, pos=0, indent=0)

    # HandBrakeCLI inexplicably uses a comma instead of a colon to
    # separate the track identifier from the track data in the "audio
    # tracks" and "subtitle tracks" nodes, so we "massage" these parsed
    # nodes to get a consistent parsed reperesentation.
    for value in result.values():
        MassageTrackData(value, 'audio tracks')
        MassageTrackData(value, 'subtitle tracks')
    return result

def ParseTitleScanHelper(scan, pos, indent):
    result = {}
    cruft = []
    while True:
        pos, node = ParseNode(scan, pos=pos, indent=indent)
        if node:
            if type(node) is tuple:
                k, v = node
                result[k] = v
            else:
                cruft.append(node)
                result[None] = cruft
        else:
            break
    if len(result) == 1 and None in result:
        result = result[None]
    return pos, result

def ParseNode(scan, pos, indent):
    if pos >= len(scan):
        return pos, None
    line = scan[pos]
    spaces, colon, name, value = STRUCTURED_LINE_RE.match(line).groups()
    spaces = len(spaces) / 2
    if spaces < indent:
        return pos, None
    assert spaces == indent, '%d <> %r' % (indent, line)
    pos += 1
    if colon:
        if value:
            node = (name, value)
        else:
            pos, children = ParseTitleScanHelper(scan, pos, indent + 1)
            node = (name, children)
    else:
        node = value
    return pos, node

def only(iterable):
    """
    Return the one and only element in iterable.

    Raises an ValueError if iterable does not have exactly one item.
    """
    result, = iterable
    return result

Title = namedtuple('Title', ['number', 'info'])
Task = namedtuple('Task', ['title', 'chapter'])

TOTAL_EJECT_SECONDS = 5
EJECT_ATTEMPTS_PER_SECOND = 10

class DVD:
    def __init__(self, mountpoint, verbose, mount_timeout=0):
        if stat.S_ISBLK(os.stat(mountpoint).st_mode):
            mountpoint = FindMountPoint(mountpoint, mount_timeout)
        if not os.path.isdir(mountpoint):
            raise UserError('%r is not a directory' % mountpoint)
        self.mountpoint = mountpoint
        self.verbose = verbose

    def RipTitle(self, task, output, dry_run, verbose, no_subtitles=False):
        if verbose:
            print('Title Scan:')
            pprint(task.title.info)
            print('-' * 78)

        audio_tracks = list(task.title.info['audio tracks'].keys())
        subtitles = list(task.title.info['subtitle tracks'].keys())

        args = [
            HANDBRAKE,
            '--input', self.mountpoint,
            '--title', str(task.title.number),

            '--encoder', 'x265',
            '--quality', '16',

            # Use -E copy instead of --audio X --aencoder copy
            # This matches manual encoding and produces better quality
            '-E', 'copy',

            '--format', 'mp4',
            '--optimize',

            '--detelecine',
            '--deinterlace',
            '--nlmeans=light',  # CRITICAL: Must use = not space for correct quality!
        ]

        if task.chapter is not None:
            args += ['--chapters', str(task.chapter)]

        if no_subtitles:
            args += ['--subtitle', 'none']
        elif subtitles:
            args += ['--subtitle', ','.join(subtitles)]

        args += ['--output', output]

        if verbose:
            print(' '.join(('\n  ' + a)
                if a.startswith('-') else a for a in args))
            print('-' * 78)
        if not dry_run:
            if verbose:
                subprocess.call(args)
            else:
                check_err(args)

    def ScanTitle(self, i):
        for line in check_err([
            HANDBRAKE,
            #'--no-dvdnav', # TODO: turn this on as a fallback
            '--scan',
            '--title', str(i),
            '-i',
            self.mountpoint], stdout=subprocess.PIPE).split(os.linesep):
                if self.verbose:
                        print('< %s' % line.rstrip())
                yield line

    def ScanTitles(self, title_numbers, verbose):
        """
        Returns an iterable of parsed titles.
        """
        first = title_numbers[0] if title_numbers else 1
        raw_scan = tuple(self.ScanTitle(first))
        title_count = FindTitleCount(raw_scan, verbose)
        print('Disc claims to have %d titles.' % title_count)
        title_name, title_info = only(
                ParseTitleScan(ExtractTitleScan(raw_scan)).items())
        del raw_scan

        def MakeTitle(name, number, info):
            assert ('title %d' % number) == name
            info['duration'] = ExtractDuration('duration ' + info['duration'])
            return Title(number, info)

        yield MakeTitle(title_name, first, title_info)

        to_scan = [x for x in range(1, title_count + 1)
                   if x != first
                        and ((not title_numbers)
                             or x in title_numbers)]
        for i in to_scan:
                try:
                    scan = ExtractTitleScan(self.ScanTitle(i))
                except subprocess.CalledProcessError as exc:
                    warn("Cannot scan title %d." % i)
                else:
                    title_info_names = ParseTitleScan(scan).items()
                    if title_info_names:
                        title_name, title_info = only(title_info_names)
                        yield MakeTitle(title_name, i, title_info)
                    else:
                        warn("Cannot parse scan of title %d." % i)

    def Eject(self):
        if os.name == 'nt':
            if len(self.mountpoint) < 4 and self.mountpoint[1] == ':':
                # mountpoint is only a drive letter like "F:" or "F:\" not a subdirectory
                drive_letter = self.mountpoint[0]
                ctypes.windll.WINMM.mciSendStringW("open %s: type CDAudio alias %s_drive" % (drive_letter, drive_letter), None, 0, None)
                ctypes.windll.WINMM.mciSendStringW("set %s_drive door open" % drive_letter, None, 0, None)
            return

        # TODO: this should really be a while loop that terminates once a
        # deadline is met.
        for i in range(TOTAL_EJECT_SECONDS * EJECT_ATTEMPTS_PER_SECOND):
            if not subprocess.call(['eject', self.mountpoint]):
                return
            time.sleep(1.0 / EJECT_ATTEMPTS_PER_SECOND)

def ParseDuration(s):
    result = 0
    for field in s.strip().split(':'):
        result *= 60
        result += int(field)
    return result

def FindMountPoint(dev, timeout):
    regex = re.compile(r'^' + re.escape(os.path.realpath(dev)) + r'\b')

    now = time.time()
    end_time = now + timeout
    while end_time >= now:
        for line in check_output(['df', '-P']).split('\n'):
            m = regex.match(line)
            if m:
                line = line.split(None, 5)
                if len(line) > 1:
                    return line[-1]
        time.sleep(0.1)
        now = time.time()
    raise UserError('%r not mounted.' % dev)

def FindMainFeature(titles, verbose=False):
    if verbose:
        print('Attempting to determine main feature of %d titles...'
                % len(titles))
    main_feature = max(titles,
            key=lambda title: ParseDuration(title.info['duration']))
    if verbose:
        print('Selected %r as main feature.' % main_feature.number)
        print()

def ConstructTasks(titles, chapter_split):
    for title in titles:
        num_chapters = len(title.info['chapters'])
        if chapter_split and num_chapters > 1:
            for chapter in range(1, num_chapters + 1):
                yield Task(title, chapter)
        else:
            yield Task(title, None)

def TaskFilenames(tasks, output, dry_run=False, metadata=None):
    """
    Generate filenames for ripping tasks.

    Args:
        tasks: List of Task objects to rip
        output: Base output path/name
        dry_run: Whether this is a dry run
        metadata: Optional dict with 'title' and 'year' for naming

    Returns:
        List of output filenames
    """
    # Use metadata-based naming if available
    if metadata and metadata.get('title'):
        base_name = sanitize_filename(metadata['title'])
        if metadata.get('year'):
            base_name = f"{base_name} ({metadata['year']})"
    else:
        # Fall back to the output parameter
        base_name = os.path.basename(output) if output else "Video"

    if (len(tasks) > 1):
        # Multiple titles: create directory with individual files
        output_dir = output if not metadata else os.path.join(os.path.dirname(output) if output else '.', base_name)

        def ComputeFileName(task):
            if task.chapter is None:
                # If we have metadata, use it with title number
                if metadata and metadata.get('title'):
                    return os.path.join(output_dir,
                            f"{base_name} - Title{task.title.number:02d}.mp4")
                else:
                    return os.path.join(output_dir,
                            'Title%02d.mp4' % task.title.number)
            else:
                # Chapter split
                if metadata and metadata.get('title'):
                    return os.path.join(output_dir,
                            f"{base_name} - Title{task.title.number:02d}_Chapter{task.chapter:02d}.mp4")
                else:
                    return os.path.join(output_dir,
                            'Title%02d_%02d.mp4'
                            % (task.title.number, task.chapter))
        if not dry_run:
            os.makedirs(output_dir, exist_ok=True)
    else:
        # Single title: create single file
        def ComputeFileName(task):
            if metadata and metadata.get('title'):
                # Use metadata-based name
                output_dir = os.path.dirname(output) if output else '.'
                return os.path.join(output_dir, f"{base_name}.mp4")
            else:
                return '%s.mp4' % output

    result = [ComputeFileName(task) for task in tasks]
    if len(set(result)) != len(result):
        raise UserError("multiple tasks use same filename")
    return result

def PerformTasks(dvd, tasks, title_count, filenames,
        dry_run=False, verbose=False, no_subtitles=False):
    for task, filename in zip(tasks, filenames):
        print('=' * 78)
        if task.chapter is None:
            print('Title %s / %s => %r'
                    % (task.title.number, title_count, filename))
        else:
            num_chapters = len(task.title.info['chapters'])
            print('Title %s / %s , Chapter %s / %s=> %r'
                    % (task.title.number, title_count, task.chapter,
                        num_chapters, filename))
        print('-' * 78)
        dvd.RipTitle(task, filename, dry_run, verbose, no_subtitles)

Size = namedtuple('Size',
        ['width', 'height', 'pix_aspect_width', 'pix_aspect_height', 'fps'])

SIZE_REGEX = re.compile(
    r'^\s*(\d+)x(\d+),\s*'
    r'pixel aspect: (\d+)/(\d+),\s*'
    r'display aspect: (?:\d+(?:\.\d+)),\s*'
    r'(\d+(?:\.\d+)) fps\s*$')

SIZE_CTORS = [int] * 4 + [float]

def ParseSize(s):
    return Size(*(f(x)
        for f, x in zip(SIZE_CTORS, SIZE_REGEX.match(s).groups())))

def ComputeAspectRatio(size):
    w = size.width * size.pix_aspect_width
    h = size.height * size.pix_aspect_height
    d = gcd(w, h)
    return (w // d, h // d)

DURATION_REGEX = re.compile(
        r'^(?:.*,)?\s*duration\s+(\d\d):(\d\d):(\d\d)\s*(?:,.*)?$')

class Duration(namedtuple('Duration', 'hours minutes seconds')):
    def __str__(self):
        return '%02d:%02d:%02d' % (self)

    def in_seconds(self):
        return 60 * (60 * self.hours + self.minutes) + self.seconds

def ExtractDuration(s):
    return Duration(*map(int, DURATION_REGEX.match(s).groups()))

Chapter = namedtuple('Chapter', 'number duration')

def ParseChapters(d):
    """
    Parses dictionary of (str) chapter numbers to chapter.

    Result will be an iterable of Chapter objects, sorted by number.
    """
    for number, info in sorted(((int(n), info) for (n, info) in d.items())):
        yield Chapter(number, ExtractDuration(info))

AUDIO_TRACK_REGEX = re.compile(
        r'^(\S+)\s*((?:\([^)]*\)\s*)*)(?:,\s*(.*))?$')

AUDIO_TRACK_FIELD_REGEX = re.compile(
        r'^\(([^)]*)\)\s*\(([^)]*?)\s*ch\)\s*' +
        r'((?:\([^()]*\)\s*)*)\(iso639-2:\s*([^)]+)\)$')

AudioTrack = namedtuple('AudioTrack',
        'number lang codec channels iso639_2 extras')

def ParseAudioTracks(d):
    for number, info in sorted(((int(n), info) for (n, info) in d.items())):
        m = AUDIO_TRACK_REGEX.match(info)
        if m:
            lang, field_string, extras = m.groups()
            m2 = AUDIO_TRACK_FIELD_REGEX.match(field_string)
            if m2:
                codec, channels, more_extras, iso639_2 =  m2.groups()
                if more_extras:
                    extras = more_extras + (extras or "")
                yield AudioTrack(number, lang, codec, channels,
                    iso639_2, extras)
            else:
                warn('Cannot parse audio track fields %r' % field_string)
        else:
            warn('Cannot parse audio track info %r' % info)

SubtitleTrack = namedtuple('SubtitleTrack',
        'number info')

def ParseSubtitleTracks(d):
    for number, info in sorted(((int(n), info) for (n, info) in d.items())):
        yield SubtitleTrack(number, info)

def RenderBar(start, length, total, width):
    end = start + length
    start = int(round(start * (width - 1) / total))
    length = int(round(end * (width - 1) / total)) - start + 1
    return ('‥' * start +
            '■' * length +
            '‥' * (width - start - length))

MAX_BAR_WIDTH = 50

# TMDb metadata functions
def load_tmdb_api_key():
    """Load TMDb API key from file or environment variable."""
    # Try environment variable first
    api_key = os.environ.get('TMDB_API_KEY')
    if api_key:
        return api_key

    # Try config file
    config_file = os.path.expanduser('~/.tmdb_api_key')
    if os.path.exists(config_file):
        with open(config_file, 'r') as f:
            return f.read().strip()

    return None

def sanitize_filename(name):
    """Remove/replace characters that are invalid in filenames."""
    # Replace problematic characters with safe ones
    name = name.replace('/', '-')
    name = name.replace('\\', '-')
    name = name.replace(':', '-')
    name = name.replace('*', '')
    name = name.replace('?', '')
    name = name.replace('"', "'")
    name = name.replace('<', '')
    name = name.replace('>', '')
    name = name.replace('|', '-')
    return name

def join_mp4_files(input_files, output_file, verbose=False):
    """
    Join multiple MP4 files into a single file using FFmpeg concat filter with re-encoding.

    Uses re-encoding for reliable joining without artifacts at segment boundaries.

    Args:
        input_files: List of input file paths to join (in order)
        output_file: Path for the joined output file
        verbose: Whether to show FFmpeg output

    Returns:
        True if successful, False otherwise
    """
    if len(input_files) < 2:
        warn("Need at least 2 files to join")
        return False

    # Verify all input files exist
    for f in input_files:
        if not os.path.exists(f):
            warn(f"Input file not found: {f}")
            return False

    # Build the complex filter for concat
    # First, probe the first file to get target dimensions
    probe_args = [
        'ffprobe', '-v', 'error',
        '-select_streams', 'v:0',
        '-show_entries', 'stream=width,height',
        '-of', 'csv=p=0',
        input_files[0]
    ]
    probe_result = subprocess.run(probe_args, capture_output=True, text=True, check=False)
    if probe_result.returncode == 0 and probe_result.stdout.strip():
        target_width, target_height = probe_result.stdout.strip().split(',')
        target_width = int(target_width)
        target_height = int(target_height)
    else:
        # Default to standard DVD PAL resolution
        target_width, target_height = 720, 576

    # Build inputs and filter that scales each video to match dimensions
    inputs = []
    filter_parts = []
    concat_inputs = []

    for i, f in enumerate(input_files):
        inputs.extend(['-i', f])
        # Scale video to target size, then set SAR to 1:1 for consistent concatenation
        filter_parts.append(f'[{i}:v:0]scale={target_width}:{target_height}:force_original_aspect_ratio=disable,setsar=1[v{i}]')
        concat_inputs.append(f'[v{i}][{i}:a:0]')

    filter_complex = ';'.join(filter_parts) + ';' + ''.join(concat_inputs) + f'concat=n={len(input_files)}:v=1:a=1[outv][outa]'

    args = [
        'ffmpeg',
        *inputs,
        '-filter_complex', filter_complex,
        '-map', '[outv]',
        '-map', '[outa]',
        # Video encoding - match original dvdrip settings
        '-c:v', 'libx265',
        '-crf', '16',  # Match original dvdrip quality
        '-preset', 'medium',
        # Audio - copy if possible, or encode to AAC
        '-c:a', 'aac',
        '-b:a', '192k',
        '-y',  # Overwrite output
        output_file
    ]

    if verbose:
        print(f"[dvdrip] Joining {len(input_files)} files into {output_file} (re-encoding)")
        print(' '.join(args))

    if verbose:
        result = subprocess.run(args, check=False)
    else:
        result = subprocess.run(args, capture_output=True, check=False)

    if result.returncode != 0:
        if not verbose and result.stderr:
            warn(f"FFmpeg error: {result.stderr.decode('utf-8', errors='replace')}")
        return False

    return True

def search_tmdb(query, year=None, is_tv=False):
    """Search TMDb for a movie or TV show."""
    if not TMDB_AVAILABLE:
        raise RuntimeError("tmdbsimple not installed. Install with: pip install tmdbsimple")

    api_key = load_tmdb_api_key()
    if not api_key:
        raise RuntimeError(
            "TMDb API key not found. Set TMDB_API_KEY environment variable or "
            "save your API key to ~/.tmdb_api_key"
        )

    tmdb.API_KEY = api_key

    try:
        if is_tv:
            search = tmdb.Search()
            results = search.tv(query=query, first_air_date_year=year)
            return results['results']
        else:
            search = tmdb.Search()
            results = search.movie(query=query, year=year)
            return results['results']
    except Exception as e:
        warn(f"TMDb search failed: {e}")
        return []

def select_tmdb_result(results, is_tv=False):
    """Let user select from TMDb search results."""
    if not results:
        print("No results found in TMDb.")
        return None

    # Show up to 20 results
    max_results = min(len(results), 20)

    print(f"\nTMDb search results (showing {max_results} of {len(results)}):")
    for i, result in enumerate(results[:max_results], 1):
        if is_tv:
            title = result.get('name', 'Unknown')
            year = result.get('first_air_date', '')[:4]
        else:
            title = result.get('title', 'Unknown')
            year = result.get('release_date', '')[:4]

        tmdb_id = result.get('id', '')
        overview = result.get('overview', '')[:60]
        if len(result.get('overview', '')) > 60:
            overview += '...'

        print(f"  {i}. {title} ({year}) [ID: {tmdb_id}]")
        if overview:
            print(f"     {overview}")

    print("  0. Skip metadata (use default naming)")

    while True:
        try:
            choice = input(f"\nSelect a result (0-{max_results}), or enter a TMDb ID: ").strip()

            # Check if they entered a TMDb ID directly
            if choice.isdigit() and int(choice) > max_results:
                tmdb_id = int(choice)
                print(f"[dvdrip] Looking up TMDb ID {tmdb_id}...")
                return {'id': tmdb_id, '_use_id': True}

            choice_num = int(choice)
            if choice_num == 0:
                return None
            if 1 <= choice_num <= max_results:
                return results[choice_num - 1]
            print(f"Invalid selection. Please enter 0-{max_results} or a TMDb ID.")
        except (ValueError, KeyboardInterrupt):
            print("\nSkipping metadata.")
            return None

def get_metadata_by_id(tmdb_id, is_tv=False):
    """Get metadata from TMDb using a specific TMDb ID."""
    if not TMDB_AVAILABLE:
        raise RuntimeError("tmdbsimple not installed. Install with: pip install tmdbsimple")

    api_key = load_tmdb_api_key()
    if not api_key:
        raise RuntimeError(
            "TMDb API key not found. Set TMDB_API_KEY environment variable or "
            "save your API key to ~/.tmdb_api_key"
        )

    tmdb.API_KEY = api_key

    try:
        if is_tv:
            item = tmdb.TV(tmdb_id)
            info = item.info()
            title = info.get('name', 'Unknown')
            year = info.get('first_air_date', '')[:4]
        else:
            item = tmdb.Movies(tmdb_id)
            info = item.info()
            title = info.get('title', 'Unknown')
            year = info.get('release_date', '')[:4]

        return {
            'title': title,
            'year': year,
            'tmdb_id': tmdb_id
        }
    except Exception as e:
        warn(f"TMDb ID lookup failed: {e}")
        return None

def get_metadata_from_tmdb(search_query=None, year=None, is_tv=False):
    """Get metadata from TMDb by searching for a title."""
    if not search_query:
        search_query = input("Enter movie/TV show title (or TMDb ID): ").strip()
        if not search_query:
            return None

    # Check if user entered a TMDb ID (numeric)
    if search_query.isdigit():
        print(f"[dvdrip] Looking up TMDb ID {search_query}...")
        return get_metadata_by_id(int(search_query), is_tv=is_tv)

    results = search_tmdb(search_query, year=year, is_tv=is_tv)
    if not results:
        print("\nNo results found. Try a different search term or use the TMDb ID.")
        print("Tip: Find the TMDb ID in the URL, e.g., themoviedb.org/movie/111160")
        return None

    selected = select_tmdb_result(results, is_tv=is_tv)
    if not selected:
        return None

    # Check if user entered a TMDb ID directly at the selection prompt
    if selected.get('_use_id'):
        return get_metadata_by_id(selected['id'], is_tv=is_tv)

    # Return a clean metadata dict
    if is_tv:
        title = selected.get('name', 'Unknown')
        year = selected.get('first_air_date', '')[:4]
    else:
        title = selected.get('title', 'Unknown')
        year = selected.get('release_date', '')[:4]

    return {
        'title': title,
        'year': year,
        'tmdb_id': selected.get('id')
    }

def DisplayScan(titles, metadata=None):
    max_title_seconds = max(
                    title.info['duration'].in_seconds()
                    for title in titles)

    # Display metadata if available
    if metadata and metadata.get('title'):
        print('=' * 78)
        print(f"TMDb Metadata: {metadata['title']} ({metadata.get('year', 'unknown')})")
        print('=' * 78)
        print()

    for title in titles:
        info = title.info
        size = ParseSize(info['size'])
        xaspect, yaspect = ComputeAspectRatio(size)
        duration = info['duration']
        title_seconds = duration.in_seconds()
        print('Title % 3d/% 3d: %s  %d×%d  %d:%d  %3g fps' %
                (title.number, len(titles), duration, size.width,
                    size.height, xaspect, yaspect, size.fps))
        for at in ParseAudioTracks(info['audio tracks']):
            print('  audio % 3d: %s (%sch)  [%s]' %
                    (at.number, at.lang, at.channels, at.extras))
        for sub in ParseSubtitleTracks(info['subtitle tracks']):
            print('  sub % 3d: %s' %
                    (sub.number, sub.info))
        position = 0
        if title_seconds > 0:
            for chapter in ParseChapters(info['chapters']):
                seconds = chapter.duration.in_seconds()
                bar_width = int(round(
                    MAX_BAR_WIDTH * title_seconds / max_title_seconds))
                bar = RenderBar(position, seconds, title_seconds, bar_width)
                print('  chapter % 3d: %s ◖%s◗'
                        % (chapter.number, chapter.duration, bar))
                position += seconds
        print()

def ParseArgs():
    description, epilog = __doc__.strip().split('\n', 1)
    parser = argparse.ArgumentParser(description=description, epilog=epilog,
            formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('-v', '--verbose',
            action='store_true',
            help="Increase verbosity.")
    parser.add_argument('-c', '--chapter_split',
            action='store_true',
            help="Split each chapter out into a separate file.")
    parser.add_argument('-n', '--dry-run',
            action='store_true',
            help="Don't actually write anything.")
    parser.add_argument('--scan',
            action='store_true',
            help="Display scan of disc; do not rip.")
    parser.add_argument('--main-feature',
            action='store_true',
            help="Rip only the main feature title.")
    parser.add_argument('-t', '--titles',
            default="*",
            help="""Comma-separated list of title numbers to consider
            (starting at 1) or * for all titles.""")
    parser.add_argument(
        '-i', '--input',
        help="Volume to rip (auto-detected if omitted).",
        required=False
    )
    parser.add_argument('-o', '--output',
            help="""Output location. Extension is added if only one title
            being ripped, otherwise, a directory will be created to contain
            ripped titles.""")
    parser.add_argument('--mount-timeout',
            default=15,
            help="Amount of time to wait for a mountpoint to be mounted",
            type=float)
    parser.add_argument('--title-search',
            help="Search TMDb for this title and use metadata for naming")
    parser.add_argument('--year',
            type=int,
            help="Release year to narrow TMDb search")
    parser.add_argument('--tv',
            action='store_true',
            help="Search for TV show instead of movie")
    parser.add_argument('--no-metadata',
            action='store_true',
            help="Skip metadata lookup and use default naming")
    parser.add_argument('--no-subtitles',
            action='store_true',
            help="Exclude all subtitle tracks from output")
    parser.add_argument('--join',
            action='store_true',
            help="Join all ripped titles into a single MP4 file using FFmpeg")
    parser.add_argument('--join-titles',
            help="""Comma-separated list of title numbers to join into a single
            file (e.g., '1,2,3'). Implies joining.""")
    parser.add_argument('--keep-files',
            action='store_true',
            help="Keep individual files after joining (default: delete them)")
    args = parser.parse_args()

    if not args.input:
        try:
            args.input = find_optical_drive_device(prefer_with_media=True)
            print(f"[dvdrip] Auto-detected optical drive: {args.input}")
        except Exception as e:
            parser.error(f"No input specified and auto-detection failed: {e}")
    if not args.scan and args.output is None:
        raise UserError("output argument is required")

    return args

# TODO: make it possible to have ranges with no end (meaning they end at last
# title)
NUM_RANGE_REGEX = re.compile(r'^(\d*)-(\d+)|(\d+)$')
def parse_titles_arg(titles_arg):
    if titles_arg == '*':
        return None # all titles
    else:
        def str_to_ints(s):
            m = NUM_RANGE_REGEX.match(s)
            if not m :
                raise UserError(
                    "--titles must be * or list of integer ranges, found %r" %
                    titles_arg)
            else:
                start,end,only = m.groups()
                if only is not None:
                    return [int(only)]
                else:
                    start = int(start) if start else 1
                    end = int(end)
                    return range(start, end + 1)
        result = set()
        for s in titles_arg.split(','):
            result.update(str_to_ints(s))
        result = sorted(list(result))
        return result

def main():
    args = ParseArgs()
    # If input is a block device (e.g. /dev/sr0), convert it to a mountpoint
    mounted_temp_dir = None

    if is_block_device(args.input):
        mp = find_mountpoint(args.input)
        if mp:
            args.input = mp
        else:
            # Mount it now (read-only)
            mounted_temp_dir = mount_device_readonly(args.input, timeout_sec=args.mount_timeout)
            args.input = mounted_temp_dir

    try:
        dvd = DVD(args.input, args.verbose, args.mount_timeout)
        print('Reading from %r' % dvd.mountpoint)
        title_numbers = parse_titles_arg(args.titles)
        titles = tuple(dvd.ScanTitles(title_numbers, args.verbose))

        if args.scan:
            # Fetch metadata for scan display if available
            metadata = None
            if not args.no_metadata:
                try:
                    if args.title_search:
                        # User provided a search query
                        print(f"[dvdrip] Searching TMDb for '{args.title_search}'...")
                        metadata = get_metadata_from_tmdb(
                            search_query=args.title_search,
                            year=args.year,
                            is_tv=args.tv
                        )
                    elif TMDB_AVAILABLE and load_tmdb_api_key():
                        # API is available, offer to search
                        print("\n[dvdrip] TMDb metadata available. Search for title info?")
                        response = input("Search TMDb? (y/n): ").strip().lower()
                        if response in ('y', 'yes'):
                            metadata = get_metadata_from_tmdb(
                                year=args.year,
                                is_tv=args.tv
                            )
                except Exception as e:
                    warn(f"Metadata lookup failed: {e}")

            DisplayScan(titles, metadata=metadata)
        else:
            if args.main_feature and len(titles) > 1:
                # TODO: make this affect scan as well
                titles = [FindMainFeature(titles, args.verbose)]

            if not titles:
                raise UserError("No titles to rip")
            else:
                if not args.output:
                    raise UserError("No output specified")

                # Fetch metadata from TMDb if requested
                metadata = None
                if not args.no_metadata:
                    try:
                        if args.title_search:
                            # User provided a search query
                            print(f"[dvdrip] Searching TMDb for '{args.title_search}'...")
                            metadata = get_metadata_from_tmdb(
                                search_query=args.title_search,
                                year=args.year,
                                is_tv=args.tv
                            )
                        elif TMDB_AVAILABLE and load_tmdb_api_key():
                            # API is available, offer to search
                            print("\n[dvdrip] TMDb metadata available. Search for better file naming?")
                            response = input("Search TMDb? (y/n): ").strip().lower()
                            if response in ('y', 'yes'):
                                metadata = get_metadata_from_tmdb(
                                    year=args.year,
                                    is_tv=args.tv
                                )

                        if metadata:
                            print(f"[dvdrip] Using metadata: {metadata['title']} ({metadata.get('year', 'unknown year')})")
                    except Exception as e:
                        warn(f"Metadata lookup failed: {e}")
                        print("[dvdrip] Continuing with default naming...")

                print('Writing to %r' % args.output)
                tasks = tuple(ConstructTasks(titles, args.chapter_split))

                filenames = TaskFilenames(tasks, args.output, dry_run=args.dry_run, metadata=metadata)
                # Don't stomp on existing files
                for filename in filenames:
                    if os.path.exists(filename):
                        raise UserError('%r already exists' % filename)

                PerformTasks(dvd, tasks, len(titles), filenames,
                        dry_run=args.dry_run, verbose=args.verbose,
                        no_subtitles=args.no_subtitles)

                # Handle joining if requested
                if (args.join or args.join_titles) and not args.dry_run:
                    print('=' * 78)
                    print('[dvdrip] Joining files...')

                    # Determine which files to join
                    if args.join_titles:
                        # Parse the join-titles argument
                        join_title_nums = set()
                        for part in args.join_titles.split(','):
                            part = part.strip()
                            if part.isdigit():
                                join_title_nums.add(int(part))
                            else:
                                warn(f"Invalid title number in --join-titles: {part}")

                        # Filter filenames to only include specified titles
                        files_to_join = []
                        for task, filename in zip(tasks, filenames):
                            if task.title.number in join_title_nums:
                                files_to_join.append(filename)
                    else:
                        # Join all files
                        files_to_join = list(filenames)

                    if len(files_to_join) >= 2:
                        # Generate output filename for joined file (same directory as individual files)
                        output_dir = os.path.dirname(filenames[0]) if filenames else '.'
                        if not output_dir:
                            output_dir = '.'

                        if metadata and metadata.get('title'):
                            base_name = sanitize_filename(metadata['title'])
                            if metadata.get('year'):
                                base_name = f"{base_name} ({metadata['year']})"
                            joined_output = os.path.join(output_dir, f"{base_name} - Joined.mp4")
                        else:
                            joined_output = os.path.join(output_dir, "Joined.mp4")

                        # Check if joined output already exists
                        if os.path.exists(joined_output):
                            warn(f"Joined output file already exists: {joined_output}")
                        else:
                            print(f'[dvdrip] Joining {len(files_to_join)} files into: {joined_output}')
                            if join_mp4_files(files_to_join, joined_output, verbose=args.verbose):
                                print(f'[dvdrip] Successfully created: {joined_output}')

                                # Delete individual files unless --keep-files
                                if not args.keep_files:
                                    print('[dvdrip] Removing individual files...')
                                    for f in files_to_join:
                                        try:
                                            os.remove(f)
                                            if args.verbose:
                                                print(f'  Deleted: {f}')
                                        except OSError as e:
                                            warn(f"Could not delete {f}: {e}")

                                    # Try to remove the directory if empty
                                    output_dir = os.path.dirname(filenames[0]) if filenames else None
                                    if output_dir and output_dir != '.' and os.path.isdir(output_dir):
                                        try:
                                            os.rmdir(output_dir)
                                            if args.verbose:
                                                print(f'  Removed empty directory: {output_dir}')
                                        except OSError:
                                            pass  # Directory not empty, that's fine
                            else:
                                warn("Failed to join files. Individual files preserved.")
                    else:
                        if files_to_join:
                            warn("Need at least 2 files to join. Skipping join.")
                        else:
                            warn("No files matched --join-titles specification.")

                print('=' * 78)
                if not args.dry_run:
                    dvd.Eject()
    finally:
        if mounted_temp_dir:
            unmount(mounted_temp_dir)

def warn(msg):
        print('warning: %s' % (msg,), file=sys.stderr)

if __name__ == '__main__':
    error = None
    try:
        main()
    except FileExistsError as exc:
        error = '%s: %r' % (exc.strerror, exc.filename)
    except UserError as exc:
        error = exc.message

    if error is not None:
        print('%s: error: %s'
                % (os.path.basename(sys.argv[0]), error), file=sys.stderr)
        sys.exit(1)
