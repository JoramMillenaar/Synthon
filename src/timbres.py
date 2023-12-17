from src.dataclasses import Timbre, ADSRProfile, Vibrato, Tremolo, Harmonic

default_timbre = Timbre(
    envelope=ADSRProfile(
        attack=0.1,  # Quick attack for a sharp onset
        decay=0.4,  # Moderate decay
        sustain_amplitude=0.7,  # Sustain at 70% amplitude
        release=0.5,  # Somewhat prolonged release
        sustain=2.0,  # Sustain for 2 seconds
        sustain_till_close=False,
    ),
    vibrato=Vibrato(
        rate=5.5,  # Vibrato rate in Hz
        depth=0.06,  # Moderate depth for a subtle effect
    ),
    tremolo=Tremolo(
        rate=4.0,  # Tremolo rate in Hz
        depth=0.1,  # Significant depth for a strong effect
    ),
    harmonics=(
        Harmonic(multiple=2, amplitude=0.5, sustain=None),  # First harmonic at half amplitude
        Harmonic(multiple=3, amplitude=0.3, sustain=None),  # Second harmonic at lower amplitude
    )
)
