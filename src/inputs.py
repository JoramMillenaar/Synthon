import numpy as np

from typing import Iterator

from src.base import AudioStream
from src.services import generate_sine_wave, midi_note_to_frequency


class ConstantAudioStream(AudioStream):
    def __init__(self, audio_chunk, sample_rate: int):
        super().__init__(chunk_size=len(audio_chunk), sample_rate=sample_rate)
        self.audio_chunk = audio_chunk

    def iterable(self) -> Iterator:
        while True:
            yield self.audio_chunk


class ReadStream(AudioStream):
    def __init__(self, read_stream: AudioStream):
        super().__init__(sample_rate=read_stream.sample_rate, chunk_size=read_stream.chunk_size)
        self.read_stream = read_stream

    def iterable(self) -> Iterator:
        while True:
            yield self.read_stream.current


class SineWaveStream(AudioStream):
    def __init__(self, chunk_size: int, sample_rate: int):
        super().__init__(sample_rate=sample_rate, chunk_size=chunk_size)
        self._volume = 0
        self._frequency = 0

    def set_volume(self, value: float):
        self._volume = value
        return self

    def set_frequency(self, value: float):
        self._frequency = value
        return self

    def iterable(self):
        return generate_sine_wave(
            self._frequency, chunk_size=self.chunk_size, sample_rate=self.sample_rate, volume=self._volume
        )


class MidiSineWaveStream(SineWaveStream):
    def __init__(self, chunk_size: int, sample_rate: int):
        super().__init__(sample_rate=sample_rate, chunk_size=chunk_size)
        self._velocity = 0
        self.note = 0

    def set_velocity(self, value: int):
        self._velocity = value
        self.set_volume(value / 127)
        return self

    def set_note(self, value: int):
        self.note = value
        self.set_frequency(midi_note_to_frequency(value))
        return self


class PlaceholderAudioStream(AudioStream):
    def __init__(self, chunk_size: int, sample_rate: int):
        super().__init__(sample_rate=sample_rate, chunk_size=chunk_size)
        self.current_stream = ConstantAudioStream(np.zeros(chunk_size, dtype=np.float32), sample_rate)

    def set_stream(self, new_stream: AudioStream):
        self.current_stream = new_stream

    def iterable(self) -> Iterator:
        while True:
            yield from self.current_stream
