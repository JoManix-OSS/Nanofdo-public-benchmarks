import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import benchmark


class BenchmarkClientTests(unittest.TestCase):
    def setUp(self):
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.key_file = Path(self.temporary_directory.name) / ".nanofdo-benchmark-key"
        self.key_file_patch = patch.object(benchmark, "KEY_FILE", self.key_file)
        self.key_file_patch.start()
        self.environment_patch = patch.dict(os.environ, {}, clear=True)
        self.environment_patch.start()

    def tearDown(self):
        self.environment_patch.stop()
        self.key_file_patch.stop()
        self.temporary_directory.cleanup()

    def test_environment_key_has_priority(self):
        os.environ["NANOFDO_BENCHMARK_KEY"] = "DEV-environment-key"
        self.key_file.write_text("DEV-file-key", encoding="utf-8")

        with patch.object(benchmark, "register") as register:
            key = benchmark.load_or_register_key("researcher@example.com")

        self.assertEqual(key, "DEV-environment-key")
        register.assert_not_called()

    def test_stored_key_prevents_new_registration(self):
        self.key_file.write_text("DEV-stored-key", encoding="utf-8")

        with patch.object(benchmark, "register") as register:
            key = benchmark.load_or_register_key("researcher@example.com")

        self.assertEqual(key, "DEV-stored-key")
        register.assert_not_called()

    def test_first_registration_persists_key(self):
        with patch.object(benchmark, "register", return_value="DEV-new-key") as register:
            key = benchmark.load_or_register_key("researcher@example.com")

        self.assertEqual(key, "DEV-new-key")
        self.assertEqual(self.key_file.read_text(encoding="utf-8"), "DEV-new-key")
        register.assert_called_once_with("researcher@example.com")

    def test_email_is_required_without_existing_key(self):
        with self.assertRaises(SystemExit):
            benchmark.load_or_register_key(None)


if __name__ == "__main__":
    unittest.main()
