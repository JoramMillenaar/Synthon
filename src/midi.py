from typing import Callable

import mido
from mido import Message


class MidiInputHandler:
    def __init__(self, port_name: str):
        self.port_name = port_name
        self.observers: dict[int, list[Callable[[Message], ...]]] = {c: [] for c in range(16)}
        self.device = mido.open_input(self.port_name, callback=self.notify_observers)

    def register_observer(self, observer: Callable[[Message], ...], channel: int):
        self.observers[channel].append(observer)

    def notify_observers(self, message: mido.Message):
        for observer in self.observers[message.channel]:
            observer(message)
