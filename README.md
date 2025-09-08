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
| <img width="1280" height="1018" alt="Screenshot 2025-09-08 at 21-38-40 " src="https://github.com/user-attachments/assets/c6fd5d52-0cea-4183-8ae8-8b8cf7677a81" /> | <img width="1280" height="1018" alt="Screenshot 2025-09-08 at 21-38-34 " src="https://github.com/user-attachments/assets/e899ab38-550a-408f-8f70-8e797b2e8e3d" /> |



