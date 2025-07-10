# SPyProf
Sampling Python profiler

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
