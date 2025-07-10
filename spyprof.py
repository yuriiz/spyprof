import atexit
import signal
import site
from collections import Counter
from pathlib import Path

from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import PythonLexer

DUMP_INTERVAL = 10  # seconds
SAMPLES_PER_SECOND = 1000
SAMPLE_INTERVAL = 1 / SAMPLES_PER_SECOND

_real_counter: Counter[tuple[str, int]] = Counter()
_prof_counter: Counter[tuple[str, int]] = Counter()
_n_samples = 0


def alarm(signum, frame) -> None:
    global _n_samples
    increment(_real_counter, frame)
    _n_samples += 1
    if _n_samples and _n_samples % (SAMPLES_PER_SECOND * DUMP_INTERVAL) == 0:
        dump()


def prof(signum, frame) -> None:
    increment(_prof_counter, frame)


def increment(counter: Counter[tuple[str, int]], frame) -> None:
    signal.setitimer(signal.ITIMER_REAL, 0)
    signal.setitimer(signal.ITIMER_PROF, 0)
    while frame:
        code = frame.f_code
        counter[code.co_filename, frame.f_lineno] += 1
        # move up the stack
        frame = frame.f_back
    signal.setitimer(signal.ITIMER_REAL, SAMPLE_INTERVAL, SAMPLE_INTERVAL)
    signal.setitimer(signal.ITIMER_PROF, SAMPLE_INTERVAL, SAMPLE_INTERVAL)


def fmt_html_line(
    stats: Counter[tuple[str, int]],
    filename: str,
    no: int,
    line: str,
    total_samples: int,
) -> str:
    samples = stats.get((filename, no + 1), None)
    if samples:
        k = 0xFF * samples // total_samples
        r = 0xFF
        g = 0xFF - k
        b = 0xFF - k
        attrs = ' style="background: #%02x%02x%02x"' % (r, g, b)
        seconds = "% 7.2f" % samples
    else:
        attrs = ""
        seconds = " " * 7
    return "<pre%s>%s %s</pre>" % (
        attrs,
        seconds,
        line if line.strip() else "&nbsp;",
    )


def dump() -> None:
    signal.setitimer(signal.ITIMER_REAL, 0)
    signal.setitimer(signal.ITIMER_PROF, 0)
    out = Path("spyprof")
    if not out.exists():
        out.mkdir()
    formatter = HtmlFormatter(nowrap=True)
    styles = formatter.get_style_defs()
    for counter, path in (
        (_real_counter, out / "real.html"),
        (_prof_counter, out / "prof.html"),
    ):
        if not counter:
            continue
        maxtime = max(counter.values())
        Path(path).write_text(
            """<!doctype html>
            <html>
            <head>
                <style type="text/css">
                    {}
                    h1, pre {{
                        margin: 0.2em;
                    }}
                </style>
            </head>
            <body>
                {}
            </body>
            </html>""".format(
                styles,
                "\n".join(
                    "<h1>%s</h1>" % filename
                    + "\n".join(
                        fmt_html_line(counter, filename, no, line, maxtime)
                        for no, line in enumerate(
                            highlight(line, PythonLexer(), formatter)
                            for line in Path(filename).read_text().splitlines()
                        )
                    )
                    for filename in set(filename for (filename, line) in counter)
                    if Path(filename).exists()
                    and not set(Path(filename).parents)
                    & set(map(Path, site.getsitepackages()))
                ),
            )
        )
        print("spyprof: profiling report written to %s" % path)


signal.signal(signal.SIGALRM, alarm)
signal.signal(signal.SIGPROF, prof)
signal.setitimer(signal.ITIMER_REAL, SAMPLE_INTERVAL, SAMPLE_INTERVAL)
signal.setitimer(signal.ITIMER_PROF, SAMPLE_INTERVAL, SAMPLE_INTERVAL)
atexit.register(dump)
