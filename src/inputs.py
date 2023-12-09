import numpy as np

from typing import Iterator

from src.base import AudioStream
from src.services import midi_note_to_frequency, generate_harmonics


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


class NoteStream(AudioStream):
    def __init__(self, chunk_size: int, sample_rate: int):
        super().__init__(sample_rate=sample_rate, chunk_size=chunk_size)
        self._harmonic_profile = None
        self._velocity = 0
        self.note = 0

    def set_velocity(self, value: int):
        self._velocity = value
        return self

    def set_note(self, value: int):
        self.note = value
        return self

    @property
    def frequency(self):
        return midi_note_to_frequency(self.note)

    @property
    def volume(self):
        return self._velocity / 127

    def add_harmonic_profile(self, harmonics: tuple[tuple[float, float], ...]):
        """
        param harmonics: A list of tuples, each tuple containing a harmonic multiple and its relative amplitude.
                         For example, [(2, 0.5), (3, 0.25)] would add the first and second harmonics at half
                        and a quarter of the fundamental's amplitude, respectively.
        """
        self._harmonic_profile = harmonics
        return self

    def iterable(self):
        return generate_harmonics(
            self.frequency,
            chunk_size=self.chunk_size,
            sample_rate=self.sample_rate,
            volume=self.volume,
            harmonics_info=self._harmonic_profile
        )


class PlaceholderAudioStream(AudioStream):
    def __init__(self, chunk_size: int, sample_rate: int):
        super().__init__(sample_rate=sample_rate, chunk_size=chunk_size)
        self.current_stream = ConstantAudioStream(np.zeros(chunk_size, dtype=np.float32), sample_rate)

    def set_stream(self, new_stream: AudioStream):
        self.current_stream = new_stream

    def iterable(self) -> Iterator:
        while True:
            yield from self.current_stream
