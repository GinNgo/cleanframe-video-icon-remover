import json
import tempfile
import unittest
from pathlib import Path

from app.core import VideoInfo, VideoToolError, normalize_region, write_audit_event


class CoreTests(unittest.TestCase):
    def setUp(self):
        self.info = VideoInfo(1080, 1920, 24.0, 10.0, 8_000_000, True)

    def test_region_is_normalized_to_even_values(self):
        self.assertEqual(normalize_region(11, 13, 101, 99, self.info), (10, 12, 100, 98))

    def test_small_region_is_rejected(self):
        with self.assertRaises(VideoToolError):
            normalize_region(0, 0, 6, 20, self.info)

    def test_out_of_bounds_region_is_rejected(self):
        with self.assertRaises(VideoToolError):
            normalize_region(1000, 1800, 100, 200, self.info)

    def test_audit_event_contains_provenance(self):
        with tempfile.TemporaryDirectory() as directory:
            log = Path(directory) / "audit.jsonl"
            write_audit_event(log, "owned.mp4", "abc123", self.info, (10, 12, 100, 98))
            event = json.loads(log.read_text(encoding="utf-8"))
            self.assertEqual(event["source_sha256"], "abc123")
            self.assertTrue(event["rights_attested"])


if __name__ == "__main__":
    unittest.main()

