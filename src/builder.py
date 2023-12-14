from abc import ABC

from src.base import AudioStream
from src.effects import MultiplyAudioStreamDecorator, ADSRStreamDecorator
from src.inputs import HarmonicStream, SineWaveStream
from src.outputs import AudioPlaybackDecorator, AudioFileOutputDecorator


class DecoratorPipeline(ABC):
    def __init__(self):
        self._decorators = {}

    def build(self, audio_source: AudioStream):
        for decorator in self._decorators.values():
            audio_source = decorator(audio_source)
        return audio_source


class NoteAudioStreamBuilder:
    def __init__(self, chunk_size, sample_rate):
        self.chunk_size = chunk_size
        self.sample_rate = sample_rate
        self._decorators = {}
        self._harmonics = None

    def set_volume(self, value: float):
        self._decorators['multiply'] = lambda s: MultiplyAudioStreamDecorator(s).set_multiplier(value)

    def set_adsr(self, attack_time: float, decay_time: float, release_time: float, sustain_level: float):
        self._decorators['adsr'] = lambda s: ADSRStreamDecorator(
            s, attack_time=attack_time, decay_time=decay_time, release_time=release_time, sustain_level=sustain_level
        )

    def set_harmonics(self, harmonics: dict[int, float]):
        self._harmonics = harmonics

    def set_vibrato(self):
        raise NotImplementedError

    def set_tremelo(self):
        raise NotImplementedError

    def build(self, frequency: float, volume: float):
        if self._harmonics:
            effect = NoteAudioStreamBuilder(self.chunk_size, self.sample_rate)
            effect._decorators = self._decorators
            s = HarmonicStream(
                harmonics=self._harmonics,
                effect_pipeline=effect,
                chunk_size=self.chunk_size,
                sample_rate=self.sample_rate,
                frequency=frequency,
                volume=volume
            )
        else:
            s = SineWaveStream(self.chunk_size, self.sample_rate).set_frequency(frequency).set_volume(volume)
            for decorator in list(self._decorators.values()):
                s = decorator(s)
        return s


class OutputPipeline(DecoratorPipeline):
    def enable_speaker_playback(self):
        self._decorators['playback'] = lambda s: AudioPlaybackDecorator(s)

    def enable_file_output(self, filename: str):
        self._decorators['fileStream'] = lambda s: AudioFileOutputDecorator(s, filename=filename)
