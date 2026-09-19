import random
import time

from rich.console import Console
from rich.live import Live
from rich.text import Text


WAVE_CHARS = "▁▂▃▄▅▆▇█"


def _frame(width=24):
    return "".join(random.choice(WAVE_CHARS[:7]) for _ in range(width))


def voice_graph(
    duration=None,
    width=24,
    left_padding=2,
    color="#C9A27E",
):
    """
    Animated terminal voice graph.

    duration=None:
        Keep animating until the caller stops Live.

    duration=<seconds>:
        Animate for that many seconds.
    """
    console = Console()
    started = time.monotonic()

    with Live(console=console, refresh_per_second=12) as live:
        while duration is None or time.monotonic() - started < duration:
            text = Text()
            text.append(" " * left_padding)
            text.append("VOICE  ", style="dim")
            text.append(_frame(width), style=color)

            live.update(text)
            time.sleep(0.08)


def show_voice():
    """One animated burst suitable for after a WIZ response."""
    voice_graph(duration=0.8)
