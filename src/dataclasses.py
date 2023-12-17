from dataclasses import dataclass
from typing import Optional


@dataclass
class ADSRProfile:
    attack: float
    decay: float
    sustain_amplitude: float
    release: float
    sustain: Optional[float] = None
    sustain_till_close: bool = False


@dataclass
class Harmonic:
    multiple: int
    amplitude: float
    sustain: float | None


@dataclass
class Vibrato:
    rate: float  # Frequency of vibrato modulation (in Hz)
    depth: float  # Depth of vibrato modulation (usually in cents or a fraction of a semitone)


@dataclass
class Tremolo:
    rate: float  # Frequency of tremolo modulation (in Hz)
    depth: float  # Depth of tremolo modulation (amplitude variation, usually a percentage)


@dataclass
class Timbre:
    envelope: ADSRProfile
    vibrato: Optional[Vibrato] = None
    tremolo: Optional[Tremolo] = None
    harmonics: Optional[tuple[Harmonic, ...]] = None


guitar_envelope = ADSRProfile(attack=.1, decay=.1, sustain_amplitude=.7, release=.1)
guitar_timbre = Timbre(envelope=guitar_envelope)
