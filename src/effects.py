import itertools

import numpy as np

from src.base import AudioStream, AudioStreamDecorator
from src.dataclasses import Vibrato, Tremolo, ADSRProfile
from src.services import buffer_stream


class ADSRStreamDecorator(AudioStreamDecorator):
    def __init__(self, stream: AudioStream, profile: ADSRProfile):
        super().__init__(stream)
        self.profile = profile

        self._gen = buffer_stream(
            itertools.chain(
                self._gradient_generator(profile.attack, start=0, end=1),
                self._gradient_generator(profile.decay, start=1, end=profile.sustain_amplitude),
                self._generate_sustain_phase(),
                self._gradient_generator(profile.decay, start=profile.sustain_amplitude, end=0),
                [np.zeros(self.chunk_size, dtype=np.float32)]
            ), self.chunk_size
        )

    def _gradient_generator(self, time: float, start: float = 0, end: float = 1):
        duration = int(time * self.sample_rate)
        phase_gradient = np.linspace(start, end, duration)
        for t in range(0, duration, self.chunk_size):
            yield phase_gradient[t:t + self.chunk_size]

    def _generate_sustain_phase(self):
        if self.profile.sustain_till_close:
            while not self.is_closing:
                yield np.ones(self.chunk_size, dtype=np.float32) * self.profile.sustain_amplitude
        else:
            sustain_duration = int(self.profile.sustain * self.sample_rate)
            for _ in range(0, sustain_duration, self.chunk_size):
                yield np.ones(self.chunk_size, dtype=np.float32) * self.profile.sustain_amplitude

    def transform(self, stream_item):
        return stream_item * next(self._gen)


class VibratoDecorator(AudioStreamDecorator):
    def __init__(self, stream: AudioStream, profile: Vibrato):
        super().__init__(stream)
        self.profile = profile
        self.lfo_phase = 0  # (Low-Frequency Oscillator)

    def compute_lfo(self):
        t = np.arange(self.chunk_size) / self.sample_rate
        lfo = np.sin(2 * np.pi * self.profile.rate * t + self.lfo_phase)
        self.lfo_phase += 2 * np.pi * self.profile.rate * self.chunk_size / self.sample_rate
        self.lfo_phase %= 2 * np.pi
        return lfo

    def transform(self, stream_item):
        lfo = self.compute_lfo()
        vibrato_effect = 1 + self.profile.depth * lfo
        return stream_item * vibrato_effect


class TremoloDecorator(AudioStreamDecorator):
    def __init__(self, stream: AudioStream, profile: Tremolo):
        super().__init__(stream)
        self.profile = profile
        self.lfo_phase = 0  # (Low-Frequency Oscillator)

    def compute_lfo(self):
        t = np.arange(self.chunk_size) / self.sample_rate
        lfo = np.sin(2 * np.pi * self.profile.rate * t + self.lfo_phase)
        self.lfo_phase += 2 * np.pi * self.profile.rate * self.chunk_size / self.sample_rate
        self.lfo_phase %= 2 * np.pi
        return lfo

    def transform(self, stream_item):
        lfo = self.compute_lfo()
        tremolo_effect = 1 - self.profile.depth + self.profile.depth * lfo
        return stream_item * tremolo_effect
