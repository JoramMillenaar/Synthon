<p align="center">
    <img src="logo.png" alt="drawing" width="250" />
</p>

# SYNTHON - Python Music Synthesis Toolkit

This suite of Python scripts offers a range of tools for audio processing and music synthesis. It includes a variety of modules for generating, manipulating, and outputting audio data. While each script has its specific functionality, they collectively form a toolkit for synthesizing and processing audio in Python.

The synthesizer is controlled using MIDI data. If you don't have a MIDI device on hand, checkout my other project [here](https://github.com/jofoks/Virtual-MIDI-Keyboard) to make your PC's keyboard into a MIDI keyboard.

## Features

- **Command-Line Interface**: Main commands in `synthon.py` for integrating different modules.
- **Audio Stream Processing**: Base classes for handling audio streams with ease.
- **MIDI Input Handling**: MIDI input processing capabilities in `midi.py`.
- **Audio Output Management**: Classes for audio playback and file output in `outputs.py`.
- **Audio Input Streams**: Various types of audio input streams in `inputs.py`.
- **Audio Effects**: Multiple audio effects like fade-in, fade-out, delay, and multiplication in `effects.py`.
- **Synthesizer Functionalities**: Core synthesizer features in `synth.py`.
- **Effect Pipeline Building**: Constructing and customizing audio effect pipelines in `builder.py`.

## Installation

Ensure Python is installed on your system. Depending on the modules, additional libraries may be required. Install them using pip:

```bash
pip install mido numpy sounddevice
```

## Usage

Run the main script from the command line with the necessary options:

```
python synthon.py [OPTIONS]
```

Options:
- `--multiplier`: A float specifying the effect multiplier. Default is 0.3.
- `--fade_in`: An integer specifying the fade-in duration in seconds. Default is 0.2.
- `--fade_out`: An integer specifying the fade-out duration in seconds. Default is 0.2.
- `--sample_rate`: An integer specifying the sample rate for the synthesizer. Default is 44100.
- `--chunk_size`: An integer specifying the chunk size for the synthesizer. Default is 512.
- `--disable_speaker`: A flag to disable output to the speaker. It's set to true by default.
- `--stream_to_file`: A flag to enable streaming to a file. It's set to false by default.
- `--filename`: A string specifying the filename for the output file. This option is required if `--stream_to_file` is enabled.
- `--port_name`: A string specifying the MIDI input port name. Default is 'IAC Driver Bus 1'.

Note:
- The `--stream_to_file` option requires `--filename` to be specified.
- Default values are used if specific options are not provided.
### Example

```bash
python synthon.py --stream_to_file --filename example.wav --fade_in 0.5
```

This command runs the `synthon.py` script with specified options.

## Project Files

- `base.py`: Base classes for audio streaming.
- `synthon.py`: Main command interface for the toolkit.
- `composer.py`: Audio stream composition tools.
- `services.py`: Utility functions for audio processing.
- `midi.py`: MIDI input handling.
- `outputs.py`: Audio playback and file output functionalities.
- `inputs.py`: Different types of audio input streams.
- `effects.py`: Audio effects implementation.
- `synth.py`: Core synthesizer functionalities.
- `builder.py`: Construction of audio effect pipelines.
