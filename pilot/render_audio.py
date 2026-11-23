"""Render the original listening guides for the kick exercise using only Python."""

from array import array
from math import exp, sin, tau
from pathlib import Path
from random import Random
import sys
import wave


RATE = 48_000
EIGHTH = RATE * 60 // (90 * 2)
BAR = 8 * EIGHTH
OUTPUT = Path(__file__).with_name("audio")


def kick():
    sound = []
    for frame in range(RATE // 2):
        t = frame / RATE
        phase = tau * (54 * t + 3.6 * (1 - exp(-32 * t)))
        sound.append(0.38 * exp(-3 * t) * (sin(phase) + 0.20 * sin(2 * phase)))
    return sound


def trim(sound, length):
    result = sound[:length]
    fade = RATE // 100
    for i in range(fade):
        result[-fade + i] *= (fade - 1 - i) / (fade - 1)
    return result


def pitched(hz, seconds, gain):
    sound = []
    for frame in range(round(seconds * RATE)):
        t = frame / RATE
        envelope = min(1, t / 0.004, (seconds - t) / 0.025) * exp(-3 * t)
        phase = tau * hz * t
        sound.append(gain * envelope * (sin(phase) + 0.38 * sin(2 * phase)))
    return sound


def percussion(seconds, decay, gain, seed):
    rng = Random(seed)
    return [gain * exp(-decay * n / RATE) * rng.uniform(-1, 1)
            for n in range(round(seconds * RATE))]


def place(bar, eighth_index, sound):
    start = eighth_index * EIGHTH
    assert start + len(sound) <= len(bar)
    for i, value in enumerate(sound, start):
        bar[i] += value


def render():
    full = kick()
    short = trim(full, RATE // 8)
    long = trim(full, RATE // 2)
    backing = [0.0] * BAR
    hat = percussion(0.035, 130, 0.10, seed=2)
    snare = percussion(0.14, 37, 0.24, seed=4)
    bass = pitched(65.4064, 0.22, 0.23)
    for beat in (0, 2, 4, 6):
        place(backing, beat, hat)
    for backbeat in (2, 6):
        place(backing, backbeat, snare)
    for offbeat in (1, 5):
        place(backing, offbeat, bass)
    place(backing, 7, pitched(391.9954, 0.14, 0.105))
    place(backing, 0, short)

    OUTPUT.mkdir(exist_ok=True)
    for label, position, second_kick in (("a", 4, short), ("b", 5, short), ("c", 4, long)):
        bar = backing.copy()
        place(bar, position, second_kick)
        assert max(abs(v) for v in bar) < 1, "A common gain must leave all takes unclipped"
        samples = array("h", (round(32767 * v) for v in bar))
        if sys.byteorder != "little":
            samples.byteswap()
        with wave.open(str(OUTPUT / f"take-{label}.wav"), "wb") as wav:
            wav.setparams((1, 2, RATE, 0, "NONE", "not compressed"))
            wav.writeframes(samples.tobytes() * 2)


if __name__ == "__main__":
    render()
