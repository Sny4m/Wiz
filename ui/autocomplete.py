from prompt_toolkit.completion import Completer, Completion
from prompt_toolkit.document import Document


class WizCompleter(Completer):

    def __init__(self, commands):
        self.commands = commands

    def get_completions(self, document: Document, complete_event):
        text = document.text_before_cursor

        if not text.startswith("/"):
            return

        query = text.lower()

        for command, description in self.commands:
            if command.startswith(query):
                yield Completion(
                    command,
                    start_position=-len(text),
                    display=command,
                    display_meta=description,
                )
