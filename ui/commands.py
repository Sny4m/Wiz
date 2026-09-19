from pathlib import Path
import sys

COMMANDS = [
    ("/help", "Show available commands"),
    ("/clear", "Clear the conversation"),
    ("/status", "Show WIZ status"),
    ("/about", "About WIZ and its creator"),
    ("/memory", "Show memory status"),
    ("/tools", "Show connected tools"),
    ("/version", "Show WIZ version"),
    ("/reset", "Restart WIZ"),
    ("/exit", "Exit WIZ"),
]


def handle_command(command):
    # Import the UI functions lazily to avoid circular imports.
    from .terminal import (
        clear_ui,
        reset_wiz,
        show_about,
        show_command_menu,
        show_memory,
        show_status,
        show_tools,
        show_version,
    )

    command = command.strip()

    if command == "/":
        show_command_menu()
        return True

    parts = command.split()
    if not parts:
        return True

    name = parts[0].lower()

    if name == "/help":
        show_command_menu()
        return True

    if name == "/clear":
        clear_ui()
        return True

    if name == "/status":
        show_status()
        return True

    if name == "/about":
        show_about()
        return True

    if name == "/memory":
        show_memory()
        return True

    if name == "/tools":
        show_tools()
        return True

    if name == "/version":
        show_version()
        return True

    if name == "/reset":
        reset_wiz()
        return True

    if name == "/exit":
        return False

    # Preserve the original unknown-command UI.
    from rich.console import Console
    console = Console()
    console.print()
    console.print(" " * 2 + f"Unknown command: {name}", style="dim")
    console.print(" " * 2 + "Type / to see commands.", style="dim")
    console.print()
    return True
