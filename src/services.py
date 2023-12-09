import numpy as np
import sounddevice as sd

BASE_A4 = 440


def midi_note_to_frequency(note: int) -> float:
    return BASE_A4 * (2.0 ** ((note - 69) / 12.0))


def generate_sine_wave(freq: float, chunk_size: int, sample_rate: int, volume: float):
    t = 0
    while True:
        samples = np.arange(t, t + chunk_size, dtype=np.float32) / sample_rate
        chunk = np.sin(2 * np.pi * freq * samples) * volume
        yield chunk
        t += chunk_size


def play_sound(output_device: sd.RawOutputStream, chunk: np.array):
    output_device.write(np.clip(chunk, -1, 1))


def array_to_wav_format(data: np.array):
    """Convert the float32 array to int16 to write to WAV file"""
    return (data * 32767).astype(np.int16).tobytes()


def generate_harmonics(base_freq: float, chunk_size: int, sample_rate: int, volume: float,
                       harmonics_info: tuple[tuple[int, float], ...]):
    harmonic_gens = []
    for multiple, amplitude in harmonics_info:
        harmonic_gens.append(generate_sine_wave(multiple * base_freq, chunk_size, sample_rate, amplitude))

    for chunk in generate_sine_wave(base_freq, chunk_size, sample_rate, volume):
        yield np.sum(np.array([chunk, *[next(h) for h in harmonic_gens]], dtype=np.float32), axis=0)
