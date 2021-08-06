from typing import List, Reversible, Tuple
import textwrap
import tcod
import color


class Message:
    def __init__(self, text: str, fg: Tuple[int, int, int]):
        self.plainText = text
        self.fg = fg
        self.count = 1

    @property
    def fullText(self) -> str:
        if self.count > 1:
            return f"{self.plainText} (x{self.count})"
        return self.plainText


class MessageLog:
    def __init__(self):
        self.messages: List[Message] = []

    def addMessage(self, text: str, fg: Tuple[int, int, int] = color.white, stack: bool = True):
        if stack and len(self.messages) > 0 and text == self.messages[-1].plainText:
            self.messages[-1].count += 1
        else:
            self.messages.append(Message(text, fg))

    def render(self, console: tcod.Console, x: int, y: int, width: int, height: int):
        yOffset = height - 1

        for message in reversed(self.messages):
            for line in reversed(textwrap.wrap(message.fullText, width)):
                console.print(x=x, y=y + yOffset, string=line, fg=message.fg)
                yOffset -= 1
                if yOffset < 0:
                    return
