import unittest
import time

def pause_screen(seconds):
    """Pause the screen for the specified number of seconds"""
    time.sleep(seconds)

class TestPauseScreen(unittest.TestCase):
    def test_pause_screen(self):
        # Test pausing the screen for 3 seconds
        start_time = time.time()
        pause_screen(3)
        elapsed_time = time.time() - start_time
        self.assertAlmostEqual(elapsed_time, 3, delta=0.1)

        # Test pausing the screen for 5 seconds
        start_time = time.time()
        pause_screen(5)
        elapsed_time = time.time() - start_time
        self.assertAlmostEqual(elapsed_time, 5, delta=0.1)

        # Test pausing the screen for 0.5 seconds
        start_time = time.time()
        pause_screen(0.5)
        elapsed_time = time.time() - start_time
        self.assertAlmostEqual(elapsed_time, 0.5, delta=0.1)

if __name__ == '__main__':
    unittest.main()