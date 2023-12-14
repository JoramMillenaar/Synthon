from typing import Iterator

import numpy as np

from src.base import AudioStream
from src.composer import AudioStreamComposer


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
        self.volume = 0
        self.frequency = 0

    def set_volume(self, value: float):
        self.volume = value
        return self

    def set_frequency(self, value: float):
        self.frequency = value
        return self

    def iterable(self):
        t = 0
        while True:
            samples = np.arange(t, t + self.chunk_size, dtype=np.float32) / self.sample_rate
            chunk = np.sin(2 * np.pi * self.frequency * samples) * self.volume
            yield chunk
            t += self.chunk_size


class HarmonicStream(AudioStream):
    def __init__(self,
                 harmonics: dict[int, float],
                 effect_pipeline,
                 frequency: float,
                 volume: float,
                 chunk_size: int,
                 sample_rate: int
                 ):
        super().__init__(sample_rate=sample_rate, chunk_size=chunk_size)
        self.volume = volume
        self.frequency = frequency
        self.harmonics = harmonics
        self.effect_pipeline = effect_pipeline
        self.composer = AudioStreamComposer(sample_rate, chunk_size)
        self._prime_composer()

    def _prime_composer(self):
        for multiple, amplitude in self.harmonics.items():
            stream = self.effect_pipeline.build(frequency=self.frequency * multiple, volume=amplitude)
            self.composer.add_stream(stream, identifier=multiple)

    def iterable(self):
        return self.composer

    def start_closing(self):
        self.composer.start_closing()
        super().start_closing()


class PlaceholderAudioStream(AudioStream):
    def __init__(self, chunk_size: int, sample_rate: int):
        super().__init__(sample_rate=sample_rate, chunk_size=chunk_size)
        self.current_stream = ConstantAudioStream(np.zeros(chunk_size, dtype=np.float32), sample_rate)

    def set_stream(self, new_stream: AudioStream):
        self.current_stream = new_stream

    def iterable(self) -> Iterator:
        while True:
            yield from self.current_stream
