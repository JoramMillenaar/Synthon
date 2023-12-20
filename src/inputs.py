from src.base import AudioStream
from src.composer import AudioStreamComposer
from src.dataclasses import Harmonic, ADSRProfile, Timbre
from src.effects import ADSRStreamDecorator, VibratoDecorator, TremoloDecorator
from src.services import generate_sine_wave


class SineWaveStream(AudioStream):
    def __init__(self, frequency: float, amplitude: float, chunk_size: int, sample_rate: int):
        super().__init__(sample_rate=sample_rate, chunk_size=chunk_size)
        self.amplitude = amplitude
        self.frequency = frequency

    def iterable(self):
        return generate_sine_wave(self.frequency, self.chunk_size, self.sample_rate, self.amplitude)


class HarmonicStream(AudioStream):
    def __init__(self,
                 frequency: float,
                 volume: float,
                 harmonics: tuple[Harmonic],
                 envelope: ADSRProfile,
                 chunk_size: int,
                 sample_rate: int
                 ):
        super().__init__(sample_rate=sample_rate, chunk_size=chunk_size)
        self.volume = volume
        self.frequency = frequency
        self.harmonics = harmonics
        self.envelope = envelope
        self.composer = AudioStreamComposer(sample_rate, chunk_size)
        self._prime_composer()

    def _prime_composer(self):
        for harmonic in self.harmonics:
            stream = SineWaveStream(
                frequency=self.frequency * harmonic.multiple,
                amplitude=harmonic.amplitude * self.volume,
                chunk_size=self.chunk_size,
                sample_rate=self.sample_rate
            )
            stream = ADSRStreamDecorator(stream, profile=self.envelope)
            self.composer.add_stream(stream, identifier=harmonic.multiple)

    def iterable(self):
        return self.composer

    def start_closing(self):
        self.composer.start_closing()
        super().start_closing()


class TimbredNoteStream(AudioStream):
    def __init__(self, frequency: float, amplitude: float, timbre_profile: Timbre, chunk_size: int, sample_rate: int):
        super().__init__(sample_rate=sample_rate, chunk_size=chunk_size)
        self.stream = SineWaveStream(
            frequency=frequency,
            amplitude=amplitude,
            chunk_size=chunk_size,
            sample_rate=sample_rate
        )

        if timbre_profile.harmonics:
            self.stream = HarmonicStream(
                frequency=frequency,
                volume=amplitude,
                harmonics=timbre_profile.harmonics,
                envelope=timbre_profile.envelope,
                sample_rate=self.sample_rate,
                chunk_size=self.chunk_size
            )
        else:
            self.stream = ADSRStreamDecorator(self.stream, timbre_profile.envelope)

        if timbre_profile.vibrato and timbre_profile.vibrato.rate and timbre_profile.vibrato.depth:
            self.stream = VibratoDecorator(self.stream, profile=timbre_profile.vibrato)

        if timbre_profile.tremolo and timbre_profile.tremolo.rate and timbre_profile.tremolo.depth:
            self.stream = TremoloDecorator(self.stream, profile=timbre_profile.tremolo)

    def start_closing(self):
        self.stream.start_closing()
        super().start_closing()

    def iterable(self):
        return self.stream
