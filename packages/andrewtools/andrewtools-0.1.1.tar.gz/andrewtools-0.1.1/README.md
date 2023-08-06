# About
<!-- UPDATE VERSION IN BADGE MANUALLY -->
![PyPI Version](https://img.shields.io/badge/pypi-v0.1.1-orange)
![Build](https://img.shields.io/github/workflow/status/andrewt110216/andrewtools/Tests?style=plastic)

`andrewtools` is an assortment of handy Python tools made by someone named Andrew.

# Quick Start

## Supported Python Versions

Python 3.8+

## Mac / Linux
```
pip install andrewtools
```

## Windows
```
py -m pip install andrewtools
```

# Examples

## Progress Bar

If you are working on a program that uses a loop that takes a significant amount of time to execute, it can be nice to follow the progress of your program while it runs. Use `progress_bar` to visualize the progress via the command line.

```
import time
from andrewtools import progress_bar

iterations = 10
for i in range(iterations):
    time.sleep(0.5)
    progress_bar(i, iterations, width=10, prefix="Progress")

# Printed to command line:
Progress | ***------- | 30%  <- % and progress bar update in-place while loop runs
```

- Warning: this function will not play well if the loop includes other print statements. The progress bar may get printed on a separate line for each iteration, which may not be desirable.
- Note: in the case of a constant runtime per iteration, the progress bar provides a good estimate of the relative amount of execution *time* remaining. Be aware that in the case of variable runtimes per iteration (e.g. if there is an inner loop with a varying workload), the progress bar is *not* a good estimate of the remaining execution time. It simply tracks the progress through the *number* of iterations.

## AndrewTimer

`AndrewTimer` provides a simple API for a timer to use to measure execution time of your programs.

```
from andrewtools import AndrewTimer

    at = AndrewTimer()
    for i in range(10):
        time.sleep(0.5)
        at.lap()

        # Use in tandem with `progress_bar` as follows:
        end = f"(Last {at.last_lap(format=True)}) (Total: {at.elapsed(format=True)})"
        progress_bar(i, 10, width=10, label="Progress", end=end)

    # Measure total time since instantiation
    total_time = at.elapsed('s', format=True)

    # Measure average time of all laps recorded on the timer
    average_time = at.average('s', format=True)

    # Display formatted times
    print(f"Total: {total_time}, Average: {average_time}")  # approx. 5.000s 0.500s
```