from functools import cached_property

from src.base import AudioStream
from src.dataclasses import Timbre
from src.inputs import SineWaveStream, TimbredNoteStream


class MusicNote(AudioStream):
    def __init__(self, frequency: float, amplitude: float, sample_rate: int, chunk_size: int):
        super().__init__(sample_rate=sample_rate, chunk_size=chunk_size)
        self.frequency = frequency
        self.amplitude = amplitude
        self._timbre = None
        self._timbre_decorator = None

        self._sine_gen = SineWaveStream(
            frequency=self.frequency,
            amplitude=self.amplitude,
            chunk_size=self.chunk_size,
            sample_rate=self.sample_rate
        )

    @property
    def timbre(self):
        return self._timbre

    @timbre.setter
    def timbre(self, value: Timbre):
        self._timbre = value

    @cached_property
    def stream(self):
        if self._timbre:
            return TimbredNoteStream(
                frequency=self.frequency,
                amplitude=self.amplitude,
                timbre_profile=self._timbre,
                chunk_size=self.chunk_size,
                sample_rate=self.sample_rate
            )
        else:
            return self._sine_gen

    def start_closing(self):
        self.stream.start_closing()
        super().start_closing()

    def iterable(self):
        return self.stream


class MusicNoteFactory:
    def __init__(self, sample_rate: int, chunk_size: int, timbre: Timbre = None):
        self.sample_rate = sample_rate
        self.chunk_size = chunk_size
        self.timbre = timbre

    def create_note(self, frequency: float, amplitude: float) -> MusicNote:
        note = MusicNote(frequency=frequency, amplitude=amplitude,
                         sample_rate=self.sample_rate, chunk_size=self.chunk_size)
        if self.timbre:
            note.timbre = self.timbre
        return note
