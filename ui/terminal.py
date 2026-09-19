import sys
import time
import random
from datetime import datetime

from rich.console import Console
from rich.text import Text

from prompt_toolkit import PromptSession
from prompt_toolkit.styles import Style

from ui.commands import COMMANDS, handle_command
from ui.autocomplete import WizCompleter
from voice.tts import speak, startup_greeting
from voice.graph import show_voice
from voice.stt import listen


# ==================================================
# CONSOLE
# ==================================================

console = Console()

WIZ_COLOR = "#C9A27E"
WIZ_FULL_NAME = "Wise Interactive Companion"

WIZ_VERSION = "0.1.0"

CREATOR_NAME = "Sanyam"
CREATOR_GITHUB = "sny4m"

UI_LEFT_PADDING = 2

WAVE_CHARS = "▁▂▃▄▅▆▇█"

LOGO_GAP = 2


# ==================================================
# ASCII WIZ
# ==================================================

W_ASCII = [
    "██╗       ██╗",
    "██║       ██║",
    "██║  █╗   ██║",
    "██║ ███╗  ██║",
    "╚███╔███╔╝██║",
    " ╚══╝╚══╝ ╚═╝",
]

I_ASCII = [
    "██╗",
    "██║",
    "██║",
    "██║",
    "██║",
    "╚═╝",
]

Z_ASCII = [
    "███████╗",
    "╚════██║",
    "    ███╔╝",
    "   ███╔╝",
    "  ███████╗",
    "  ╚══════╝",
]


# ==================================================
# LOGO
# ==================================================

def build_final_logo():

    height = max(
        len(W_ASCII),
        len(I_ASCII),
        len(Z_ASCII),
    )

    lines = []

    for row in range(height):

        w = (
            W_ASCII[row]
            if row < len(W_ASCII)
            else ""
        )

        i = (
            I_ASCII[row]
            if row < len(I_ASCII)
            else ""
        )

        z = (
            Z_ASCII[row]
            if row < len(Z_ASCII)
            else ""
        )

        lines.append(
            w
            + (" " * LOGO_GAP)
            + i
            + (" " * LOGO_GAP)
            + z
        )

    return lines


FINAL_LOGO = build_final_logo()


# ==================================================
# PROMPT SESSION
# ==================================================

wiz_style = Style.from_dict({
    # Black autocomplete popup
    "completion-menu": "bg:#000000",

    # Normal command text — inherit normal terminal color
    "completion-menu.completion": "bg:#000000 #C9A27E",

    # Selected command
    "completion-menu.completion.current": "bg:#000000 #FFFFFF",

    # Command description
    "completion-menu.meta": "bg:#000000 #888888",

    # Description when selected
    "completion-menu.meta.completion.current": "bg:#000000 #AAAAAA",

    # Scrollbar
    "scrollbar.background": "bg:#000000",
    "scrollbar.button": "bg:#333333",
})

session = PromptSession(
    completer=WizCompleter(COMMANDS),
    complete_while_typing=True,
    style=wiz_style,
)


# ==================================================
# TERMINAL CONTROL
# ==================================================

def clear_screen():

    sys.stdout.write("\033[2J")
    sys.stdout.write("\033[3J")
    sys.stdout.write("\033[H")
    sys.stdout.flush()


def move_home():

    sys.stdout.write("\033[H")


# ==================================================
# STARTUP ANIMATION
# ==================================================

def draw_startup_frame(
    w_y=None,
    i_y=None,
    z_y=None,
):

    move_home()

    # Completely erase old animation frame.
    for _ in range(16):
        sys.stdout.write("\033[2K\n")

    move_home()

    terminal_width = console.width
    canvas_height = 14

    canvas = [
        [" "] * terminal_width
        for _ in range(canvas_height)
    ]

    w_width = max(
        len(line)
        for line in W_ASCII
    )

    i_width = max(
        len(line)
        for line in I_ASCII
    )

    w_x = UI_LEFT_PADDING

    i_x = (
        w_x
        + w_width
        + LOGO_GAP
    )

    z_x = (
        i_x
        + i_width
        + LOGO_GAP
    )

    def draw_letter(
        art,
        x,
        y,
    ):

        if y is None:
            return

        for row, line in enumerate(art):

            target_y = y + row

            if (
                target_y < 0
                or target_y >= canvas_height
            ):
                continue

            for column, char in enumerate(line):

                if char == " ":
                    continue

                target_x = x + column

                if (
                    0
                    <= target_x
                    < terminal_width
                ):

                    canvas[target_y][
                        target_x
                    ] = char

    draw_letter(
        W_ASCII,
        w_x,
        w_y,
    )

    draw_letter(
        I_ASCII,
        i_x,
        i_y,
    )

    draw_letter(
        Z_ASCII,
        z_x,
        z_y,
    )

    for row in canvas:

        line = "".join(row).rstrip()

        sys.stdout.write(
            line + "\n"
        )

    sys.stdout.flush()


