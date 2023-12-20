import itertools

import numpy as np

from src.base import AudioStream, AudioStreamDecorator
from src.dataclasses import Vibrato, Tremolo, ADSRProfile
from src.services import buffer_stream, generate_sine_wave


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
        self.sine_gen = generate_sine_wave(
            freq=self.profile.rate,
            volume=self.profile.depth,
            sample_rate=self.sample_rate,
            chunk_size=self.chunk_size,
        )

    def transform(self, stream_item):
        vibrato_effect = 1 + self.profile.depth * next(self.sine_gen)
        return stream_item * vibrato_effect


class TremoloDecorator(AudioStreamDecorator):
    def __init__(self, stream: AudioStream, profile: Tremolo):
        super().__init__(stream)
        self.profile = profile
        self.sine_gen = generate_sine_wave(
            freq=self.profile.rate,
            volume=self.profile.depth,
            sample_rate=self.sample_rate,
            chunk_size=self.chunk_size,
        )

    def transform(self, stream_item):
        tremolo_effect = 1 - self.profile.depth + self.profile.depth * next(self.sine_gen)
        return stream_item * tremolo_effect
