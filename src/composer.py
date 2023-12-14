from typing import Hashable

import numpy as np

from src.base import AudioStream


class AudioStreamComposer(AudioStream):
    def __init__(self, sample_rate: int, chunk_size: int):
        super().__init__(sample_rate, chunk_size)
        self._active_streams = {}
        self._closing_streams = []

    def add_stream(self, stream: AudioStream, identifier: Hashable):
        if identifier not in self._active_streams:
            self._active_streams[identifier] = stream

    def close_stream(self, identifier: Hashable):
        if stream := self._active_streams.get(identifier):
            del self._active_streams[identifier]
            stream.start_closing()
            self._closing_streams.append(stream)

    def start_closing(self):
        for key in list(self._active_streams.keys()):
            self.close_stream(key)
        super().start_closing()

    def iterable(self):
        while True:
            agg = np.zeros(self.chunk_size, dtype=np.float32)
            for s in list(self._active_streams.values()) + self._closing_streams:
                try:
                    agg += next(s)
                except StopIteration:
                    s.close()

            self._closing_streams = [s for s in self._closing_streams if not s.is_closed]

            yield agg
