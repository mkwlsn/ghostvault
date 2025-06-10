import unittest
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import subprocess

VAULT = Path.home() / "ghostvault"
SYSTEM = VAULT / "system"
TEST_COMMAND = ["python3", str(SYSTEM / "ghost_init.py")]

class TestGhostInit(unittest.TestCase):

    def test_vault_directory_exists(self):
        self.assertTrue(VAULT.exists(), "VAULT directory should exist.")

    def test_system_directory_exists(self):
        self.assertTrue(SYSTEM.exists(), "SYSTEM directory should exist.")

    def test_init_normie_mode_runs(self):
        result = subprocess.run(TEST_COMMAND, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        print("STDOUT:", result.stdout)
        print("STDERR:", result.stderr)
        self.assertEqual(result.returncode, 0, "ghost_init.py should exit cleanly in normie mode.")
        self.assertIn("setup complete", result.stdout)

    def test_init_cursed_mode_runs(self):
        result = subprocess.run(TEST_COMMAND + ["--cursed"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        print("STDOUT:", result.stdout)
        print("STDERR:", result.stderr)
        self.assertEqual(result.returncode, 0, "ghost_init.py should exit cleanly in cursed mode.")
        self.assertIn("𝔤𝔥𝔬𝔰𝔱 𝔦𝔰 𝔟𝔬𝔲𝔫𝔡", result.stdout)

    def test_ghostd_status(self):
        from ghost_daemon import status_ghostd
        result = status_ghostd()
        self.assertTrue(result is None or isinstance(result, str), "Expected status_ghostd() to return a string or None")
        self.assertIn("status", result.lower() if result else "")

    def test_module_sync_runs(self):
        from ghost_modules import ghost_sync_modules
        try:
            ghost_sync_modules()
        except Exception as e:
            self.fail(f"ghost_sync_modules() raised an exception: {e}")

    def test_queue_and_log_task(self):
        from ghost_runtime import queue_task, log_event
        try:
            queue_task("test-task")
            log_event("Test event log")
        except Exception as e:
            self.fail(f"Queue or log functions failed: {e}")

if __name__ == "__main__":
    unittest.main()