def animate_letter(
    positions,
    name,
    target_y=3,
    start_y=-7,
):

    frames = 7

    for frame in range(frames):

        progress = (
            frame
            / (frames - 1)
        )

        eased = (
            1
            - (1 - progress) ** 3
        )

        y = round(
            start_y
            + (
                target_y
                - start_y
            ) * eased
        )

        positions[name] = y

        draw_startup_frame(
            positions["W"],
            positions["I"],
            positions["Z"],
        )

        time.sleep(0.035)

    # Small bounce on landing.

    for y in (
        target_y - 1,
        target_y,
    ):

        positions[name] = y

        draw_startup_frame(
            positions["W"],
            positions["I"],
            positions["Z"],
        )

        time.sleep(0.04)


def startup_animation():

    clear_screen()

    positions = {
        "W": None,
        "I": None,
        "Z": None,
    }

    animate_letter(
        positions,
        "W",
    )

    animate_letter(
        positions,
        "I",
    )

    animate_letter(
        positions,
        "Z",
    )

    draw_startup_frame(
        3,
        3,
        3,
    )

    time.sleep(0.2)

    clear_screen()


# ==================================================
# TIME
# ==================================================

def current_time():

    return datetime.now().strftime(
        "%H:%M:%S"
    )


def current_date():

    return datetime.now().strftime(
        "%A, %d %b %Y"
    )


# ==================================================
# HEADER
# ==================================================

def show_header():

    # ----------------------------------------------
    # WIZ ASCII
    # ----------------------------------------------

    for line in FINAL_LOGO:

        console.print(
            " " * UI_LEFT_PADDING
            + line,
            style=f"bold {WIZ_COLOR}",
        )

    console.print()

    # ----------------------------------------------
    # Brand + clock
    # ----------------------------------------------

    brand = WIZ_FULL_NAME
    clock_text = current_time()

    available = (
        console.width
        - UI_LEFT_PADDING
        - len(brand)
        - len(clock_text)
        - 2
    )

    gap = max(
        4,
        available,
    )

    header = Text()

    header.append(
        " " * UI_LEFT_PADDING
    )

    header.append(
        brand,
        style="dim",
    )

    header.append(
        " " * gap
    )

    header.append(
        clock_text,
        style="bold white",
    )

    console.print(header)

    # ----------------------------------------------
    # Date
    # ----------------------------------------------

    console.print(
        " " * UI_LEFT_PADDING
        + current_date(),
        style="dim",
    )

    console.print()

    # ----------------------------------------------
    # Status
    # ----------------------------------------------

    status = Text()

    status.append(
        " " * UI_LEFT_PADDING
    )

    status.append(
        "● ",
        style=WIZ_COLOR,
    )

    status.append(
        "Online",
        style="white",
    )

    console.print(status)

    console.print()


# ==================================================
# COMMAND MENU
# ==================================================

def show_command_menu():

    console.print()

    console.print(
        " " * UI_LEFT_PADDING
        + "Commands",
        style=f"bold {WIZ_COLOR}",
    )

    console.print()

    for command, description in COMMANDS:

        line = Text()

        line.append(
            " " * UI_LEFT_PADDING
        )

        line.append(
            f"{command:<10}",
            style=f"bold {WIZ_COLOR}",
        )

        line.append(
            description,
            style="dim",
        )

        console.print(line)

    console.print()


# ==================================================
# ABOUT
# ==================================================

def show_about():

    console.print()

    console.print(
        " " * UI_LEFT_PADDING
        + "WIZ",
        style=f"bold {WIZ_COLOR}",
    )

    console.print(
        " " * UI_LEFT_PADDING
        + WIZ_FULL_NAME,
        style="dim",
    )

    console.print()

    console.print(
        " " * UI_LEFT_PADDING
        + f"Created by {CREATOR_NAME}",
        style="white",
    )

    console.print(
        " " * UI_LEFT_PADDING
        + f"GitHub  @{CREATOR_GITHUB}",
        style="dim",
    )

    console.print()

    console.print(
        " " * UI_LEFT_PADDING
        + "Your personal computer companion.",
        style="dim",
    )

    console.print()


# ==================================================
# STATUS
# ==================================================

def show_status():

    console.print()

    console.print(
        " " * UI_LEFT_PADDING
        + "Status",
        style=f"bold {WIZ_COLOR}",
    )

    console.print(
        " " * UI_LEFT_PADDING
        + "● WIZ online",
    )

    console.print(
        " " * UI_LEFT_PADDING
        + "Voice     ready",
        style="dim",
    )

    console.print(
        " " * UI_LEFT_PADDING
        + "Computer  ready",
        style="dim",
    )

    console.print(
        " " * UI_LEFT_PADDING
        + "Memory    ready",
        style="dim",
    )

    console.print(
        " " * UI_LEFT_PADDING
        + "MCP       ready",
        style="dim",
    )

    console.print()


# ==================================================
# MEMORY
# ==================================================

def show_memory():

    console.print()

    console.print(
        " " * UI_LEFT_PADDING
        + "Memory",
        style=f"bold {WIZ_COLOR}",
    )

    console.print(
        " " * UI_LEFT_PADDING
        + "Local session memory ready",
        style="dim",
    )

    console.print()


