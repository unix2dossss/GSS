## GSS — Garage Security System

A small, self-hosted security system built on a Linux server using Python.

It reads frames from a camera, detects motion, streams live video over HTTP, and records clips when something actually happens. Built as a practical alternative to buying an off-the-shelf system.

### Why this exists

I built this because I didn't want to spend $200 on a cheap, unreliable security system. It’s a simple, headless camera system running on an old HP laptop in my garage.

---

### What it does

- Motion detection using frame differencing (pixel-level, not brightness-based)
- Livestream
- Automatic recording on motion
- Optional loud audio alerts via connected speakers
- Telegram notifications with snapshots and recording links

Runs headless and locally. No cloud services.

---

### Architecture

The system follows a simple publish–subscribe setup:

- One component reads frames from the camera
- Other components subscribe and handle detection, streaming, recording, and alerts

This keeps things modular and easy to extend.

---

### Running it

Requirements:
- Linux
- Python 3
- A USB or built-in camera

Create a virtual environment, install dependencies, and run the main process.  
In practice this is set up as a `systemd` service so it starts on boot and restarts if it crashes.


### License

MIT
