# SPyProf
Sampling line-by-line Python profiler.

# Installation
```bash
pip install https://github.com/yuriiz/spyprof
```

# Usage
Import `spyprof` module at startup:

```python
import spyprof
```

Profiling reports will be written to `spyprof` directory periodically every 10 seconds and at application exit.

Profiling report measured with `ITIMER_REAL` timer will be written to spyprof/real.html.

Profiling report measured with `ITIMER_PROF` timer will be written to spyprof/prof.html.

# Example

Running following code:
```python
import math
from time import sleep

import spyprof


def foo():
    """
    CPU time consuming code.
    """
    for i in range(10**8):
        math.sqrt(i)
        math.sqrt(i)
        pass


def bar():
    """
    Real time consuming code.
    """
    sleep(10)


if __name__ == "__main__":
    foo()
    bar()
```

Will result in the following reports:
| real.html | prof.html |
| --------- | --------- |
| <img width="1280" height="958" alt="Screenshot 2025-09-08 at 21-13-57 " src="https://github.com/user-attachments/assets/a801a750-9471-439b-85d0-3fce44c37cc6" /> | <img width="1280" height="958" alt="Screenshot 2025-09-08 at 21-14-04 " src="https://github.com/user-attachments/assets/5a1360cc-19e3-4571-b808-e415049e3d3b" /> |