# ==================================================
# TOOLS
# ==================================================

def show_tools():

    console.print()

    console.print(
        " " * UI_LEFT_PADDING
        + "Tools",
        style=f"bold {WIZ_COLOR}",
    )

    console.print(
        " " * UI_LEFT_PADDING
        + "Computer control    ready",
        style="dim",
    )

    console.print(
        " " * UI_LEFT_PADDING
        + "Filesystem          ready",
        style="dim",
    )

    console.print(
        " " * UI_LEFT_PADDING
        + "MCP                 ready",
        style="dim",
    )

    console.print()


# ==================================================
# VERSION
# ==================================================

def show_version():

    console.print()

    console.print(
        " " * UI_LEFT_PADDING
        + f"WIZ {WIZ_VERSION}",
        style="dim",
    )

    console.print()


# ==================================================
# CLEAR
# ==================================================

def clear_ui():

    clear_screen()

    show_header()

    show_voice()


# ==================================================
# RESET
# ==================================================

def reset_wiz():

    clear_screen()

    startup_animation()

    show_header()

    console.print(
        " " * UI_LEFT_PADDING
        + "Session restarted.",
        style="bold white",
    )

    console.print(
        " " * UI_LEFT_PADDING
        + "WIZ is ready.",
        style="dim",
    )

    console.print()

    show_voice()


# ==================================================
# USER MESSAGE
# ==================================================

def show_user_message(
    message,
):

    console.print(
        " " * UI_LEFT_PADDING
        + "You",
        style="bold white",
    )

    console.print(
        " " * UI_LEFT_PADDING
        + f"› {message}",
    )

    console.print()


# ==================================================
# WIZ MESSAGE
# ==================================================

def show_wiz_message(
    message,
    response_time,
):

    console.print(
        " " * UI_LEFT_PADDING
        + "WIZ",
        style=f"bold {WIZ_COLOR}",
    )

    console.print(
        " " * UI_LEFT_PADDING
        + f"› {message}",
    )

    console.print()

    console.print(
        " " * UI_LEFT_PADDING
        + f"Response {response_time:.2f}s",
        style="dim",
    )

    console.print()


# ==================================================
# DUMMY BRAIN
# ==================================================

def dummy_response(
    message,
):

    message = (
        message
        .lower()
        .strip()
    )

    if (
        "hello" in message
        or "hi" in message
    ):

        return (
            "Hey. I'm WIZ. "
            "What are we working on?"
        )

    if "what can you do" in message:

        return (
            "I can talk with you, "
            "control your computer, "
            "work with files, and "
            "connect to your tools."
        )

    if "open notepad" in message:

        return "Opening Notepad..."

    if "who are you" in message:

        return (
            "I'm WIZ — your personal "
            "computer companion."
        )

    if "how are you" in message:

        return (
            "Doing good. Ready when you are."
        )

    return "Got it. I'm listening."


# ==================================================
# STARTUP
# ==================================================

def startup():

    startup_animation()

    show_header()

    console.print(
        " " * UI_LEFT_PADDING
        + "WIZ is ready.",
        style="dim",
    )

    console.print()

    show_voice()

    # Voice-only startup greeting. Nothing is printed as the greeting.
    speak(startup_greeting())


# ==================================================
# SHUTDOWN
# ==================================================

def shutdown():

    console.print()

    console.print(
        " " * UI_LEFT_PADDING
        + "WIZ is shutting down...",
        style=f"bold {WIZ_COLOR}",
    )

    time.sleep(0.4)

    console.print(
        " " * UI_LEFT_PADDING
        + "Saving session...",
        style="dim",
    )

    time.sleep(0.35)

    console.print(
        " " * UI_LEFT_PADDING
        + "✓ Done",
        style=WIZ_COLOR,
    )

    console.print()

    console.print(
        " " * UI_LEFT_PADDING
        + "Goodbye.",
        style="dim",
    )

    console.print()


# ==================================================
# MAIN
# ==================================================

def run():

    startup()

    try:

        while True:

            console.print(
                " " * UI_LEFT_PADDING
                + "Listening",
                style="dim",
            )

            # --------------------------------------
            # Interactive prompt-toolkit input
            # --------------------------------------

            message = listen()

            if not message:
                message = session.prompt(
                    " " * UI_LEFT_PADDING
                    + "› "
                )

            if not message.strip():
                continue

            # --------------------------------------
            # Slash command
            # --------------------------------------

            if message.startswith("/"):

                should_continue = (
                    handle_command(message)
                )

                if not should_continue:
                    break

                continue

            # --------------------------------------
            # Normal WIZ message
            # --------------------------------------

            start = time.perf_counter()

            response = dummy_response(
                message
            )

            elapsed = (
                time.perf_counter()
                - start
            )

            show_user_message(
                message
            )

            show_wiz_message(
                response,
                elapsed,
            )

            speak(response)
            show_voice()

    except KeyboardInterrupt:

        pass

    except EOFError:

        pass

    finally:

        shutdown()


# ==================================================
# ENTRY POINT
# ==================================================

if __name__ == "__main__":

    run()
