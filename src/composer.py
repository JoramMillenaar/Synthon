import numpy as np

from src.base import AudioStream
from src.inputs import MidiSineWaveStream


class AudioStreamComposer(AudioStream):
    # TODO: generalize this composer (don't specialize in sine wave streams)

    def __init__(self, sample_rate: int, chunk_size: int):
        super().__init__(sample_rate, chunk_size)
        self._active_sine_waves = {}
        self._closing_sine_waves = []

    def add_stream(self, stream: MidiSineWaveStream, note: int):
        if note not in self._active_sine_waves:
            self._active_sine_waves[note] = stream

    def close_stream(self, note):
        if note in self._active_sine_waves:
            stream = self._active_sine_waves[note]
            del self._active_sine_waves[note]
            stream.is_closing = True
            self._closing_sine_waves.append(stream)

    def iterable(self):
        while True:
            active = [next(s) for s in list(self._active_sine_waves.values())]

            for s in self._closing_sine_waves:
                try:
                    active.append(next(s))
                except StopIteration:
                    s.close()

            self._closing_sine_waves = [s for s in self._closing_sine_waves if not s.is_closed]

            data = np.array(active, dtype=np.float32)

            if data.ndim > 1:
                res = np.sum(data, axis=0)
                yield res
            else:
                yield data
