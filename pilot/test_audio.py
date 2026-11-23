"""Check the committed listening takes against the musical claims on the card."""

from array import array
from html.parser import HTMLParser
from pathlib import Path
import sys
import unittest
import wave


class AudioLinks(HTMLParser):
    def __init__(self):
        super().__init__()
        self.players = set()
        self.links = set()

    def handle_starttag(self, tag, attributes):
        attrs = dict(attributes)
        if tag in ("audio", "source") and attrs.get("src"):
            self.players.add(attrs["src"])
        if tag == "a" and attrs.get("href"):
            self.links.add(attrs["href"])


class KickExerciseTest(unittest.TestCase):
    def test_player_and_download_links_reach_each_take(self):
        page = Path(__file__).with_name("kick-placement.html")
        media = AudioLinks()
        media.feed(page.read_text())
        expected = {f"audio/take-{name}.wav" for name in "abc"}
        self.assertEqual(media.players, expected)
        self.assertTrue(expected <= media.links)
        for relative_path in expected:
            self.assertTrue((page.parent / relative_path).is_file(), relative_path)

    def test_only_the_second_kick_changes(self):
        bars = []
        for name in ("a", "b", "c"):
            path = Path(__file__).with_name("audio") / f"take-{name}.wav"
            with wave.open(str(path)) as wav:
                audio_format = wav.getframerate(), wav.getnchannels(), wav.getsampwidth()
                self.assertEqual(audio_format, (48_000, 1, 2))
                self.assertEqual(wav.getnframes(), 256_000)
                samples = array("h", wav.readframes(wav.getnframes()))
            if sys.byteorder != "little":
                samples.byteswap()
            self.assertTrue(samples[:128_000] == samples[128_000:], f"Take {name} must repeat one bar")
            self.assertLess(max(abs(value) for value in samples), 32767)
            bars.append(samples[:128_000])

        reference, moved, longer = bars
        beat_three, three_and = 64_000, 80_000
        short, long, end_fade = 6_000, 24_000, 480
        self.assertTrue(reference[:beat_three] == moved[:beat_three])
        self.assertTrue(reference[beat_three + short:three_and] == moved[beat_three + short:three_and])
        self.assertTrue(reference[three_and + short:] == moved[three_and + short:])
        original_hit = slice(beat_three, beat_three + short)
        delayed_hit = slice(three_and, three_and + short)
        removed = (a - b for a, b in zip(reference[original_hit], moved[original_hit]))
        added = (b - a for a, b in zip(reference[delayed_hit], moved[delayed_hit]))
        differences = list(zip(removed, added))
        self.assertGreater(max(abs(a) for a, _ in differences), 1000)
        self.assertTrue(all(abs(a - b) <= 2 for a, b in differences), "The same kick must move by one eighth")
        self.assertTrue(reference[:beat_three + short - end_fade] == longer[:beat_three + short - end_fade])
        self.assertTrue(reference[three_and:beat_three + long] != longer[three_and:beat_three + long])
        self.assertTrue(reference[beat_three + long:] == longer[beat_three + long:])


if __name__ == "__main__":
    unittest.main()
