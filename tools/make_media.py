"""Generates the audio jingle (wav + mp3) and the walk video (mp4 + poster)."""
import math
import os
import subprocess
import array
import wave

import imageio
import imageio_ffmpeg
import numpy
from PIL import Image
import sys

sys.path.insert(0, os.path.dirname(__file__))
from make_images import park_scene

ROOT = os.path.join(os.path.dirname(__file__), "..")
MEDIA = os.path.join(ROOT, "media")
IMG = os.path.join(ROOT, "img")
os.makedirs(MEDIA, exist_ok=True)

FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()

# ---------- audio: cheerful little jingle, C major ----------
SR = 22050
notes = [  # (freq, duration)
    (523.25, 0.35), (659.25, 0.35), (783.99, 0.35), (1046.50, 0.5),
    (783.99, 0.3), (1046.50, 0.8),
]
samples = []
for freq, dur in notes:
    n = int(SR * dur)
    for i in range(n):
        t = i / SR
        env = min(1.0, i / 400) * math.exp(-2.2 * t / dur)  # attack + decay
        v = 0.45 * math.sin(2 * math.pi * freq * t) + 0.12 * math.sin(2 * math.pi * freq * 2 * t)
        samples.append(int(v * env * 32000))
# small silence tail
samples += [0] * int(SR * 0.3)

with wave.open(os.path.join(MEDIA, "jingle.wav"), "wb") as w:
    w.setnchannels(1)
    w.setsampwidth(2)
    w.setframerate(SR)
    w.writeframes(array.array("h", samples).tobytes())

subprocess.run([FFMPEG, "-y", "-loglevel", "error", "-i", os.path.join(MEDIA, "jingle.wav"),
                "-b:a", "64k", os.path.join(MEDIA, "jingle.mp3")], check=True)

# ---------- video: Anna & dog walk across the park (landscape!) ----------
W, H, FPS, SECS = 640, 360, 12, 5
frames = int(FPS * SECS)
writer = imageio.get_writer(os.path.join(MEDIA, "walk.mp4"), fps=FPS, codec="libx264", quality=7, macro_block_size=8)
poster = None
for f in range(frames):
    t = f / frames
    wx = int(-80 + t * 780)
    step = f // 3
    img = park_scene(W, H, step=step, wx=wx, clouds=(0.15 + 0.05 * math.sin(t * 6), 0.5),
                     ground=(120, 168, 120))
    writer.append_data(numpy.asarray(img))
    if f == frames // 2:
        poster = img
writer.close()
poster.save(os.path.join(IMG, "videoposter.jpg"), quality=82)

for name in ("jingle.wav", "jingle.mp3", "walk.mp4"):
    print(name, os.path.getsize(os.path.join(MEDIA, name)) // 1024, "KB")
print("poster ok")
