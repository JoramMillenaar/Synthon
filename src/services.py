import json
import os
from typing import Iterator

import numpy as np
import sounddevice as sd


PROJECT_ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATES_DIR = os.path.join(PROJECT_ROOT_DIR, 'templates')
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


def buffer_stream(generator: Iterator[np.array], buffer_size: int):
    """Ensures the yielded chunks are of length 'buffer_size'"""
    current_buffer = np.array([], dtype=float)
    for phase_slice in generator:
        remaining_space = buffer_size - len(current_buffer)
        if len(phase_slice) <= remaining_space:
            current_buffer = np.concatenate((current_buffer, phase_slice))
        else:
            current_buffer = np.concatenate((current_buffer, phase_slice[:remaining_space]))
            yield current_buffer

            current_buffer = phase_slice[remaining_space:]

        if len(current_buffer) == buffer_size:
            yield current_buffer
            current_buffer = np.array([], dtype=float)

    if len(current_buffer) > 0:
        padded_buffer = np.pad(current_buffer, (0, buffer_size - len(current_buffer)), mode='constant')
        yield padded_buffer


def load_template(filepath):
    full_path = os.path.join(TEMPLATES_DIR, filepath)
    if not os.path.exists(full_path):
        raise FileNotFoundError(f"Template file '{full_path}' not found.")

    with open(full_path, 'r') as file:
        template = json.load(file)

    # Special handling for harmonics
    if 'harmonic' in template:
        template['harmonic'] = [','.join(map(str, h)) for h in template['harmonic']]

    return template
