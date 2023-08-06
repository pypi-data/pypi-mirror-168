"""An easy-to-use timer"""
import time
from andrewtools import progress_bar
from andrewtools.utils import validate_type


class AndrewTimer:
    def __init__(self):
        self.start_time = time.time()
        self.lap_start = self.start_time
        self.laps = []

    def elapsed(self, units="s", format=False):
        """
        Return the total elapsed time

        :param str units: 's' = seconds, 'ms' = milliseconds, 'ns' = nanoseconds
                          'm' = minutes
        :param bool format: False = return elapsed time as a float
                            True = return a format string with units appended
        """
        # Validate input types
        units = validate_type(units, str)
        format = validate_type(format, bool)

        # Calculate elapsed time in correct units
        elapsed = time.time() - self.start_time
        elapsed = self._convert(elapsed, units)

        if format:
            return self._format(elapsed, units)
        return elapsed

    def lap(self):
        """End the current lap and start a new lap"""
        now = time.time()
        self.laps.append(now - self.lap_start)
        self.lap_start = now

    def average(self, units="s", format=False):
        """
        Return average lap time

        :param str units: 's' = seconds, 'ms' = milliseconds, 'ns' = nanoseconds
                          'm' = minutes
        :param bool format: False = return elapsed time as a float
                            True = return a format string with units appended
        """
        # Validate input types
        units = validate_type(units, str)
        format = validate_type(format, bool)

        # Calculate average lap time in correct units
        avg = sum(self.laps) / len(self.laps)
        avg = self._convert(avg, units)

        if format:
            return self._format(avg, units)
        return avg

    def get_laps(self):
        return self.laps

    def last_lap(self, units="s", format=False):
        """
        Return the time of the last lap

        :param str units: 's' = seconds, 'ms' = milliseconds, 'ns' = nanoseconds
                          'm' = minutes
        :param bool format: False = return elapsed time as a float
                            True = return a format string with units appended
        """
        # Validate input types
        units = validate_type(units, str)
        format = validate_type(format, bool)

        # Get time of last lap in correct units
        last_lap = self.laps[-1] if self.laps else 0
        last_lap = self._convert(last_lap, units)

        if format:
            return self._format(last_lap, units)
        return last_lap

    def _convert(self, time, units):
        if units == "s":
            return time
        elif units == "ms":
            return time * 1_000
        elif units == "ns":
            return time * 1_000_000
        elif units == "m":
            return time / 60
        else:
            raise ValueError(f"Units must be 'm', 's', 'ms', or 'ns', not {units}")

    def _format(self, time, units):
        return f"{time:,.3f}{units}"


if __name__ == "__main__":

    # Usage
    t = AndrewTimer()
    for i in range(10):
        time.sleep(0.5)
        t.lap()
        end = f"(Last {t.last_lap(format=True)}) (Total: {t.elapsed(format=True)})"
        progress_bar(i, 10, width=10, label="Progress", end=end)

    total_time = t.elapsed("s", format=True)
    average_time = t.average("s", format=True)
    print(f"Total: {total_time}, Average: {average_time}")  # approx. 5.000s 0.500s
